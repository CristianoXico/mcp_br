"""
Módulo para acesso à API do Banco de Nomes Geográficos do Brasil (BNGB) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/bngb?versao=1
"""

from .ibge_base import *

def pesquisar_nomes_geograficos(nome: str, max_registros: int = 50) -> List[Dict]:
    """
    Pesquisa nomes geográficos no BNGB
    
    Args:
        nome: Nome a ser pesquisado
        max_registros: Número máximo de registros a serem retornados
    """
    cache_key = f"bngb_pesquisa_{nome}_{max_registros}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/nomes/{nome}"
        params = {"maxRegistros": max_registros}
        resultados = make_request(url, params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao pesquisar nome geográfico '{nome}': {e}")
        return []

def obter_nome_geografico(id_nome: str) -> Dict:
    """
    Obtém informações detalhadas de um nome geográfico pelo seu ID
    
    Args:
        id_nome: ID do nome geográfico
    """
    cache_key = f"bngb_nome_{id_nome}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/nomes/id/{id_nome}"
        nome = make_request(url)
        return save_to_cache(cache_key, nome)
    except Exception as e:
        logger.error(f"Erro ao obter nome geográfico com ID {id_nome}: {e}")
        return {"erro": str(e)}

def listar_tipos_nomes_geograficos() -> List[Dict]:
    """
    Lista todos os tipos de nomes geográficos
    """
    cache_key = "bngb_tipos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de nomes geográficos: {e}")
        return []

def listar_nomes_geograficos_por_tipo(id_tipo: str, max_registros: int = 50) -> List[Dict]:
    """
    Lista nomes geográficos por tipo
    
    Args:
        id_tipo: ID do tipo de nome geográfico
        max_registros: Número máximo de registros a serem retornados
    """
    cache_key = f"bngb_nomes_tipo_{id_tipo}_{max_registros}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/nomes/tipos/{id_tipo}"
        params = {"maxRegistros": max_registros}
        nomes = make_request(url, params)
        return save_to_cache(cache_key, nomes)
    except Exception as e:
        logger.error(f"Erro ao listar nomes geográficos do tipo {id_tipo}: {e}")
        return []

def listar_nomes_geograficos_por_uf(uf: str, max_registros: int = 50) -> List[Dict]:
    """
    Lista nomes geográficos por UF
    
    Args:
        uf: Sigla da UF (SP, RJ, MG, etc.)
        max_registros: Número máximo de registros a serem retornados
    """
    cache_key = f"bngb_nomes_uf_{uf}_{max_registros}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/nomes/uf/{uf}"
        params = {"maxRegistros": max_registros}
        nomes = make_request(url, params)
        return save_to_cache(cache_key, nomes)
    except Exception as e:
        logger.error(f"Erro ao listar nomes geográficos da UF {uf}: {e}")
        return []

def listar_nomes_geograficos_por_municipio(id_municipio: str, max_registros: int = 50) -> List[Dict]:
    """
    Lista nomes geográficos por município
    
    Args:
        id_municipio: ID do município
        max_registros: Número máximo de registros a serem retornados
    """
    cache_key = f"bngb_nomes_municipio_{id_municipio}_{max_registros}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_BNGB}/nomes/municipio/{id_municipio}"
        params = {"maxRegistros": max_registros}
        nomes = make_request(url, params)
        return save_to_cache(cache_key, nomes)
    except Exception as e:
        logger.error(f"Erro ao listar nomes geográficos do município {id_municipio}: {e}")
        return []
