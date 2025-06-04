"""
Façade do domínio Localidades do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Localidades.

- Funções utilitárias de acesso à API: ibge_localidades_api.py
- Handlers MCP: ibge_localidades_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_localidades_handlers.py.
"""

from typing import List, Dict
from .ibge_localidades_handlers import *

# O bloco abaixo estava fora de função/classe e causava erro de indentação.
# Se for uma função utilitária, deve estar dentro de uma função. Caso contrário, manter comentado.

# """
# cache_key = f"estados{f'_regiao_{regiao}' if regiao else ''}"
# cached_data = get_cached_data(cache_key)
# if cached_data:
#     return cached_data
# try:
#     if regiao:
#         url = f"{BASE_URL_LOCALIDADES}/regioes/{regiao}/estados"
#     else:
#         url = f"{BASE_URL_LOCALIDADES}/estados"
#     estados = make_request(url)
#     return save_to_cache(cache_key, estados)
# except Exception as e:
#     logger.error(f"Erro ao listar estados: {e}")
#     return [{"erro": str(e)}]

def listar_mesorregioes(uf: str = None) -> List[Dict]:
    """
    Lista todas as mesorregiões
    
    Args:
        uf: ID opcional do estado para filtrar mesorregiões
    """
    cache_key = f"mesorregioes{f'_uf_{uf}' if uf else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if uf:
            url = f"{BASE_URL_LOCALIDADES}/estados/{uf}/mesorregioes"
        else:
            url = f"{BASE_URL_LOCALIDADES}/mesorregioes"
        mesorregioes = make_request(url)
        return save_to_cache(cache_key, mesorregioes)
    except Exception as e:
        logger.error(f"Erro ao listar mesorregiões: {e}")
        return [{"erro": str(e)}]

def listar_microrregioes(mesorregiao: str = None, uf: str = None) -> List[Dict]:
    """
    Lista todas as microrregiões
    
    Args:
        mesorregiao: ID opcional da mesorregião para filtrar microrregiões
        uf: ID opcional do estado para filtrar microrregiões
    """
    cache_key = f"microrregioes{f'_mesorregiao_{mesorregiao}' if mesorregiao else ''}{f'_uf_{uf}' if uf else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if mesorregiao:
            url = f"{BASE_URL_LOCALIDADES}/mesorregioes/{mesorregiao}/microrregioes"
        elif uf:
            url = f"{BASE_URL_LOCALIDADES}/estados/{uf}/microrregioes"
        else:
            url = f"{BASE_URL_LOCALIDADES}/microrregioes"
        microrregioes = make_request(url)
        return save_to_cache(cache_key, microrregioes)
    except Exception as e:
        logger.error(f"Erro ao listar microrregiões: {e}")
        return [{"erro": str(e)}]

def listar_municipios(microrregiao: str = None, mesorregiao: str = None, uf: str = None) -> List[Dict]:
    """
    Lista todos os municípios
    
    Args:
        microrregiao: ID opcional da microrregião para filtrar municípios
        mesorregiao: ID opcional da mesorregião para filtrar municípios
        uf: ID opcional do estado para filtrar municípios
    """
    cache_key = f"municipios{f'_microrregiao_{microrregiao}' if microrregiao else ''}{f'_mesorregiao_{mesorregiao}' if mesorregiao else ''}{f'_uf_{uf}' if uf else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if microrregiao:
            url = f"{BASE_URL_LOCALIDADES}/microrregioes/{microrregiao}/municipios"
        elif mesorregiao:
            url = f"{BASE_URL_LOCALIDADES}/mesorregioes/{mesorregiao}/municipios"
        elif uf:
            url = f"{BASE_URL_LOCALIDADES}/estados/{uf}/municipios"
        else:
            url = f"{BASE_URL_LOCALIDADES}/municipios"
        municipios = make_request(url)
        return save_to_cache(cache_key, municipios)
    except Exception as e:
        logger.error(f"Erro ao listar municípios: {e}")
        return [{"erro": str(e)}]

