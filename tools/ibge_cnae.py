"""
Façade do domínio CNAE (Classificação Nacional de Atividades Econômicas) do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio CNAE.

- Funções utilitárias de acesso à API: ibge_cnae_api.py
- Handlers MCP: ibge_cnae_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_cnae_handlers.py.
"""

from typing import List, Dict
from .ibge_cnae_handlers import *

"""
Façade do domínio CNAE (Classificação Nacional de Atividades Econômicas) do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio CNAE.

- Funções utilitárias de acesso à API: ibge_cnae_api.py
- Handlers MCP: ibge_cnae_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_cnae_handlers.py.
"""


def listar_classes(id_grupo: str = None) -> List[Dict]:
    """
    Lista todas as classes da CNAE
    
    Args:
        id_grupo: ID opcional do grupo para filtrar classes
    """
    cache_key = f"cnae_classes{f'_grupo_{id_grupo}' if id_grupo else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_grupo:
            url = f"{BASE_URL_CNAE}/grupos/{id_grupo}/classes"
        else:
            url = f"{BASE_URL_CNAE}/classes"
        classes = make_request(url)
        return save_to_cache(cache_key, classes)
    except Exception as e:
        logger.error(f"Erro ao listar classes CNAE: {e}")
        return [{"erro": str(e)}]

def obter_classe(id_classe: str) -> Dict:
    """
    Obtém informações detalhadas de uma classe específica da CNAE
    
    Args:
        id_classe: ID da classe
    """
    cache_key = f"cnae_classe_{id_classe}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/classes/{id_classe}"
        classe = make_request(url)
        return save_to_cache(cache_key, classe)
    except Exception as e:
        logger.error(f"Erro ao obter classe CNAE {id_classe}: {e}")
        return {"erro": str(e)}

def listar_subclasses(id_classe: str = None) -> List[Dict]:
    """
    Lista todas as subclasses da CNAE
    
    Args:
        id_classe: ID opcional da classe para filtrar subclasses
    """
    cache_key = f"cnae_subclasses{f'_classe_{id_classe}' if id_classe else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_classe:
            url = f"{BASE_URL_CNAE}/classes/{id_classe}/subclasses"
        else:
            url = f"{BASE_URL_CNAE}/subclasses"
        subclasses = make_request(url)
        return save_to_cache(cache_key, subclasses)
    except Exception as e:
        logger.error(f"Erro ao listar subclasses CNAE: {e}")
        return [{"erro": str(e)}]

def obter_subclasse(id_subclasse: str) -> Dict:
    """
    Obtém informações detalhadas de uma subclasse específica da CNAE
    
    Args:
        id_subclasse: ID da subclasse
    """
    cache_key = f"cnae_subclasse_{id_subclasse}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/subclasses/{id_subclasse}"
        subclasse = make_request(url)
        return save_to_cache(cache_key, subclasse)
    except Exception as e:
        logger.error(f"Erro ao obter subclasse CNAE {id_subclasse}: {e}")
        return {"erro": str(e)}

def pesquisar_cnae(termo: str) -> List[Dict]:
    """
    Pesquisa na CNAE por um termo específico
    
    Args:
        termo: Termo a ser pesquisado
    """
    cache_key = f"cnae_pesquisa_{termo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/subclasses/busca"
        params = {"q": termo}
        resultados = make_request(url, params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao pesquisar CNAE com termo '{termo}': {e}")
        return [{"erro": str(e)}]
