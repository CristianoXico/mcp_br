"""
Módulo para acesso à API de Calendário do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/calendario?versao=3
"""

from .ibge_base import *

def listar_eventos(data_inicio: str = None, data_fim: str = None) -> List[Dict]:
    """
    Lista eventos do calendário do IBGE
    
    Args:
        data_inicio: Data de início no formato AAAA-MM-DD (opcional)
        data_fim: Data de fim no formato AAAA-MM-DD (opcional)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"data_inicio_{data_inicio}_data_fim_{data_fim}"
    cache_key = f"calendario_eventos_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CALENDARIO}/eventos"
        
        # Parâmetros da consulta
        params = {}
        
        if data_inicio:
            params["data"] = data_inicio
            if data_fim:
                params["data"] += f",{data_fim}"
        
        # Faz a requisição
        eventos = make_request(url, params)
        return save_to_cache(cache_key, eventos)
    except Exception as e:
        logger.error(f"Erro ao listar eventos do calendário: {e}")
        return []

def obter_evento(id_evento: str) -> Dict:
    """
    Obtém informações detalhadas de um evento pelo seu ID
    
    Args:
        id_evento: ID do evento
    """
    cache_key = f"calendario_evento_{id_evento}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CALENDARIO}/eventos/{id_evento}"
        evento = make_request(url)
        return save_to_cache(cache_key, evento)
    except Exception as e:
        logger.error(f"Erro ao obter evento com ID {id_evento}: {e}")
        return {"erro": str(e)}

def listar_eventos_por_tipo(tipo: str, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
    """
    Lista eventos do calendário do IBGE por tipo
    
    Args:
        tipo: Tipo de evento (divulgacao, coleta, etc.)
        data_inicio: Data de início no formato AAAA-MM-DD (opcional)
        data_fim: Data de fim no formato AAAA-MM-DD (opcional)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"tipo_{tipo}_data_inicio_{data_inicio}_data_fim_{data_fim}"
    cache_key = f"calendario_eventos_tipo_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CALENDARIO}/eventos/tipos/{tipo}"
        
        # Parâmetros da consulta
        params = {}
        
        if data_inicio:
            params["data"] = data_inicio
            if data_fim:
                params["data"] += f",{data_fim}"
        
        # Faz a requisição
        eventos = make_request(url, params)
        return save_to_cache(cache_key, eventos)
    except Exception as e:
        logger.error(f"Erro ao listar eventos do tipo {tipo}: {e}")
        return []

def listar_eventos_por_produto(id_produto: str, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
    """
    Lista eventos do calendário do IBGE por produto
    
    Args:
        id_produto: ID do produto
        data_inicio: Data de início no formato AAAA-MM-DD (opcional)
        data_fim: Data de fim no formato AAAA-MM-DD (opcional)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"produto_{id_produto}_data_inicio_{data_inicio}_data_fim_{data_fim}"
    cache_key = f"calendario_eventos_produto_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CALENDARIO}/eventos/produtos/{id_produto}"
        
        # Parâmetros da consulta
        params = {}
        
        if data_inicio:
            params["data"] = data_inicio
            if data_fim:
                params["data"] += f",{data_fim}"
        
        # Faz a requisição
        eventos = make_request(url, params)
        return save_to_cache(cache_key, eventos)
    except Exception as e:
        logger.error(f"Erro ao listar eventos do produto {id_produto}: {e}")
        return []

def listar_tipos_eventos() -> List[Dict]:
    """
    Lista todos os tipos de eventos do calendário do IBGE
    """
    cache_key = "calendario_tipos_eventos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CALENDARIO}/eventos/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de eventos: {e}")
        return []
