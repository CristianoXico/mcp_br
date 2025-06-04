"""
Funções utilitárias para acesso à API da RBMC do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1
"""

from typing import Dict, List, Optional
from .ibge_base import get_cached_data, save_to_cache, logger, BASE_URL_RBMC, make_request

def listar_estacoes() -> List[Dict]:
    cache_key = "rbmc_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RBMC: {e}")
        return []

def obter_estacao(id_estacao: str) -> Dict:
    cache_key = f"rbmc_estacao_{id_estacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/{id_estacao}"
        estacao = make_request(url)
        return save_to_cache(cache_key, estacao)
    except Exception as e:
        logger.error(f"Erro ao obter estação RBMC com ID {id_estacao}: {e}")
        return {"erro": str(e)}

def listar_estacoes_por_uf(uf: str) -> List[Dict]:
    cache_key = f"rbmc_estacoes_uf_{uf}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/uf/{uf}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RBMC da UF {uf}: {e}")
        return []

def listar_estacoes_por_municipio(id_municipio: str) -> List[Dict]:
    cache_key = f"rbmc_estacoes_municipio_{id_municipio}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/municipio/{id_municipio}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RBMC do município {id_municipio}: {e}")
        return []

def listar_estacoes_por_tipo(tipo: str) -> List[Dict]:
    cache_key = f"rbmc_estacoes_tipo_{tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/tipo/{tipo}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RBMC do tipo {tipo}: {e}")
        return []

def listar_tipos_estacoes() -> List[Dict]:
    cache_key = "rbmc_tipos_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de estações RBMC: {e}")
        return []

def listar_arquivos_estacao(id_estacao: str, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Dict]:
    cache_key = f"rbmc_arquivos_{id_estacao}_{data_inicio}_{data_fim}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/{id_estacao}/arquivos"
        params = {}
        if data_inicio:
            params["data_inicio"] = data_inicio
        if data_fim:
            params["data_fim"] = data_fim
        arquivos = make_request(url, params if params else None)
        return save_to_cache(cache_key, arquivos)
    except Exception as e:
        logger.error(f"Erro ao listar arquivos da estação RBMC {id_estacao}: {e}")
        return []

def obter_arquivo_estacao(id_estacao: str, id_arquivo: str) -> Dict:
    cache_key = f"rbmc_arquivo_{id_estacao}_{id_arquivo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_RBMC}/estacoes/{id_estacao}/arquivos/{id_arquivo}"
        arquivo = make_request(url)
        return save_to_cache(cache_key, arquivo)
    except Exception as e:
        logger.error(f"Erro ao obter arquivo da estação RBMC {id_estacao}, arquivo {id_arquivo}: {e}")
        return {"erro": str(e)}
