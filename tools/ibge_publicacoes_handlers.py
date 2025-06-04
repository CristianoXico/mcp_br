"""Handlers MCP e lógica de negócio para publicações do IBGE."""
from typing import Dict, List
from .ibge_publicacoes_api import api_get_publicacoes
from .cache_utils import get_cached_data, save_to_cache
from .logger import get_logger

logger = get_logger("ibge_publicacoes_handlers")

def listar_publicacoes(quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"publicacoes_lista_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {"qtd": quantidade, "page": pagina}
        publicacoes = api_get_publicacoes("publicacoes", params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações: {e}")
        return {"items": [], "erro": str(e)}

def obter_publicacao(id_publicacao: str) -> Dict:
    cache_key = f"publicacoes_publicacao_{id_publicacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        publicacao = api_get_publicacoes(f"publicacoes/{id_publicacao}")
        return save_to_cache(cache_key, publicacao)
    except Exception as e:
        logger.error(f"Erro ao obter publicação com ID {id_publicacao}: {e}")
        return {"erro": str(e)}

def listar_publicacoes_por_tipo(tipo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"publicacoes_tipo_{tipo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {"qtd": quantidade, "page": pagina}
        publicacoes = api_get_publicacoes(f"publicacoes/tipos/{tipo}", params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações do tipo {tipo}: {e}")
        return {"items": [], "erro": str(e)}

def listar_publicacoes_por_tema(tema: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"publicacoes_tema_{tema}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {"qtd": quantidade, "page": pagina}
        publicacoes = api_get_publicacoes(f"publicacoes/temas/{tema}", params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao listar publicações do tema {tema}: {e}")
        return {"items": [], "erro": str(e)}

def pesquisar_publicacoes(termo: str, quantidade: int = 10, pagina: int = 1) -> Dict:
    cache_key = f"publicacoes_pesquisa_{termo}_qtd_{quantidade}_pag_{pagina}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {"qtd": quantidade, "page": pagina}
        publicacoes = api_get_publicacoes(f"publicacoes/busca/{termo}", params)
        return save_to_cache(cache_key, publicacoes)
    except Exception as e:
        logger.error(f"Erro ao pesquisar publicações com o termo '{termo}': {e}")
        return {"items": [], "erro": str(e)}

def listar_tipos_publicacoes() -> List[Dict]:
    cache_key = "publicacoes_tipos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        tipos = api_get_publicacoes("publicacoes/tipos")
        return save_to_cache(cache_key, tipos)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de publicações: {e}")
        return []

def listar_temas_publicacoes() -> List[Dict]:
    cache_key = "publicacoes_temas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        temas = api_get_publicacoes("publicacoes/temas")
        return save_to_cache(cache_key, temas)
    except Exception as e:
        logger.error(f"Erro ao listar temas de publicações: {e}")
        return []
