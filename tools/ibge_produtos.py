"""
Módulo para acesso à API de Produtos do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/produtos?versao=1
"""

from .ibge_base import *

"""
Façade do domínio IBGE-Produtos.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Produtos.

- Funções utilitárias de acesso à API: ibge_produtos_api.py
- Handlers MCP: ibge_produtos_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_produtos_handlers.py.
"""

from .ibge_produtos_handlers import *

def listar_produtos_por_tipo(id_tipo: str) -> List[Dict]:
    """
    Lista produtos por tipo
    
    Args:
        id_tipo: ID do tipo de produto
    """
    cache_key = f"produtos_tipo_{id_tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/tipos/{id_tipo}"
        produtos = make_request(url)
        return save_to_cache(cache_key, produtos)
    except Exception as e:
        logger.error(f"Erro ao listar produtos do tipo {id_tipo}: {e}")
        return []

def listar_produtos_por_tema(id_tema: str) -> List[Dict]:
    """
    Lista produtos por tema
    
    Args:
        id_tema: ID do tema
    """
    cache_key = f"produtos_tema_{id_tema}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PRODUTOS}/produtos/temas/{id_tema}"
        produtos = make_request(url)
        return save_to_cache(cache_key, produtos)
    except Exception as e:
        logger.error(f"Erro ao listar produtos do tema {id_tema}: {e}")
        return []

def listar_tipos_produtos() -> List[Dict]:
    """
    Lista todos os tipos de produtos do IBGE
    """
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
    """
    Obtém informações detalhadas de um tipo de produto pelo seu ID
    
    Args:
        id_tipo: ID do tipo de produto
    """
    cache_key = f"produtos_tipo_detalhe_{id_tipo}"
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
    """
    Lista todos os temas de produtos do IBGE
    """
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
    """
    Obtém informações detalhadas de um tema de produto pelo seu ID
    
    Args:
        id_tema: ID do tema de produto
    """
    cache_key = f"produtos_tema_detalhe_{id_tema}"
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
