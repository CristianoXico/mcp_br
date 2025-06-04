"""
Módulo para acesso à API de Notícias do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/noticias?versao=3
"""

from .ibge_base import *

def listar_noticias(quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista notícias do IBGE com paginação
    
    Args:
        quantidade: Número de notícias por página
        pagina: Número da página
    """
    cache_key = f"noticias_lista_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias: {e}")
        return {"items": [], "erro": str(e)}

def obter_noticia(id_noticia: str) -> Dict:
    """
    Obtém informações detalhadas de uma notícia pelo seu ID
    
    Args:
        id_noticia: ID da notícia
    """
    cache_key = f"noticias_noticia_{id_noticia}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/{id_noticia}"
        noticia = make_request(url)
        return save_to_cache(cache_key, noticia)
    except Exception as e:
        logger.error(f"Erro ao obter notícia com ID {id_noticia}: {e}")
        return {"erro": str(e)}

def listar_noticias_por_tipo(tipo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista notícias do IBGE por tipo
    
    Args:
        tipo: Tipo de notícia (release, noticia, etc.)
        quantidade: Número de notícias por página
        pagina: Número da página
    """
    cache_key = f"noticias_tipo_{tipo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/tipos/{tipo}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias do tipo {tipo}: {e}")
        return {"items": [], "erro": str(e)}

def listar_noticias_por_produto(id_produto: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Lista notícias do IBGE por produto
    
    Args:
        id_produto: ID do produto
        quantidade: Número de notícias por página
        pagina: Número da página
    """
    cache_key = f"noticias_produto_{id_produto}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/produtos/{id_produto}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias do produto {id_produto}: {e}")
        return {"items": [], "erro": str(e)}

def pesquisar_noticias(termo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    """
    Pesquisa notícias do IBGE por termo
    
    Args:
        termo: Termo a ser pesquisado
        quantidade: Número de notícias por página
        pagina: Número da página
    """
    cache_key = f"noticias_pesquisa_{termo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/busca/{termo}"
        params = {
            "qtd": quantidade,
            "page": pagina
        }
        
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao pesquisar notícias com o termo '{termo}': {e}")
        return {"items": [], "erro": str(e)}

def listar_tipos_noticias() -> List[Dict]:
    """
    Lista todos os tipos de notícias do IBGE
    """
    cache_key = "noticias_tipos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/tipos"
        tipos = make_request(url)
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de notícias: {e}")
        return []
