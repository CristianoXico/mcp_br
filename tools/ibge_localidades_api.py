"""
Funções utilitárias para acesso à API de Localidades do IBGE (requisições HTTP, cache, autenticação, logging).
Documentação: https://servicodados.ibge.gov.br/api/docs/localidades
"""

from typing import List, Dict
from .ibge_base import make_request, get_cached_data, save_to_cache, logger, BASE_URL_LOCALIDADES


def listar_regioes() -> List[Dict]:
    cache_key = "regioes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_LOCALIDADES}/regioes"
        regioes = make_request(url)
        return save_to_cache(cache_key, regioes)
    except Exception as e:
        logger.error(f"Erro ao listar regiões: {e}")
        return [{"erro": str(e)}]


def listar_estados(regiao: str = None) -> List[Dict]:
    cache_key = f"estados{f'_regiao_{regiao}' if regiao else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        if regiao:
            url = f"{BASE_URL_LOCALIDADES}/regioes/{regiao}/estados"
        else:
            url = f"{BASE_URL_LOCALIDADES}/estados"
        estados = make_request(url)
        return save_to_cache(cache_key, estados)
    except Exception as e:
        logger.error(f"Erro ao listar estados: {e}")
        return [{"erro": str(e)}]


def listar_mesorregioes(uf: str = None) -> List[Dict]:
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
    cache_key = f"municipio_codigo_{codigo_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_LOCALIDADES}/municipios/{codigo_municipio}"
        municipio = make_request(url)
        return save_to_cache(cache_key, municipio)
    except Exception as e:
        logger.error(f"Erro ao buscar município por código: {e}")
        return {"erro": str(e)}


def buscar_municipio_por_nome(nome_municipio: str) -> List[Dict]:
    cache_key = f"municipio_nome_{nome_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_LOCALIDADES}/municipios"
        params = {"nome": nome_municipio}
        municipios = make_request(url, params)
        return save_to_cache(cache_key, municipios)
    except Exception as e:
        logger.error(f"Erro ao buscar município por nome: {e}")
        return [{"erro": str(e)}]


def listar_distritos(municipio: str = None, uf: str = None) -> List[Dict]:
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
    cache_key = f"area_territorial_{codigo_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_LOCALIDADES}/municipios/{codigo_municipio}/area"
        area = make_request(url)
        return save_to_cache(cache_key, area)
    except Exception as e:
        logger.error(f"Erro ao buscar área territorial: {e}")
        return {"erro": str(e)}
