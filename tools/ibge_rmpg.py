"""
Módulo para acesso à API da Rede Maregráfica Permanente para Geodésia (RMPG) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/rmpg?versao=1
"""

from .ibge_base import *

def listar_estacoes() -> List[Dict]:
    """
    Lista todas as estações da RMPG
    """
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
    """
    Obtém informações detalhadas de uma estação da RMPG pelo seu ID
    
    Args:
        id_estacao: ID da estação
    """
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
    """
    Lista estações da RMPG por UF
    
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
    """
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
    """
    Lista estações da RMPG por município
    
    Args:
        id_municipio: ID do município
    """
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
    """
    Lista estações da RMPG por status
    
    Args:
        status: Status da estação (ATIVA, INATIVA, etc.)
    """
    cache_key = f"rmpg_estacoes_status_{status}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RMPG}/estacoes/status/{status}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RMPG com status {status}: {e}")
        return []

def listar_status_estacoes() -> List[Dict]:
    """
    Lista todos os status possíveis para estações da RMPG
    """
    cache_key = "rmpg_status_estacoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RMPG}/estacoes/status"
        status = make_request(url)
        return save_to_cache(cache_key, status)
    except Exception as e:
        logger.error(f"Erro ao listar status de estações RMPG: {e}")
        return []

def listar_dados_estacao(id_estacao: str, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
    """
    Lista dados de uma estação da RMPG
    
    Args:
        id_estacao: ID da estação
        data_inicio: Data de início no formato AAAA-MM-DD (opcional)
        data_fim: Data de fim no formato AAAA-MM-DD (opcional)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"estacao_{id_estacao}_data_inicio_{data_inicio}_data_fim_{data_fim}"
    cache_key = f"rmpg_dados_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RMPG}/estacoes/{id_estacao}/dados"
        
        # Parâmetros da consulta
        params = {}
        
        if data_inicio:
            params["data"] = data_inicio
            if data_fim:
                params["data"] += f",{data_fim}"
        
        # Faz a requisição
        dados = make_request(url, params)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao listar dados da estação RMPG {id_estacao}: {e}")
        return []

def obter_dado_estacao(id_estacao: str, id_dado: str) -> Dict:
    """
    Obtém informações detalhadas de um dado de uma estação da RMPG
    
    Args:
        id_estacao: ID da estação
        id_dado: ID do dado
    """
    cache_key = f"rmpg_dado_{id_estacao}_{id_dado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RMPG}/estacoes/{id_estacao}/dados/{id_dado}"
        dado = make_request(url)
        return save_to_cache(cache_key, dado)
    except Exception as e:
        logger.error(f"Erro ao obter dado {id_dado} da estação RMPG {id_estacao}: {e}")
        return {"erro": str(e)}
