"""
Módulo para acesso à API de Nomes do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/nomes
"""

from .ibge_base import *

def pesquisar_nomes(nome: str) -> List[Dict]:
    """
    Pesquisa informações sobre um nome específico
    
    Args:
        nome: Nome a ser pesquisado
    """
    cache_key = f"nomes_pesquisa_{nome}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOMES}/{nome}"
        resultados = make_request(url)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao pesquisar nome '{nome}': {e}")
        return [{"erro": str(e)}]

def ranking_nomes(
    localidade: str = None, 
    sexo: str = None, 
    decada: str = None,
    periodo_inicio: str = None,
    periodo_fim: str = None
) -> List[Dict]:
    """
    Obtém o ranking de nomes mais populares
    
    Args:
        localidade: ID da localidade (BR para Brasil, UF para estados, etc.)
        sexo: Filtro por sexo (M ou F)
        decada: Filtro por década (1930, 1940, etc.)
        periodo_inicio: Ano de início do período (se não for por década)
        periodo_fim: Ano de fim do período (se não for por década)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"localidade_{localidade}_sexo_{sexo}_decada_{decada}_periodo_{periodo_inicio}_{periodo_fim}"
    cache_key = f"nomes_ranking_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOMES}/ranking"
        
        # Parâmetros da consulta
        params = {}
        
        if localidade:
            params["localidade"] = localidade
        
        if sexo:
            params["sexo"] = sexo
        
        # Configuração do período
        if decada:
            params["decada"] = decada
        elif periodo_inicio and periodo_fim:
            params["periodo"] = f"{periodo_inicio},{periodo_fim}"
        
        # Faz a requisição
        resultados = make_request(url, params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao obter ranking de nomes: {e}")
        return [{"erro": str(e)}]

def frequencia_nome(
    nome: str,
    localidade: str = None, 
    sexo: str = None, 
    decada: str = None,
    periodo_inicio: str = None,
    periodo_fim: str = None
) -> List[Dict]:
    """
    Obtém a frequência de um nome ao longo do tempo
    
    Args:
        nome: Nome a ser pesquisado
        localidade: ID da localidade (BR para Brasil, UF para estados, etc.)
        sexo: Filtro por sexo (M ou F)
        decada: Filtro por década (1930, 1940, etc.)
        periodo_inicio: Ano de início do período (se não for por década)
        periodo_fim: Ano de fim do período (se não for por década)
    """
    # Constrói a chave de cache baseada nos parâmetros
    params_str = f"nome_{nome}_localidade_{localidade}_sexo_{sexo}_decada_{decada}_periodo_{periodo_inicio}_{periodo_fim}"
    cache_key = f"nomes_frequencia_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOMES}/{nome}/frequencia"
        
        # Parâmetros da consulta
        params = {}
        
        if localidade:
            params["localidade"] = localidade
        
        if sexo:
            params["sexo"] = sexo
        
        # Configuração do período
        if decada:
            params["decada"] = decada
        elif periodo_inicio and periodo_fim:
            params["periodo"] = f"{periodo_inicio},{periodo_fim}"
        
        # Faz a requisição
        resultados = make_request(url, params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao obter frequência do nome '{nome}': {e}")
        return [{"erro": str(e)}]
