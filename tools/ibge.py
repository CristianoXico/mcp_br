import httpx
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_cache():
    """Carrega os dados do cache"""
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cache.json')
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"municipios": {}, "estados": {}, "regioes": {}}

def salvar_cache(cache):
    """Salva os dados no cache"""
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cache.json')
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# URLs base das APIs do IBGE
BASE_URL_LOCALIDADES = "https://servicodados.ibge.gov.br/api/v1/localidades"
BASE_URL_CENSOS = "https://servicodados.ibge.gov.br/api/v2/censos"
BASE_URL_METADADOS = "https://servicodados.ibge.gov.br/api/v2/metadados-estatisticos"
BASE_URL_AGREGADOS = "https://servicodados.ibge.gov.br/api/v3/agregados"
BASE_URL_MALHAS = "https://servicodados.ibge.gov.br/api/v3/malhas"

# Timeout padrão para requisições HTTP
DEFAULT_TIMEOUT = 15.0  # segundos

def buscar_municipio_por_codigo(codigo_municipio: str) -> dict:
    """Busca informações detalhadas de um município por código"""
    try:
        cache = carregar_cache()
        if codigo_municipio in cache["municipios"]:
            return cache["municipios"][codigo_municipio]

        url = f"{BASE_URL_LOCALIDADES}/municipios/{codigo_municipio}"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        municipio_data = response.json()

        resultado = {
            "id": municipio_data["id"],
            "nome": municipio_data["nome"],
            "uf": municipio_data["microrregiao"]["mesorregiao"]["UF"]["nome"],
            "sigla_uf": municipio_data["microrregiao"]["mesorregiao"]["UF"]["sigla"],
            "regiao": municipio_data["microrregiao"]["mesorregiao"]["UF"]["regiao"]["nome"]
        }

        cache["municipios"][codigo_municipio] = resultado
        salvar_cache(cache)
        
        return resultado
    except Exception as e:
        return {"erro": str(e)}

def listar_estados() -> list:
    """Lista todos os estados do Brasil"""
    try:
        cache = carregar_cache()
        if "estados" in cache:
            return cache["estados"]

        url = f"{BASE_URL_LOCALIDADES}/estados"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        estados = response.json()

        # Formata os dados
        estados_formatados = [{
            "id": e["id"],
            "nome": e["nome"],
            "sigla": e["sigla"],
            "regiao": e["regiao"]["nome"]
        } for e in estados]

        cache["estados"] = estados_formatados
        salvar_cache(cache)
        
        return estados_formatados
    except Exception as e:
        return {"erro": str(e)}

def buscar_municipio_por_nome(nome_municipio: str) -> dict:
    """Busca informações de um município por nome"""
    try:
        url = f"{BASE_URL_LOCALIDADES}/municipios"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        municipios = response.json()

        municipio = next(
            (m for m in municipios if m["nome"].lower() == nome_municipio.lower()),
            None
        )

        if not municipio:
            return {"erro": f"Município '{nome_municipio}' não encontrado."}

        return buscar_municipio_por_codigo(str(municipio["id"]))
    except Exception as e:
        return {"erro": str(e)}

def listar_regioes() -> list:
    """Lista todas as regiões do Brasil"""
    try:
        cache = carregar_cache()
        if "regioes" in cache:
            return cache["regioes"]

        url = f"{BASE_URL_LOCALIDADES}/regioes"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        regioes = response.json()

        # Formata os dados
        regioes_formatadas = [{
            "id": r["id"],
            "nome": r["nome"],
            "sigla": r["sigla"]
        } for r in regioes]

        cache["regioes"] = regioes_formatadas
        salvar_cache(cache)
        
        return regioes_formatadas
    except Exception as e:
        return {"erro": str(e)}

