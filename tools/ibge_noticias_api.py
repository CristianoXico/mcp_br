"""
Funções utilitárias para acesso à API de Notícias do IBGE.
Documentação: https://servicodados.ibge.gov.br/api/docs/noticias?versao=3
"""

from typing import Dict
from .ibge_base import get_cached_data, save_to_cache, logger, BASE_URL_NOTICIAS, make_request

def listar_noticias(quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"noticias_lista_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_NOTICIAS}/noticias"
        params = {"qtd": quantidade, "page": pagina}
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias: {e}")
        return {"items": [], "erro": str(e)}

def obter_noticia(id_noticia: str) -> Dict:
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
    cache_key = f"noticias_tipo_{tipo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/tipo/{tipo}"
        params = {"qtd": quantidade, "page": pagina}
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias por tipo {tipo}: {e}")
        return {"items": [], "erro": str(e)}

def listar_noticias_por_produto(id_produto: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"noticias_produto_{id_produto}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/produto/{id_produto}"
        params = {"qtd": quantidade, "page": pagina}
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao listar notícias por produto {id_produto}: {e}")
        return {"items": [], "erro": str(e)}

def pesquisar_noticias(termo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"noticias_pesquisa_{termo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_NOTICIAS}/noticias/pesquisa/{termo}"
        params = {"qtd": quantidade, "page": pagina}
        noticias = make_request(url, params)
        return save_to_cache(cache_key, noticias)
    except Exception as e:
        logger.error(f"Erro ao pesquisar notícias pelo termo {termo}: {e}")
        return {"items": [], "erro": str(e)}

def listar_tipos_noticias() -> Dict:
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
        return {"tipos": [], "erro": str(e)}
