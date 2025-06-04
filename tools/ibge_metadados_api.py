"""
Funções utilitárias para acesso à API de Metadados Estatísticos do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/metadados-estatisticos
"""

from typing import List, Dict
from .ibge_base import get_cached_data, save_to_cache, logger, BASE_URL_METADADOS, make_request

def listar_fontes() -> List[Dict]:
    cache_key = "fontes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/fontes"
        fontes = make_request(url)
        return save_to_cache(cache_key, fontes)
    except Exception as e:
        logger.error(f"Erro ao listar fontes: {e}")
        return [{"erro": str(e)}]

def listar_pesquisas() -> List[Dict]:
    cache_key = "pesquisas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas"
        pesquisas = make_request(url)
        return save_to_cache(cache_key, pesquisas)
    except Exception as e:
        logger.error(f"Erro ao listar pesquisas: {e}")
        return [{"erro": str(e)}]

def listar_periodos_pesquisa(pesquisa: str) -> List[Dict]:
    cache_key = f"periodos_pesquisa_{pesquisa}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos"
        periodos = make_request(url)
        return save_to_cache(cache_key, periodos)
    except Exception as e:
        logger.error(f"Erro ao listar períodos da pesquisa {pesquisa}: {e}")
        return [{"erro": str(e)}]

def obter_metadados_pesquisa_periodo(pesquisa: str, periodo: str) -> Dict:
    cache_key = f"metadados_{pesquisa}_{periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/metadados"
        metadados = make_request(url)
        return save_to_cache(cache_key, metadados)
    except Exception as e:
        logger.error(f"Erro ao obter metadados da pesquisa {pesquisa} para o período {periodo}: {e}")
        return {"erro": str(e)}

def listar_agregados_pesquisa_periodo(pesquisa: str, periodo: str) -> List[Dict]:
    cache_key = f"agregados_{pesquisa}_{periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados"
        agregados = make_request(url)
        return save_to_cache(cache_key, agregados)
    except Exception as e:
        logger.error(f"Erro ao listar agregados da pesquisa {pesquisa} para o período {periodo}: {e}")
        return [{"erro": str(e)}]

def obter_agregado(pesquisa: str, periodo: str, agregado: str) -> Dict:
    cache_key = f"agregado_{pesquisa}_{periodo}_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}"
        dados = make_request(url)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao obter agregado {agregado} da pesquisa {pesquisa} para o período {periodo}: {e}")
        return {"erro": str(e)}

def listar_variaveis_agregado(pesquisa: str, periodo: str, agregado: str) -> List[Dict]:
    cache_key = f"variaveis_{pesquisa}_{periodo}_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis"
        variaveis = make_request(url)
        return save_to_cache(cache_key, variaveis)
    except Exception as e:
        logger.error(f"Erro ao listar variáveis do agregado {agregado}: {e}")
        return [{"erro": str(e)}]

def obter_variavel(pesquisa: str, periodo: str, agregado: str, variavel: str) -> Dict:
    cache_key = f"variavel_{pesquisa}_{periodo}_{agregado}_{variavel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis/{variavel}"
        dados = make_request(url)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao obter variável {variavel} do agregado {agregado}: {e}")
        return {"erro": str(e)}

def listar_classificacoes_agregado(pesquisa: str, periodo: str, agregado: str) -> List[Dict]:
    cache_key = f"classificacoes_{pesquisa}_{periodo}_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes"
        classificacoes = make_request(url)
        return save_to_cache(cache_key, classificacoes)
    except Exception as e:
        logger.error(f"Erro ao listar classificações do agregado {agregado}: {e}")
        return [{"erro": str(e)}]

def listar_niveis_classificacao(pesquisa: str, periodo: str, agregado: str, classificacao: str) -> List[Dict]:
    cache_key = f"niveis_{pesquisa}_{periodo}_{agregado}_{classificacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis"
        niveis = make_request(url)
        return save_to_cache(cache_key, niveis)
    except Exception as e:
        logger.error(f"Erro ao listar níveis da classificação {classificacao}: {e}")
        return [{"erro": str(e)}]

def listar_categorias_nivel(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str) -> List[Dict]:
    cache_key = f"categorias_{pesquisa}_{periodo}_{agregado}_{classificacao}_{nivel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias"
        categorias = make_request(url)
        return save_to_cache(cache_key, categorias)
    except Exception as e:
        logger.error(f"Erro ao listar categorias do nível {nivel}: {e}")
        return [{"erro": str(e)}]

def obter_categoria(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str, categoria: str) -> Dict:
    cache_key = f"categoria_{pesquisa}_{periodo}_{agregado}_{classificacao}_{nivel}_{categoria}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias/{categoria}"
        dados = make_request(url)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao obter categoria {categoria}: {e}")
        return {"erro": str(e)}

def listar_dominios() -> List[Dict]:
    cache_key = "dominios"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/dominios"
        dominios = make_request(url)
        return save_to_cache(cache_key, dominios)
    except Exception as e:
        logger.error(f"Erro ao listar domínios: {e}")
        return [{"erro": str(e)}]

def listar_variaveis() -> List[Dict]:
    cache_key = "variaveis"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/variaveis"
        variaveis = make_request(url)
        return save_to_cache(cache_key, variaveis)
    except Exception as e:
        logger.error(f"Erro ao listar variáveis: {e}")
        return [{"erro": str(e)}]

def listar_unidades_medida() -> List[Dict]:
    cache_key = "unidades_medida"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/unidades-medida"
        unidades = make_request(url)
        return save_to_cache(cache_key, unidades)
    except Exception as e:
        logger.error(f"Erro ao listar unidades de medida: {e}")
        return [{"erro": str(e)}]

def listar_conceitos() -> List[Dict]:
    cache_key = "conceitos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_METADADOS}/conceitos"
        conceitos = make_request(url)
        return save_to_cache(cache_key, conceitos)
    except Exception as e:
        logger.error(f"Erro ao listar conceitos: {e}")
        return [{"erro": str(e)}]