def buscar_area_territorial(codigo_municipio: str) -> dict:
    """Busca a área territorial de um município"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "areas" in cache and codigo_municipio in cache["areas"]:
            return cache["areas"][codigo_municipio]

        # Primeiro busca as informações básicas do município para confirmar existência
        url_municipio = f"{BASE_URL_LOCALIDADES}/municipios/{codigo_municipio}"
        response_municipio = httpx.get(url_municipio, timeout=DEFAULT_TIMEOUT)
        response_municipio.raise_for_status()
        municipio_data = response_municipio.json()

        # Agora busca a área territorial usando a API de dados censitários
        url_area = f"{BASE_URL_CENSOS}/area/{codigo_municipio}"
        response_area = httpx.get(url_area, timeout=DEFAULT_TIMEOUT)
        response_area.raise_for_status()
        area_data = response_area.json()

        # A API retorna uma lista, precisamos pegar o primeiro item
        area = area_data[0]["area_km2"] if area_data else None

        resultado = {
            "municipio": codigo_municipio,
            "nome": municipio_data["nome"],
            "area_km2": area,
            "fonte": "IBGE - Censo 2010"
        }

        # Salva no cache
        if "areas" not in cache:
            cache["areas"] = {}
        cache["areas"][codigo_municipio] = resultado
        salvar_cache(cache)

        return resultado
    except Exception as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "areas" in cache and codigo_municipio in cache["areas"]:
            return cache["areas"][codigo_municipio]
        return {"erro": str(e)}

def buscar_densidade_demografica(codigo_municipio: str) -> dict:
    """Calcula a densidade demográfica de um município"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "densidades" in cache and codigo_municipio in cache["densidades"]:
            return cache["densidades"][codigo_municipio]

        # Busca a população
        populacao = buscar_populacao_por_codigo(codigo_municipio)
        if "erro" in populacao:
            return populacao

        # Busca a área
        area = buscar_area_territorial(codigo_municipio)
        if "erro" in area:
            return area

        # Calcula a densidade
        densidade = populacao["populacao"] / area["area_km2"]

        resultado = {
            "municipio": codigo_municipio,
            "densidade": densidade,
            "populacao": populacao["populacao"],
            "area_km2": area["area_km2"],
            "data_referencia": populacao["data_referencia"],
            "fonte": "IBGE"
        }

        # Salva no cache
        if "densidades" not in cache:
            cache["densidades"] = {}
        cache["densidades"][codigo_municipio] = resultado
        salvar_cache(cache)

        return resultado
    except Exception as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "densidades" in cache and codigo_municipio in cache["densidades"]:
            return cache["densidades"][codigo_municipio]
        return {"erro": str(e)}

