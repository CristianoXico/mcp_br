"""
Módulo para acesso à API da Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS (RBMC) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/rbmc?versao=1
"""

from .ibge_base import *

def listar_estacoes() -> List[Dict]:
    """
    Lista todas as estações da RBMC
    """
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
    """
    Obtém informações detalhadas de uma estação da RBMC pelo seu ID
    
    Args:
        id_estacao: ID da estação
    """
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
    """
    Lista estações da RBMC por UF
    
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
    """
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
    """
    Lista estações da RBMC por município
    
    Args:
        id_municipio: ID do município
    """
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
    """
    Lista estações da RBMC por tipo
    
    Args:
        tipo: Tipo de estação (GNSS, GPS, etc.)
    """
    cache_key = f"rbmc_estacoes_tipo_{tipo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RBMC}/estacoes/tipos/{tipo}"
        estacoes = make_request(url)
        return save_to_cache(cache_key, estacoes)
    except Exception as e:
        logger.error(f"Erro ao listar estações RBMC do tipo {tipo}: {e}")
        return []

def listar_tipos_estacoes() -> List[Dict]:
    """
    Lista todos os tipos de estações da RBMC
    """
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

def listar_arquivos_estacao(id_estacao: str, data_inicio: str = None, data_fim: str = None) -> List[Dict]:
    """
    Lista arquivos de uma estação da RBMC
    
    Args:
        id_estacao: ID da estação
        data_inicio: Data de início no formato AAAA-MM-DD (opcional)
        data_fim: Data de fim no formato AAAA-MM-DD (opcional)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"estacao_{id_estacao}_data_inicio_{data_inicio}_data_fim_{data_fim}"
    cache_key = f"rbmc_arquivos_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RBMC}/estacoes/{id_estacao}/arquivos"
        
        # Parâmetros da consulta
        params = {}
        
        if data_inicio:
            params["data"] = data_inicio
            if data_fim:
                params["data"] += f",{data_fim}"
        
        # Faz a requisição
        arquivos = make_request(url, params)
        return save_to_cache(cache_key, arquivos)
    except Exception as e:
        logger.error(f"Erro ao listar arquivos da estação RBMC {id_estacao}: {e}")
        return []

def obter_arquivo_estacao(id_estacao: str, id_arquivo: str) -> Dict:
    """
    Obtém informações detalhadas de um arquivo de uma estação da RBMC
    
    Args:
        id_estacao: ID da estação
        id_arquivo: ID do arquivo
    """
    cache_key = f"rbmc_arquivo_{id_estacao}_{id_arquivo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_RBMC}/estacoes/{id_estacao}/arquivos/{id_arquivo}"
        arquivo = make_request(url)
        return save_to_cache(cache_key, arquivo)
    except Exception as e:
        logger.error(f"Erro ao obter arquivo {id_arquivo} da estação RBMC {id_estacao}: {e}")
        return {"erro": str(e)}
