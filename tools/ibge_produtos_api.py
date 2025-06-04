"""
Módulo utilitário para acesso à API de Produtos do IBGE
Funções de baixo nível, com cache, logging e tratamento de erros.
"""

from .ibge_base import *
from typing import List, Dict

def listar_produtos() -> List[Dict]:
    cache_key = "produtos_lista"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos"
        produtos = make_request(url)
        return save_to_cache(cache_key, produtos)
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {e}")
        return []

def obter_produto(id_produto: str) -> Dict:
    cache_key = f"produtos_produto_{id_produto}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/{id_produto}"
        produto = make_request(url)
        return save_to_cache(cache_key, produto)
    except Exception as e:
        logger.error(f"Erro ao obter produto com ID {id_produto}: {e}")
        return {"erro": str(e)}

def listar_produtos_por_tipo(id_tipo: str) -> List[Dict]:
    cache_key = f"produtos_tipo_{id_tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/tipos/{id_tipo}"
        produtos = make_request(url)
        return save_to_cache(cache_key, produtos)
    except Exception as e:
        logger.error(f"Erro ao listar produtos por tipo {id_tipo}: {e}")
        return []

def listar_produtos_por_tema(id_tema: str) -> List[Dict]:
    cache_key = f"produtos_tema_{id_tema}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/temas/{id_tema}"
        produtos = make_request(url)
        return save_to_cache(cache_key, produtos)
    except Exception as e:
        logger.error(f"Erro ao listar produtos por tema {id_tema}: {e}")
        return []

def listar_tipos_produtos() -> List[Dict]:
    cache_key = "produtos_tipos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de produtos: {e}")
        return []

def obter_tipo_produto(id_tipo: str) -> Dict:
    cache_key = f"produtos_tipo_{id_tipo}_detalhe"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/tipos/{id_tipo}"
        tipo = make_request(url)
        return save_to_cache(cache_key, tipo)
    except Exception as e:
        logger.error(f"Erro ao obter tipo de produto com ID {id_tipo}: {e}")
        return {"erro": str(e)}

def listar_temas_produtos() -> List[Dict]:
    cache_key = "produtos_temas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/temas"
        temas = make_request(url)
        return save_to_cache(cache_key, temas)
    except Exception as e:
        logger.error(f"Erro ao listar temas de produtos: {e}")
        return []

def obter_tema_produto(id_tema: str) -> Dict:
    cache_key = f"produtos_tema_{id_tema}_detalhe"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/temas/{id_tema}"
        tema = make_request(url)
        return save_to_cache(cache_key, tema)
    except Exception as e:
        logger.error(f"Erro ao obter tema de produto com ID {id_tema}: {e}")
        return {"erro": str(e)}
