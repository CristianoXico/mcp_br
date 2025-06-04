"""
Handlers MCP e lógica de negócio para nomes do IBGE.
"""
from typing import Dict, List, Optional
from .ibge_nomes_api import api_get_nomes
from .cache_utils import get_cached_data, save_to_cache
from .logger import get_logger

logger = get_logger("ibge_nomes_handlers")

def pesquisar_nomes(nome: str) -> List[Dict]:
    cache_key = f"nomes_pesquisa_{nome}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        resultados = api_get_nomes(f"{nome}")
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao pesquisar nome '{nome}': {e}")
        return [{"erro": str(e)}]

def ranking_nomes(
    localidade: Optional[str] = None,
    sexo: Optional[str] = None,
    decada: Optional[str] = None,
    periodo_inicio: Optional[str] = None,
    periodo_fim: Optional[str] = None
) -> List[Dict]:
    params_str = f"localidade_{localidade}_sexo_{sexo}_decada_{decada}_periodo_{periodo_inicio}_{periodo_fim}"
    cache_key = f"nomes_ranking_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {}
        if localidade:
            params["localidade"] = localidade
        if sexo:
            params["sexo"] = sexo
        if decada:
            params["decada"] = decada
        if periodo_inicio:
            params["periodo_inicio"] = periodo_inicio
        if periodo_fim:
            params["periodo_fim"] = periodo_fim
        resultados = api_get_nomes("ranking", params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao obter ranking de nomes: {e}")
        return [{"erro": str(e)}]

def frequencia_nome(
    nome: str,
    localidade: Optional[str] = None,
    sexo: Optional[str] = None,
    decada: Optional[str] = None,
    periodo_inicio: Optional[str] = None,
    periodo_fim: Optional[str] = None
) -> List[Dict]:
    params_str = f"nome_{nome}_localidade_{localidade}_sexo_{sexo}_decada_{decada}_periodo_{periodo_inicio}_{periodo_fim}"
    cache_key = f"nomes_frequencia_{params_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {}
        if localidade:
            params["localidade"] = localidade
        if sexo:
            params["sexo"] = sexo
        if decada:
            params["decada"] = decada
        if periodo_inicio:
            params["periodo_inicio"] = periodo_inicio
        if periodo_fim:
            params["periodo_fim"] = periodo_fim
        resultados = api_get_nomes(f"frequencia/{nome}", params)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao obter frequência do nome '{nome}': {e}")
        return [{"erro": str(e)}]
