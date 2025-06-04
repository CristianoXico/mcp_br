"""
Módulo para acesso à API de Publicações do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/publicacoes
"""

from .ibge_base import *

def listar_publicacoes(quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista publicações do IBGE com paginação
    
    Args:
        quantidade: Número de publicações por página
        pagina: Número da página
    """
    cache_key = f"publicacoes_lista_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        publicacoes = make_request(url, params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações: {e}")
        return {"items": [], "erro": str(e)}

def obter_publicacao(id_publicacao: str) -> Dict:
    """
    Obtém informações detalhadas de uma publicação pelo seu ID
    
    Args:
        id_publicacao: ID da publicação
    """
    cache_key = f"publicacoes_publicacao_{id_publicacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/{id_publicacao}"
        publicacao = make_request(url)
        return save_to_cache(cache_key, publicacao)
    except Exception as e:
        logger.error(f"Erro ao obter publicação com ID {id_publicacao}: {e}")
        return {"erro": str(e)}

def listar_publicacoes_por_tipo(tipo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista publicações do IBGE por tipo
    
    Args:
        tipo: Tipo de publicação (livro, revista, etc.)
        quantidade: Número de publicações por página
        pagina: Número da página
    """
    cache_key = f"publicacoes_tipo_{tipo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/tipos/{tipo}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        publicacoes = make_request(url, params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações do tipo {tipo}: {e}")
        return {"items": [], "erro": str(e)}

def listar_publicacoes_por_tema(tema: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista publicações do IBGE por tema
    
    Args:
        tema: Tema da publicação
        quantidade: Número de publicações por página
        pagina: Número da página
    """
    cache_key = f"publicacoes_tema_{tema}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/temas/{tema}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        publicacoes = make_request(url, params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações do tema {tema}: {e}")
        return {"items": [], "erro": str(e)}

def pesquisar_publicacoes(termo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Pesquisa publicações do IBGE por termo
    
    Args:
        termo: Termo a ser pesquisado
        quantidade: Número de publicações por página
        pagina: Número da página
    """
    cache_key = f"publicacoes_pesquisa_{termo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/busca/{termo}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        publicacoes = make_request(url, params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao pesquisar publicações com o termo '{termo}': {e}")
        return {"items": [], "erro": str(e)}

def listar_tipos_publicacoes() -> List[Dict]:
    """
    Lista todos os tipos de publicações do IBGE
    """
    cache_key = "publicacoes_tipos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de publicações: {e}")
        return []

def listar_temas_publicacoes() -> List[Dict]:
    """
    Lista todos os temas de publicações do IBGE
    """
    cache_key = "publicacoes_temas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_PUBLICACOES}/publicacoes/temas"
        temas = make_request(url)
        return save_to_cache(cache_key, temas)
    except Exception as e:
        logger.error(f"Erro ao listar temas de publicações: {e}")
        return []
