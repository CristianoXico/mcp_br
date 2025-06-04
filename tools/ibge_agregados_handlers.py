"""
Handlers MCP e lógica de negócio para Agregados do IBGE.
"""
from typing import Dict, List, Optional
from .ibge_agregados_api import api_get_agregados
from .cache_utils import get_cached_data, save_to_cache
from .logger import get_logger

logger = get_logger("ibge_agregados_handlers")

def listar_agregados() -> List[Dict]:
    cache_key = "agregados"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        agregados = api_get_agregados()
        return save_to_cache(cache_key, agregados)
    except Exception as e:
        logger.error(f"Erro ao listar agregados: {e}")
        return [{"erro": str(e)}]

def obter_agregado_por_id(id_agregado: str) -> Dict:
    cache_key = f"agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        agregado = api_get_agregados(f"{id_agregado}")
        return save_to_cache(cache_key, agregado)
    except Exception as e:
        logger.error(f"Erro ao obter agregado {id_agregado}: {e}")
        return {"erro": str(e)}

def listar_periodos_agregado(id_agregado: str) -> List[Dict]:
    cache_key = f"periodos_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        periodos = api_get_agregados(f"{id_agregado}/periodos")
        return save_to_cache(cache_key, periodos)
    except Exception as e:
        logger.error(f"Erro ao listar períodos do agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]

def listar_variaveis_agregado(id_agregado: str) -> List[Dict]:
    cache_key = f"variaveis_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        variaveis = api_get_agregados(f"{id_agregado}/variaveis")
        return save_to_cache(cache_key, variaveis)
    except Exception as e:
        logger.error(f"Erro ao listar variáveis do agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]

def listar_localidades_agregado(id_agregado: str) -> List[Dict]:
    cache_key = f"localidades_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        localidades = api_get_agregados(f"{id_agregado}/localidades")
        return save_to_cache(cache_key, localidades)
    except Exception as e:
        logger.error(f"Erro ao listar localidades do agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]

def listar_niveis_territoriais_agregado(id_agregado: str) -> List[Dict]:
    cache_key = f"niveis_territoriais_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        niveis = api_get_agregados(f"{id_agregado}/niveis-territoriais")
        return save_to_cache(cache_key, niveis)
    except Exception as e:
        logger.error(f"Erro ao listar níveis territoriais do agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]

def obter_metadados_agregado(id_agregado: str) -> Dict:
    cache_key = f"metadados_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        metadados = api_get_agregados(f"{id_agregado}/metadados")
        return save_to_cache(cache_key, metadados)
    except Exception as e:
        logger.error(f"Erro ao obter metadados do agregado {id_agregado}: {e}")
        return {"erro": str(e)}

def consultar_agregado(
    id_agregado: str,
    variaveis: List[str],
    localidades: Optional[List[str]] = None,
    classificacoes: Optional[Dict[str, List[str]]] = None,
    periodo: Optional[List[str]] = None
) -> List[Dict]:
    cache_key = f"consulta_agregado_{id_agregado}_{'_'.join(variaveis)}_{'_'.join(localidades or [])}_{str(classificacoes)}_{'_'.join(periodo or [])}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        params = {"variaveis": ','.join(variaveis)}
        if localidades:
            params["localidades"] = ','.join(localidades)
        if classificacoes:
            for k, v in classificacoes.items():
                params[f"classificacao[{k}]"] = ','.join(v)
        if periodo:
            params["periodos"] = ','.join(periodo)
        dados = api_get_agregados(f"{id_agregado}/dados", params)
        return save_to_cache(cache_key, dados)
    except Exception as e:
        logger.error(f"Erro ao consultar agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]
