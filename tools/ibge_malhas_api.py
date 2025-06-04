"""
Funções utilitárias para acesso à API de Malhas do IBGE (requisições HTTP, cache, autenticação, logging).
Documentação: https://servicodados.ibge.gov.br/api/docs/malhas
"""

from typing import Dict
from .ibge_base import get_cached_data, save_to_cache, logger, BASE_URL_MALHAS, DEFAULT_TIMEOUT
import httpx


def obter_malha(localidade: str, resolucao: str = None, formato: str = "application/vnd.geo+json", qualidade: str = None) -> Dict:
    cache_key = f"malha_localidade_{localidade}_resolucao_{resolucao}_formato_{formato}_qualidade_{qualidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_MALHAS}/{localidade}"
        params = {}
        if resolucao:
            params["resolucao"] = resolucao
        if formato:
            params["formato"] = formato
        if qualidade:
            params["qualidade"] = qualidade
        response = httpx.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        if formato == "application/vnd.geo+json" or formato == "application/json":
            resultado = response.json()
        else:
            resultado = {"conteudo": response.text, "formato": formato}
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter malha da localidade {localidade}: {e}")
        return {"erro": str(e)}


def obter_malha_por_ano(
    ano: str,
    localidade: str, 
    divisao: str = None,
    subdivisao: str = None,
    resolucao: str = None, 
    formato: str = "application/vnd.geo+json", 
    qualidade: str = None
) -> Dict:
    cache_key = f"malha_ano_{ano}_localidade_{localidade}_divisao_{divisao}_subdivisao_{subdivisao}_resolucao_{resolucao}_formato_{formato}_qualidade_{qualidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    try:
        url = f"{BASE_URL_MALHAS}/{ano}/{localidade}"
        params = {}
        if divisao:
            params["divisao"] = divisao
        if subdivisao:
            params["subdivisao"] = subdivisao
        if resolucao:
            params["resolucao"] = resolucao
        if formato:
            params["formato"] = formato
        if qualidade:
            params["qualidade"] = qualidade
        response = httpx.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        if formato == "application/vnd.geo+json" or formato == "application/json":
            resultado = response.json()
        else:
            resultado = {"conteudo": response.text, "formato": formato}
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter malha do ano {ano}, localidade {localidade}: {e}")
        return {"erro": str(e)}
