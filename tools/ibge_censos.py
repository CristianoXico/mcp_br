"""
Módulo para acesso à API de Censos do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/censos
"""

from .ibge_base import *

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
        # Obtém a área territorial
        area_data = obter_area_territorial(localidade)
        if "erro" in area_data:
            return area_data
        
        # Obtém a população
        populacao_data = obter_populacao(localidade, periodo)
        if "erro" in populacao_data:
            return populacao_data
        
        # Extrai os valores
        area = None
        for item in area_data:
            if item.get("localidade", {}).get("id") == localidade:
                area = item.get("valor", 0)
                break
        
        populacao = None
        for item in populacao_data:
            if item.get("localidade", {}).get("id") == localidade:
                populacao = item.get("valor", 0)
                break
        
        if area is None or populacao is None or area == 0:
            return {"erro": "Não foi possível calcular a densidade demográfica"}
        
        # Calcula a densidade (habitantes por km²)
        densidade = populacao / area
        
        return {
            "localidade": localidade,
            "area_territorial": area,
            "populacao": populacao,
            "densidade_demografica": densidade,
            "unidade": "hab/km²"
        }
    except Exception as e:
        logger.error(f"Erro ao calcular densidade demográfica da localidade {localidade}: {e}")
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
        url = f"{BASE_URL_CENSOS}/indicadores"
        params = {"localidade": localidade}
        
        indicadores = make_request(url, params)
        return save_to_cache(cache_key, indicadores)
    except Exception as e:
        logger.error(f"Erro ao obter indicadores demográficos da localidade {localidade}: {e}")
        return {"erro": str(e)}
