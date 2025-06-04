"""
Funções utilitárias para acesso à API de Nomes do IBGE (requisições HTTP, pooling, cache, autenticação).
"""
from typing import Dict, List, Optional
from .api_config import BASE_URL_NOMES
from .cache_utils import get_cached_data, save_to_cache
from .logger import get_logger
import requests

logger = get_logger("ibge_nomes_api")

def api_get_nomes(path: str, params: Optional[dict] = None) -> dict:
    url = f"{BASE_URL_NOMES}/{path}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