def buscar_municipio_por_codigo(codigo_municipio: str) -> Dict:
    """
    Busca informações detalhadas de um município por código
    
    Args:
        codigo_municipio: Código do município no IBGE
    """
    cache_key = f"municipio_{codigo_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_LOCALIDADES}/municipios/{codigo_municipio}"
        municipio = make_request(url)
        return save_to_cache(cache_key, municipio)
    except Exception as e:
        logger.error(f"Erro ao buscar município por código {codigo_municipio}: {e}")
        return {"erro": str(e)}

def buscar_municipio_por_nome(nome_municipio: str) -> Dict:
    """
    Busca informações de um município pelo nome
    
    Args:
        nome_municipio: Nome do município
    """
    try:
        # Primeiro lista todos os municípios
        municipios = listar_municipios()
        if isinstance(municipios, list) and "erro" in municipios[0]:
            return {"erro": municipios[0]["erro"]}
        
        # Procura pelo nome (ignorando case e acentos)
        import unicodedata
        
        def normalize(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                          if unicodedata.category(c) != 'Mn')
        
        nome_normalizado = normalize(nome_municipio)
        
        for municipio in municipios:
            if normalize(municipio["nome"]) == nome_normalizado:
                return buscar_municipio_por_codigo(str(municipio["id"]))
        
        return {"erro": f"Município '{nome_municipio}' não encontrado"}
    except Exception as e:
        logger.error(f"Erro ao buscar município por nome {nome_municipio}: {e}")
        return {"erro": str(e)}

def listar_distritos(municipio: str = None, uf: str = None) -> List[Dict]:
    """
    Lista todos os distritos
    
    Args:
        municipio: ID opcional do município para filtrar distritos
        uf: ID opcional do estado para filtrar distritos
    """
    cache_key = f"distritos{f'_municipio_{municipio}' if municipio else ''}{f'_uf_{uf}' if uf else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if municipio:
            url = f"{BASE_URL_LOCALIDADES}/municipios/{municipio}/distritos"
        elif uf:
            url = f"{BASE_URL_LOCALIDADES}/estados/{uf}/distritos"
        else:
            url = f"{BASE_URL_LOCALIDADES}/distritos"
        distritos = make_request(url)
        return save_to_cache(cache_key, distritos)
    except Exception as e:
        logger.error(f"Erro ao listar distritos: {e}")
        return [{"erro": str(e)}]

def listar_subdistritos(distrito: str = None, municipio: str = None, uf: str = None) -> List[Dict]:
    """
    Lista todos os subdistritos
    
    Args:
        distrito: ID opcional do distrito para filtrar subdistritos
        municipio: ID opcional do município para filtrar subdistritos
        uf: ID opcional do estado para filtrar subdistritos
    """
    cache_key = f"subdistritos{f'_distrito_{distrito}' if distrito else ''}{f'_municipio_{municipio}' if municipio else ''}{f'_uf_{uf}' if uf else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if distrito:
            url = f"{BASE_URL_LOCALIDADES}/distritos/{distrito}/subdistritos"
        elif municipio:
            url = f"{BASE_URL_LOCALIDADES}/municipios/{municipio}/subdistritos"
        elif uf:
            url = f"{BASE_URL_LOCALIDADES}/estados/{uf}/subdistritos"
        else:
            url = f"{BASE_URL_LOCALIDADES}/subdistritos"
        subdistritos = make_request(url)
        return save_to_cache(cache_key, subdistritos)
    except Exception as e:
        logger.error(f"Erro ao listar subdistritos: {e}")
        return [{"erro": str(e)}]

def buscar_area_territorial(codigo_municipio: str) -> Dict:
    """
    Busca a área territorial de um município
    
    Args:
        codigo_municipio: Código do município no IBGE
    """
    cache_key = f"area_territorial_{codigo_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        # Primeiro busca as informações básicas do município para confirmar existência
        municipio = buscar_municipio_por_codigo(codigo_municipio)
        if "erro" in municipio:
            return municipio

        # Agora busca a área territorial usando a API de dados censitários
        url = f"{BASE_URL_CENSOS}/area/{codigo_municipio}"
        area_data = make_request(url)
        
        return save_to_cache(cache_key, area_data)
    except Exception as e:
        logger.error(f"Erro ao buscar área territorial do município {codigo_municipio}: {e}")
        return {"erro": str(e)}