async def buscar_metadados(pesquisa: str, ano: str) -> dict:
    """Busca metadados de uma pesquisa específica para um ano"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "metadados" in cache and f"{pesquisa}_{ano}" in cache["metadados"]:
            return cache["metadados"][f"{pesquisa}_{ano}"]

        # Aguarda um pequeno delay para evitar sobrecarregar o servidor
        await asyncio.sleep(1)

        url = f"https://servicodados.ibge.gov.br/api/v3/metadata/{pesquisa}/{ano}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            resultado = response.json()

            # Salva no cache
            if "metadados" not in cache:
                cache["metadados"] = {}
            cache["metadados"][f"{pesquisa}_{ano}"] = resultado
            salvar_cache(cache)

            return resultado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "metadados" in cache and f"{pesquisa}_{ano}" in cache["metadados"]:
            return cache["metadados"][f"{pesquisa}_{ano}"]
        return {"erro": f"Erro na requisição: {str(e)}"}
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "metadados" in cache and f"{pesquisa}_{ano}" in cache["metadados"]:
            return cache["metadados"][f"{pesquisa}_{ano}"]
        return {"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"erro": str(e)}

def listar_variaveis() -> list:
    """Lista todas as variáveis disponíveis"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "variaveis" in cache:
            return cache["variaveis"]

        # Aguarda um pequeno delay para evitar sobrecarregar o servidor
        time.sleep(1)

        url = "https://servicodados.ibge.gov.br/api/v3/metadata/variables"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        resultado = response.json()

        # Salva no cache
        cache["variaveis"] = resultado
        salvar_cache(cache)

        return resultado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "variaveis" in cache:
            return cache["variaveis"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "variaveis" in cache:
            return cache["variaveis"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        return [{"erro": str(e)}]

def listar_unidades_medida() -> list:
    """Lista todas as unidades de medida disponíveis"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "unidades" in cache:
            return cache["unidades"]

        # Aguarda um pequeno delay para evitar sobrecarregar o servidor
        time.sleep(1)

        url = "https://servicodados.ibge.gov.br/api/v3/metadata/units"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        resultado = response.json()

        # Salva no cache
        cache["unidades"] = resultado
        salvar_cache(cache)

        return resultado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "unidades" in cache:
            return cache["unidades"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "unidades" in cache:
            return cache["unidades"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        return [{"erro": str(e)}]

def listar_conceitos() -> list:
    """Lista todos os conceitos disponíveis"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "conceitos" in cache:
            return cache["conceitos"]

        # Aguarda um pequeno delay para evitar sobrecarregar o servidor
        time.sleep(1)

        url = "https://servicodados.ibge.gov.br/api/v3/metadata/concepts"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        resultado = response.json()

        # Salva no cache
        cache["conceitos"] = resultado
        salvar_cache(cache)

        return resultado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "conceitos" in cache:
            return cache["conceitos"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "conceitos" in cache:
            return cache["conceitos"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        return [{"erro": str(e)}]

def listar_fontes() -> list:
    """Lista todas as fontes de dados disponíveis"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "fontes" in cache:
            return cache["fontes"]

        url = f"{BASE_URL_METADADOS}/fontes"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        fontes = response.json()

        # Salva no cache
        cache["fontes"] = fontes
        salvar_cache(cache)

        return fontes
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "fontes" in cache:
            return cache["fontes"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "fontes" in cache:
            return cache["fontes"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        return [{"erro": str(e)}]


def listar_pesquisas() -> list:
    """Obtém as pesquisas com metadados associados"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "pesquisas" in cache and datetime.now().timestamp() - cache.get("pesquisas_timestamp", 0) < 86400:
            return cache["pesquisas"]

        url = f"{BASE_URL_METADADOS}/pesquisas"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        pesquisas = response.json()

        # Salva no cache com timestamp
        cache["pesquisas"] = pesquisas
        cache["pesquisas_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return pesquisas
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "pesquisas" in cache:
            return cache["pesquisas"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "pesquisas" in cache:
            return cache["pesquisas"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar pesquisas: {e}")
        return [{"erro": str(e)}]


def listar_periodos_pesquisa(pesquisa: str) -> list:
    """Obtém os períodos pesquisados com metadados associados para uma pesquisa específica"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"periodos_pesquisa_{pesquisa}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        periodos = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = periodos
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return periodos
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"periodos_pesquisa_{pesquisa}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"periodos_pesquisa_{pesquisa}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar períodos da pesquisa {pesquisa}: {e}")
        return [{"erro": str(e)}]


def obter_metadados_pesquisa_periodo(pesquisa: str, periodo: str) -> dict:
    """Obtém os metadados de uma pesquisa para um período específico"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"metadados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        metadados = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = metadados
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return metadados
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"metadados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro na requisição: {str(e)}"}
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"metadados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"Erro ao obter metadados da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}


def listar_agregados_pesquisa_periodo(pesquisa: str, periodo: str) -> list:
    """Obtém os agregados de uma pesquisa para um período específico"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"agregados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        agregados = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = agregados
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return agregados
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"agregados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"agregados_pesquisa_{pesquisa}_periodo_{periodo}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar agregados da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]


def obter_agregado(pesquisa: str, periodo: str, agregado: str) -> dict:
    """Obtém informações detalhadas de um agregado específico"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        info_agregado = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = info_agregado
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return info_agregado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro na requisição: {str(e)}"}
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"Erro ao obter agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}


def listar_variaveis_agregado(pesquisa: str, periodo: str, agregado: str) -> list:
    """Lista as variáveis de um agregado específico"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"variaveis_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        variaveis = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = variaveis
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return variaveis
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"variaveis_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"variaveis_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar variáveis do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]


def obter_variavel(pesquisa: str, periodo: str, agregado: str, variavel: str) -> dict:
    """Obtém informações detalhadas de uma variável específica"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"variavel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_variavel_{variavel}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis/{variavel}"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        info_variavel = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = info_variavel
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return info_variavel
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"variavel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_variavel_{variavel}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro na requisição: {str(e)}"}
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"variavel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_variavel_{variavel}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"Erro ao obter variável {variavel} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}


def listar_classificacoes_agregado(pesquisa: str, periodo: str, agregado: str) -> list:
    """Lista as classificações de um agregado específico"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"classificacoes_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        classificacoes = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = classificacoes
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return classificacoes
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"classificacoes_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"classificacoes_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar classificações do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]


def listar_niveis_classificacao(pesquisa: str, periodo: str, agregado: str, classificacao: str) -> list:
    """Lista os níveis de uma classificação específica"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"niveis_classificacao_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        niveis = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = niveis
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return niveis
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"niveis_classificacao_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"niveis_classificacao_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar níveis da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]


def listar_categorias_nivel(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str) -> list:
    """Lista as categorias de um nível específico de classificação"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"categorias_nivel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        categorias = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = categorias
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return categorias
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"categorias_nivel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"categorias_nivel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}"
        if cache_key in cache:
            return cache[cache_key]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        logger.error(f"Erro ao listar categorias do nível {nivel} da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]


def obter_categoria(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str, categoria: str) -> dict:
    """Obtém informações detalhadas de uma categoria específica"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        cache_key = f"categoria_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}_categoria_{categoria}"
        if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < 86400:
            return cache[cache_key]

        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias/{categoria}"
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        info_categoria = response.json()

        # Salva no cache com timestamp
        cache[cache_key] = info_categoria
        cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
        salvar_cache(cache)

        return info_categoria
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"categoria_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}_categoria_{categoria}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro na requisição: {str(e)}"}
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        cache_key = f"categoria_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}_categoria_{categoria}"
        if cache_key in cache:
            return cache[cache_key]
        return {"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"Erro ao obter categoria {categoria} do nível {nivel} da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}

