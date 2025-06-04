"""
Funções utilitárias para acesso à API da RMPG do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/rmpg?versao=1
"""

from typing import Dict, List, Optional
from .ibge_base import get_cached_data, save_to_cache, logger, BASE_URL_RMPG, make_request

def listar_estacoes() -> List[Dict]:
    cache_key = "rmpg_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RMPG: {e}")
        return []

def obter_estacao(id_estacao: str) -> Dict:
    cache_key = f"rmpg_estacao_{id_estacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/{id_estacao}"
        estacao = make_request(url)
        return save_to_cache(cache_key, estacao)
    except Exception as e:
        logger.error(f"Erro ao obter estação RMPG com ID {id_estacao}: {e}")
        return {"erro": str(e)}

def listar_estacoes_por_uf(uf: str) -> List[Dict]:
    cache_key = f"rmpg_estacoes_uf_{uf}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/uf/{uf}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RMPG da UF {uf}: {e}")
        return []

def listar_estacoes_por_municipio(id_municipio: str) -> List[Dict]:
    cache_key = f"rmpg_estacoes_municipio_{id_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/municipio/{id_municipio}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RMPG do município {id_municipio}: {e}")
        return []

def listar_estacoes_por_status(status: str) -> List[Dict]:
    cache_key = f"rmpg_estacoes_status_{status}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/status/{status}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RMPG do status {status}: {e}")
        return []

def listar_status_estacoes() -> List[Dict]:
    cache_key = "rmpg_status_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/status"
        status = make_request(url)
        return save_to_cache(cache_key, status)
    except Exception as e:
        logger.error(f"Erro ao listar status das estações RMPG: {e}")
        return []

def listar_dados_estacao(id_estacao: str, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Dict]:
    cache_key = f"rmpg_dados_{id_estacao}_{data_inicio}_{data_fim}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/{id_estacao}/dados"
        params = {}
        if data_inicio:
            params["data_inicio"] = data_inicio
        if data_fim:
            params["data_fim"] = data_fim
        dados = make_request(url, params if params else None)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao listar dados da estação RMPG {id_estacao}: {e}")
        return []

def obter_dado_estacao(id_estacao: str, id_dado: str) -> Dict:
    cache_key = f"rmpg_dado_{id_estacao}_{id_dado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RMPG}/estacoes/{id_estacao}/dados/{id_dado}"
        dado = make_request(url)
        return save_to_cache(cache_key, dado)
    except Exception as e:
        logger.error(f"Erro ao obter dado da estação RMPG {id_estacao}, dado {id_dado}: {e}")
        return {"erro": str(e)}
