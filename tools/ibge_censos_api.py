"""
Funções utilitárias para acesso à API de Censos do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/censos
"""

from typing import List, Dict
from .ibge_base import make_request, get_cached_data, save_to_cache, logger, BASE_URL_CENSOS


def obter_area_territorial(localidade: str) -> Dict:
    """
    Obtém a área territorial de uma localidade
    Args:
        localidade: ID da localidade (código do município, UF, etc.)
    """
    cache_key = f"area_territorial_{localidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_CENSOS}/area/{localidade}"
        area_data = make_request(url)
        return save_to_cache(cache_key, area_data)
    except Exception as e:
        logger.error(f"Erro ao obter área territorial da localidade {localidade}: {e}")
        return {"erro": str(e)}


def obter_populacao(localidade: str, periodo: str = None) -> Dict:
    """
    Obtém a população de uma localidade
    Args:
        localidade: ID da localidade (código do município, UF, etc.)
        periodo: Período de referência (opcional)
    """
    cache_key = f"populacao_{localidade}{f'_periodo_{periodo}' if periodo else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_CENSOS}/populacao/{localidade}"
        if periodo:
            url += f"/{periodo}"
        populacao_data = make_request(url)
        return save_to_cache(cache_key, populacao_data)
    except Exception as e:
        logger.error(f"Erro ao obter população da localidade {localidade}: {e}")
        return {"erro": str(e)}


def calcular_densidade_demografica(localidade: str, periodo: str = None) -> Dict:
    """
    Calcula a densidade demográfica de uma localidade
    Args:
        localidade: ID da localidade (código do município, UF, etc.)
        periodo: Período de referência (opcional)
    """
    try:
        area = obter_area_territorial(localidade)
        populacao = obter_populacao(localidade, periodo)
        if not area or not populacao or "erro" in area or "erro" in populacao:
            return {"erro": "Dados insuficientes para cálculo de densidade."}
        area_val = area.get("area", 0)
        pop_val = populacao.get("populacao", 0)
        if area_val == 0:
            return {"erro": "Área territorial inválida."}
        densidade = pop_val / area_val
        return {"densidade_demografica": densidade}
    except Exception as e:
        logger.error(f"Erro ao calcular densidade demográfica: {e}")
        return {"erro": str(e)}


def obter_indicadores_demograficos(localidade: str = "BR") -> Dict:
    """
    Obtém indicadores demográficos de uma localidade
    Args:
        localidade: ID da localidade (BR para Brasil, UF para estados, etc.)
    """
    cache_key = f"indicadores_demograficos_{localidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_CENSOS}/indicadores/{localidade}"
        indicadores = make_request(url)
        return save_to_cache(cache_key, indicadores)
    except Exception as e:
        logger.error(f"Erro ao obter indicadores demográficos da localidade {localidade}: {e}")
        return {"erro": str(e)}
