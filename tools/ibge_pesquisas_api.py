"""
Módulo utilitário para acesso à API de Pesquisas do IBGE
Funções de baixo nível, com cache, logging e tratamento de erros.
"""

from .ibge_base import *
from typing import List, Dict

def listar_pesquisas() -> List[Dict]:
    cache_key = "pesquisas_lista"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas"
        pesquisas = make_request(url)
        return save_to_cache(cache_key, pesquisas)
    except Exception as e:
        logger.error(f"Erro ao listar pesquisas: {e}")
        return []

def obter_pesquisa(id_pesquisa: str) -> Dict:
    cache_key = f"pesquisas_pesquisa_{id_pesquisa}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}"
        pesquisa = make_request(url)
        return save_to_cache(cache_key, pesquisa)
    except Exception as e:
        logger.error(f"Erro ao obter pesquisa com ID {id_pesquisa}: {e}")
        return {"erro": str(e)}

def listar_periodos_pesquisa(id_pesquisa: str) -> List[Dict]:
    cache_key = f"pesquisas_periodos_{id_pesquisa}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos"
        periodos = make_request(url)
        return save_to_cache(cache_key, periodos)
    except Exception as e:
        logger.error(f"Erro ao listar períodos da pesquisa {id_pesquisa}: {e}")
        return []

def obter_periodo_pesquisa(id_pesquisa: str, id_periodo: str) -> Dict:
    cache_key = f"pesquisas_periodo_{id_pesquisa}_{id_periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos/{id_periodo}"
        periodo = make_request(url)
        return save_to_cache(cache_key, periodo)
    except Exception as e:
        logger.error(f"Erro ao obter período {id_periodo} da pesquisa {id_pesquisa}: {e}")
        return {"erro": str(e)}

def listar_resultados_pesquisa(id_pesquisa: str, id_periodo: str) -> List[Dict]:
    cache_key = f"pesquisas_resultados_{id_pesquisa}_{id_periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos/{id_periodo}/resultados"
        resultados = make_request(url)
        return save_to_cache(cache_key, resultados)
    except Exception as e:
        logger.error(f"Erro ao listar resultados do período {id_periodo} da pesquisa {id_pesquisa}: {e}")
        return []

def obter_resultado_pesquisa(id_pesquisa: str, id_periodo: str, id_resultado: str) -> Dict:
    cache_key = f"pesquisas_resultado_{id_pesquisa}_{id_periodo}_{id_resultado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos/{id_periodo}/resultados/{id_resultado}"
        resultado = make_request(url)
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter resultado {id_resultado} do período {id_periodo} da pesquisa {id_pesquisa}: {e}")
        return {"erro": str(e)}

def listar_indicadores_pesquisa(id_pesquisa: str, id_periodo: str, id_resultado: str) -> List[Dict]:
    cache_key = f"pesquisas_indicadores_{id_pesquisa}_{id_periodo}_{id_resultado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos/{id_periodo}/resultados/{id_resultado}/indicadores"
        indicadores = make_request(url)
        return save_to_cache(cache_key, indicadores)
    except Exception as e:
        logger.error(f"Erro ao listar indicadores do resultado {id_resultado} do período {id_periodo} da pesquisa {id_pesquisa}: {e}")
        return []

def obter_indicador_pesquisa(id_pesquisa: str, id_periodo: str, id_resultado: str, id_indicador: str) -> Dict:
    cache_key = f"pesquisas_indicador_{id_pesquisa}_{id_periodo}_{id_resultado}_{id_indicador}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_PESQUISAS}/pesquisas/{id_pesquisa}/periodos/{id_periodo}/resultados/{id_resultado}/indicadores/{id_indicador}"
        indicador = make_request(url)
        return save_to_cache(cache_key, indicador)
    except Exception as e:
        logger.error(f"Erro ao obter indicador {id_indicador} do resultado {id_resultado} do período {id_periodo} da pesquisa {id_pesquisa}: {e}")
        return {"erro": str(e)}
