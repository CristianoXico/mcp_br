"""
Funções utilitárias para acesso à API de Publicações do IBGE (requisições HTTP, pooling, cache, autenticação).
"""
# -*- coding: utf-8 -*-

from typing import Dict, List, Optional
from .api_config import BASE_URL_PUBLICACOES
from .cache_utils import get_cached_data, save_to_cache
from .logger import get_logger
import requests

logger = get_logger("ibge_publicacoes_api")

def api_get_publicacoes(path: str, params: Optional[dict] = None) -> dict:
    url = f"{BASE_URL_PUBLICACOES}/{path}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