def listar_dominios() -> list:
    """Lista todos os domínios disponíveis"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if "dominios" in cache:
            return cache["dominios"]

        # Aguarda um pequeno delay para evitar sobrecarregar o servidor
        time.sleep(1)

        url = "https://servicodados.ibge.gov.br/api/v3/metadata/domains"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        resultado = response.json()

        # Salva no cache
        cache["dominios"] = resultado
        salvar_cache(cache)

        return resultado
    except httpx.RequestError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "dominios" in cache:
            return cache["dominios"]
        return [{"erro": f"Erro na requisição: {str(e)}"}]
    except httpx.HTTPStatusError as e:
        # Se houver erro, tenta usar o cache
        cache = carregar_cache()
        if "dominios" in cache:
            return cache["dominios"]
        return [{"erro": f"Erro HTTP {e.response.status_code}: {e.response.text}"}]
    except Exception as e:
        return [{"erro": str(e)}]

def buscar_populacao_por_codigo(codigo_municipio: str) -> dict:
    """Busca população usando código do município"""
    try:
        # Primeiro verifica no cache
        cache = carregar_cache()
        if codigo_municipio in cache["municipios"]:
            return cache["municipios"][codigo_municipio]

        print(f"Buscando dados para o código {codigo_municipio}")
        
        # Primeiro busca as informações básicas do município
        url_municipio = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo_municipio}"
        print(f"URL do município: {url_municipio}")
        response_municipio = httpx.get(url_municipio, timeout=10.0)
        response_municipio.raise_for_status()
        municipio_data = response_municipio.json()
        print(f"Dados do município: {municipio_data}")

        # Agora busca a população mais recente usando a API de estimativas
        url_populacao = f"https://servicodados.ibge.gov.br/api/v2/censos/estimativas/{codigo_municipio[:2]}/municipios/{codigo_municipio}"
        print(f"URL da população: {url_populacao}")
        response_populacao = httpx.get(url_populacao, timeout=10.0)
        response_populacao.raise_for_status()
        populacao_data = response_populacao.json()
        print(f"Dados de população: {populacao_data}")

        if not populacao_data:
            return {"erro": "Dados de população não encontrados"}

        # Pegando a última estimativa disponível
        ultima_estimativa = populacao_data[-1]
        
        resultado = {
            "municipio": municipio_data["nome"],
            "uf": municipio_data["microrregiao"]["mesorregiao"]["UF"]["nome"],
            "populacao": ultima_estimativa["estimativa"],
            "data_referencia": f"{ultima_estimativa['ano']}",
            "fonte": "IBGE - Estimativas populacionais"
        }

        # Salva no cache
        cache["municipios"][codigo_municipio] = resultado
        salvar_cache(cache)
        
        return resultado
    except httpx.HTTPStatusError as exc:
        print(f"Erro HTTP: {exc.response.status_code}")
        print(f"Resposta: {exc.response.text}")
        return {"erro": f"Erro HTTP: {exc.response.status_code} - {exc.response.text}"}
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return {"erro": str(e)}

def buscar_populacao_por_nome(nome_municipio: str) -> dict:
    """Busca população usando nome do município"""
    try:
        # Primeiro busca o código do município
        url_municipios = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        r = httpx.get(url_municipios)
        r.raise_for_status()
        municipios = r.json()

        municipio = next(
            (m for m in municipios if m["nome"].lower() == nome_municipio.lower()),
            None
        )

        if not municipio:
            return {"erro": f"Município '{nome_municipio}' não encontrado."}

        # Agora busca a população usando o código
        return buscar_populacao_por_codigo(str(municipio["id"]))
    except Exception as e:
        return {"erro": str(e)}