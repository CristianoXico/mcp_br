"""
Módulo para acesso à API de CNAE (Classificação Nacional de Atividades Econômicas) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/cnae
"""

from .ibge_base import *

def listar_secoes() -> List[Dict]:
    """Lista todas as seções da CNAE"""
    cache_key = "cnae_secoes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/secoes"
        secoes = make_request(url)
        return save_to_cache(cache_key, secoes)
    except Exception as e:
        logger.error(f"Erro ao listar seções CNAE: {e}")
        return [{"erro": str(e)}]

def obter_secao(id_secao: str) -> Dict:
    """
    Obtém informações detalhadas de uma seção específica da CNAE
    
    Args:
        id_secao: ID da seção
    """
    cache_key = f"cnae_secao_{id_secao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/secoes/{id_secao}"
        secao = make_request(url)
        return save_to_cache(cache_key, secao)
    except Exception as e:
        logger.error(f"Erro ao obter seção CNAE {id_secao}: {e}")
        return {"erro": str(e)}

def listar_divisoes(id_secao: str = None) -> List[Dict]:
    """
    Lista todas as divisões da CNAE
    
    Args:
        id_secao: ID opcional da seção para filtrar divisões
    """
    cache_key = f"cnae_divisoes{f'_secao_{id_secao}' if id_secao else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_secao:
            url = f"{BASE_URL_CNAE}/secoes/{id_secao}/divisoes"
        else:
            url = f"{BASE_URL_CNAE}/divisoes"
        divisoes = make_request(url)
        return save_to_cache(cache_key, divisoes)
    except Exception as e:
        logger.error(f"Erro ao listar divisões CNAE: {e}")
        return [{"erro": str(e)}]

def obter_divisao(id_divisao: str) -> Dict:
    """
    Obtém informações detalhadas de uma divisão específica da CNAE
    
    Args:
        id_divisao: ID da divisão
    """
    cache_key = f"cnae_divisao_{id_divisao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/divisoes/{id_divisao}"
        divisao = make_request(url)
        return save_to_cache(cache_key, divisao)
    except Exception as e:
        logger.error(f"Erro ao obter divisão CNAE {id_divisao}: {e}")
        return {"erro": str(e)}

def listar_grupos(id_divisao: str = None) -> List[Dict]:
    """
    Lista todos os grupos da CNAE
    
    Args:
        id_divisao: ID opcional da divisão para filtrar grupos
    """
    cache_key = f"cnae_grupos{f'_divisao_{id_divisao}' if id_divisao else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_divisao:
            url = f"{BASE_URL_CNAE}/divisoes/{id_divisao}/grupos"
        else:
            url = f"{BASE_URL_CNAE}/grupos"
        grupos = make_request(url)
        return save_to_cache(cache_key, grupos)
    except Exception as e:
        logger.error(f"Erro ao listar grupos CNAE: {e}")
        return [{"erro": str(e)}]

def obter_grupo(id_grupo: str) -> Dict:
    """
    Obtém informações detalhadas de um grupo específico da CNAE
    
    Args:
        id_grupo: ID do grupo
    """
    cache_key = f"cnae_grupo_{id_grupo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/grupos/{id_grupo}"
        grupo = make_request(url)
        return save_to_cache(cache_key, grupo)
    except Exception as e:
        logger.error(f"Erro ao obter grupo CNAE {id_grupo}: {e}")
        return {"erro": str(e)}

def listar_classes(id_grupo: str = None) -> List[Dict]:
    """
    Lista todas as classes da CNAE
    
    Args:
        id_grupo: ID opcional do grupo para filtrar classes
    """
    cache_key = f"cnae_classes{f'_grupo_{id_grupo}' if id_grupo else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_grupo:
            url = f"{BASE_URL_CNAE}/grupos/{id_grupo}/classes"
        else:
            url = f"{BASE_URL_CNAE}/classes"
        classes = make_request(url)
        return save_to_cache(cache_key, classes)
    except Exception as e:
        logger.error(f"Erro ao listar classes CNAE: {e}")
        return [{"erro": str(e)}]

def obter_classe(id_classe: str) -> Dict:
    """
    Obtém informações detalhadas de uma classe específica da CNAE
    
    Args:
        id_classe: ID da classe
    """
    cache_key = f"cnae_classe_{id_classe}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/classes/{id_classe}"
        classe = make_request(url)
        return save_to_cache(cache_key, classe)
    except Exception as e:
        logger.error(f"Erro ao obter classe CNAE {id_classe}: {e}")
        return {"erro": str(e)}

def listar_subclasses(id_classe: str = None) -> List[Dict]:
    """
    Lista todas as subclasses da CNAE
    
    Args:
        id_classe: ID opcional da classe para filtrar subclasses
    """
    cache_key = f"cnae_subclasses{f'_classe_{id_classe}' if id_classe else ''}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        if id_classe:
            url = f"{BASE_URL_CNAE}/classes/{id_classe}/subclasses"
        else:
            url = f"{BASE_URL_CNAE}/subclasses"
        subclasses = make_request(url)
        return save_to_cache(cache_key, subclasses)
    except Exception as e:
        logger.error(f"Erro ao listar subclasses CNAE: {e}")
        return [{"erro": str(e)}]

def obter_subclasse(id_subclasse: str) -> Dict:
    """
    Obtém informações detalhadas de uma subclasse específica da CNAE
    
    Args:
        id_subclasse: ID da subclasse
    """
    cache_key = f"cnae_subclasse_{id_subclasse}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/subclasses/{id_subclasse}"
        subclasse = make_request(url)
        return save_to_cache(cache_key, subclasse)
    except Exception as e:
        logger.error(f"Erro ao obter subclasse CNAE {id_subclasse}: {e}")
        return {"erro": str(e)}

def pesquisar_cnae(termo: str) -> List[Dict]:
    """
    Pesquisa na CNAE por um termo específico
    
    Args:
        termo: Termo a ser pesquisado
    """
    cache_key = f"cnae_pesquisa_{termo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_CNAE}/subclasses/busca"
        params = {"q": termo}
        resultados = make_request(url, params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao pesquisar CNAE com termo '{termo}': {e}")
        return [{"erro": str(e)}]
