"""
Módulo para acesso à API ProGrid do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/progrid?versao=1
"""

from .ibge_base import *

def listar_celulas() -> List[Dict]:
    """
    Lista todas as células ProGrid
    """
    cache_key = "progrid_celulas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas"
        celulas = make_request(url)
        return save_to_cache(cache_key, celulas)
    except Exception as e:
        logger.error(f"Erro ao listar células ProGrid: {e}")
        return []

def obter_celula(id_celula: str) -> Dict:
    """
    Obtém informações detalhadas de uma célula ProGrid pelo seu ID
    
    Args:
        id_celula: ID da célula
    """
    cache_key = f"progrid_celula_{id_celula}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/{id_celula}"
        celula = make_request(url)
        return save_to_cache(cache_key, celula)
    except Exception as e:
        logger.error(f"Erro ao obter célula ProGrid com ID {id_celula}: {e}")
        return {"erro": str(e)}

def listar_celulas_por_nivel(nivel: str) -> List[Dict]:
    """
    Lista células ProGrid por nível
    
    Args:
        nivel: Nível da célula (1, 2, 3, etc.)
    """
    cache_key = f"progrid_celulas_nivel_{nivel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/niveis/{nivel}"
        celulas = make_request(url)
        return save_to_cache(cache_key, celulas)
    except Exception as e:
        logger.error(f"Erro ao listar células ProGrid do nível {nivel}: {e}")
        return []

def listar_celulas_por_uf(uf: str) -> List[Dict]:
    """
    Lista células ProGrid por UF
    
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
    """
    cache_key = f"progrid_celulas_uf_{uf}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/uf/{uf}"
        celulas = make_request(url)
        return save_to_cache(cache_key, celulas)
    except Exception as e:
        logger.error(f"Erro ao listar células ProGrid da UF {uf}: {e}")
        return []

def listar_celulas_por_municipio(id_municipio: str) -> List[Dict]:
    """
    Lista células ProGrid por município
    
    Args:
        id_municipio: ID do município
    """
    cache_key = f"progrid_celulas_municipio_{id_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/municipio/{id_municipio}"
        celulas = make_request(url)
        return save_to_cache(cache_key, celulas)
    except Exception as e:
        logger.error(f"Erro ao listar células ProGrid do município {id_municipio}: {e}")
        return []

def listar_niveis_progrid() -> List[Dict]:
    """
    Lista todos os níveis ProGrid
    """
    cache_key = "progrid_niveis"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/niveis"
        niveis = make_request(url)
        return save_to_cache(cache_key, niveis)
    except Exception as e:
        logger.error(f"Erro ao listar níveis ProGrid: {e}")
        return []

def obter_nivel_progrid(nivel: str) -> Dict:
    """
    Obtém informações detalhadas de um nível ProGrid
    
    Args:
        nivel: Nível ProGrid (1, 2, 3, etc.)
    """
    cache_key = f"progrid_nivel_{nivel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PROGRID}/celulas/niveis/{nivel}"
        nivel_info = make_request(url)
        return save_to_cache(cache_key, nivel_info)
    except Exception as e:
        logger.error(f"Erro ao obter nível ProGrid {nivel}: {e}")
        return {"erro": str(e)}
