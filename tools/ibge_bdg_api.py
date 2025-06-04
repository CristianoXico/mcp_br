"""
Funções utilitárias para acesso à API do Banco de Dados Geodésicos (BDG) do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/bdg?versao=1
"""

from typing import List, Dict
from .ibge_base import make_request, get_cached_data, save_to_cache, logger, BASE_URL_BDG


def listar_estacoes() -> List[Dict]:
    """
    Lista todas as estações geodésicas
    """
    cache_key = "bdg_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BDG}/estacoes"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações geodésicas: {e}")
        return []


def obter_estacao(id_estacao: str) -> Dict:
    """
    Obtém informações de uma estação geodésica específica
    Args:
        id_estacao: ID da estação geodésica
    """
    cache_key = f"bdg_estacao_{id_estacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BDG}/estacoes/{id_estacao}"
        estacao = make_request(url)
        return save_to_cache(cache_key, estacao)
    except Exception as e:
        logger.error(f"Erro ao obter estação geodésica {id_estacao}: {e}")
        return {"erro": str(e)}


def listar_estacoes_por_tipo(tipo: str) -> List[Dict]:
    """
    Lista estações geodésicas por tipo
    Args:
        tipo: Tipo de estação (SAT, RN, VT, etc.)
    """
    cache_key = f"bdg_estacoes_tipo_{tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BDG}/estacoes/tipo/{tipo}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações do tipo {tipo}: {e}")
        return []


def listar_estacoes_por_uf(uf: str) -> List[Dict]:
    """
    Lista estações geodésicas por UF
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
    """
    cache_key = f"bdg_estacoes_uf_{uf}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BDG}/estacoes/uf/{uf}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações da UF {uf}: {e}")
        return []
