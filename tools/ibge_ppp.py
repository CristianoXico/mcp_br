"""
Módulo para acesso à API do Serviço de Posicionamento por Ponto Preciso (IBGE-PPP) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/ppp?versao=1
"""

from .ibge_base import *

def listar_processamentos() -> List[Dict]:
    """
    Lista todos os processamentos PPP
    """
    cache_key = "ppp_processamentos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos"
        processamentos = make_request(url)
        return save_to_cache(cache_key, processamentos)
    except Exception as e:
        logger.error(f"Erro ao listar processamentos PPP: {e}")
        return []

def obter_processamento(id_processamento: str) -> Dict:
    """
    Obtém informações detalhadas de um processamento PPP pelo seu ID
    
    Args:
        id_processamento: ID do processamento
    """
    cache_key = f"ppp_processamento_{id_processamento}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos/{id_processamento}"
        processamento = make_request(url)
        return save_to_cache(cache_key, processamento)
    except Exception as e:
        logger.error(f"Erro ao obter processamento PPP com ID {id_processamento}: {e}")
        return {"erro": str(e)}

def listar_processamentos_por_status(status: str) -> List[Dict]:
    """
    Lista processamentos PPP por status
    
    Args:
        status: Status do processamento (CONCLUIDO, PROCESSANDO, ERRO, etc.)
    """
    cache_key = f"ppp_processamentos_status_{status}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos/status/{status}"
        processamentos = make_request(url)
        return save_to_cache(cache_key, processamentos)
    except Exception as e:
        logger.error(f"Erro ao listar processamentos PPP com status {status}: {e}")
        return []

def listar_processamentos_por_usuario(id_usuario: str) -> List[Dict]:
    """
    Lista processamentos PPP por usuário
    
    Args:
        id_usuario: ID do usuário
    """
    cache_key = f"ppp_processamentos_usuario_{id_usuario}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos/usuario/{id_usuario}"
        processamentos = make_request(url)
        return save_to_cache(cache_key, processamentos)
    except Exception as e:
        logger.error(f"Erro ao listar processamentos PPP do usuário {id_usuario}: {e}")
        return []

def listar_status_processamentos() -> List[Dict]:
    """
    Lista todos os status possíveis para processamentos PPP
    """
    cache_key = "ppp_status"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos/status"
        status = make_request(url)
        return save_to_cache(cache_key, status)
    except Exception as e:
        logger.error(f"Erro ao listar status de processamentos PPP: {e}")
        return []

def obter_resultado_processamento(id_processamento: str) -> Dict:
    """
    Obtém o resultado de um processamento PPP pelo seu ID
    
    Args:
        id_processamento: ID do processamento
    """
    cache_key = f"ppp_resultado_{id_processamento}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PPP}/processamentos/{id_processamento}/resultado"
        resultado = make_request(url)
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter resultado do processamento PPP com ID {id_processamento}: {e}")
        return {"erro": str(e)}
