"""
Módulo utilitário para acesso à API de Países do IBGE
Funções de baixo nível, com cache, logging e tratamento de erros.
"""

from .ibge_base import *
from typing import List, Dict

def listar_paises() -> List[Dict]:
    cache_key = "paises_lista"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/paises"
        paises = make_request(url)
        return save_to_cache(cache_key, paises)
    except Exception as e:
        logger.error(f"Erro ao listar países: {e}")
        return []

def obter_pais(id_pais: str) -> Dict:
    cache_key = f"paises_pais_{id_pais}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/paises/{id_pais}"
        pais = make_request(url)
        return save_to_cache(cache_key, pais)
    except Exception as e:
        logger.error(f"Erro ao obter país com ID {id_pais}: {e}")
        return {"erro": str(e)}

def listar_paises_por_continente(id_continente: str) -> List[Dict]:
    cache_key = f"paises_continente_{id_continente}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/paises/continentes/{id_continente}"
        paises = make_request(url)
        return save_to_cache(cache_key, paises)
    except Exception as e:
        logger.error(f"Erro ao listar países do continente {id_continente}: {e}")
        return []

def listar_paises_por_bloco(id_bloco: str) -> List[Dict]:
    cache_key = f"paises_bloco_{id_bloco}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/paises/blocos/{id_bloco}"
        paises = make_request(url)
        return save_to_cache(cache_key, paises)
    except Exception as e:
        logger.error(f"Erro ao listar países do bloco {id_bloco}: {e}")
        return []

def listar_continentes() -> List[Dict]:
    cache_key = "paises_continentes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/continentes"
        continentes = make_request(url)
        return save_to_cache(cache_key, continentes)
    except Exception as e:
        logger.error(f"Erro ao listar continentes: {e}")
        return []

def obter_continente(id_continente: str) -> Dict:
    cache_key = f"paises_continente_{id_continente}_detalhe"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/continentes/{id_continente}"
        continente = make_request(url)
        return save_to_cache(cache_key, continente)
    except Exception as e:
        logger.error(f"Erro ao obter continente {id_continente}: {e}")
        return {"erro": str(e)}

def listar_blocos() -> List[Dict]:
    cache_key = "paises_blocos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/blocos"
        blocos = make_request(url)
        return save_to_cache(cache_key, blocos)
    except Exception as e:
        logger.error(f"Erro ao listar blocos econômicos: {e}")
        return []

def obter_bloco(id_bloco: str) -> Dict:
    cache_key = f"paises_bloco_{id_bloco}_detalhe"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PAISES}/blocos/{id_bloco}"
        bloco = make_request(url)
        return save_to_cache(cache_key, bloco)
    except Exception as e:
        logger.error(f"Erro ao obter bloco econômico {id_bloco}: {e}")
        return {"erro": str(e)}
