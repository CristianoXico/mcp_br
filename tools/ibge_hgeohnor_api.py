"""
Funções utilitárias para acesso à API hgeoHNOR do IBGE (requisições HTTP, cache, autenticação, logging).
Documentação: https://servicodados.ibge.gov.br/api/docs/hgeohnor?versao=1
"""

from typing import List, Dict
from .ibge_base import make_request, get_cached_data, save_to_cache, logger, BASE_URL_HGEOHNOR


def listar_estacoes() -> List[Dict]:
    """
    Lista todas as estações da Rede Altimétrica de Alta Precisão (RAAP)
    """
    cache_key = "hgeohnor_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/estacoes"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RAAP: {e}")
        return []


def obter_estacao(id_estacao: str) -> Dict:
    """
    Obtém informações detalhadas de uma estação da RAAP pelo seu ID
    Args:
        id_estacao: ID da estação
    """
    cache_key = f"hgeohnor_estacao_{id_estacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/estacoes/{id_estacao}"
        estacao = make_request(url)
        return save_to_cache(cache_key, estacao)
    except Exception as e:
        logger.error(f"Erro ao obter estação RAAP com ID {id_estacao}: {e}")
        return {"erro": str(e)}


def listar_estacoes_por_uf(uf: str) -> List[Dict]:
    """
    Lista estações da RAAP por UF
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
    """
    cache_key = f"hgeohnor_estacoes_uf_{uf}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/estacoes/uf/{uf}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RAAP da UF {uf}: {e}")
        return []


def listar_estacoes_por_municipio(id_municipio: str) -> List[Dict]:
    """
    Lista estações da RAAP por município
    Args:
        id_municipio: ID do município
    """
    cache_key = f"hgeohnor_estacoes_municipio_{id_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/estacoes/municipio/{id_municipio}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RAAP do município {id_municipio}: {e}")
        return []


def listar_estacoes_por_tipo(tipo: str) -> List[Dict]:
    """
    Lista estações da RAAP por tipo
    Args:
        tipo: Tipo de estação (RN, RRNN, etc.)
    """
    cache_key = f"hgeohnor_estacoes_tipo_{tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/estacoes/tipo/{tipo}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RAAP do tipo {tipo}: {e}")
        return []


def listar_tipos_estacoes() -> List[Dict]:
    """
    Lista todos os tipos de estações da RAAP
    """
    cache_key = "hgeohnor_tipos_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_HGEOHNOR}/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de estações RAAP: {e}")
        return []
