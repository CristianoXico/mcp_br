import httpx
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URLs base das APIs do IBGE
BASE_URL_LOCALIDADES = "https://servicodados.ibge.gov.br/api/v1/localidades"
BASE_URL_AGREGADOS = "https://servicodados.ibge.gov.br/api/v3/agregados"
BASE_URL_MALHAS = "https://servicodados.ibge.gov.br/api/v3/malhas"
BASE_URL_METADADOS = "https://servicodados.ibge.gov.br/api/v2/metadados-estatisticos"
BASE_URL_CNAE = "https://servicodados.ibge.gov.br/api/v2/cnae"
BASE_URL_NOMES = "https://servicodados.ibge.gov.br/api/v2/censos/nomes"
BASE_URL_CENSOS = "https://servicodados.ibge.gov.br/api/v2/censos"
# Novas APIs implementadas
BASE_URL_BDG = "https://servicodados.ibge.gov.br/api/v1/bdg"
BASE_URL_BNGB = "https://servicodados.ibge.gov.br/api/v1/bngb"
BASE_URL_CALENDARIO = "https://servicodados.ibge.gov.br/api/v1/calendario"
BASE_URL_HGEOHNOR = "https://servicodados.ibge.gov.br/api/v1/hgeohnor"
BASE_URL_NOTICIAS = "https://servicodados.ibge.gov.br/api/v1/noticias"
BASE_URL_PAISES = "https://servicodados.ibge.gov.br/api/v1/paises"
BASE_URL_PESQUISAS = "https://servicodados.ibge.gov.br/api/v1/pesquisas"
BASE_URL_PPP = "https://servicodados.ibge.gov.br/api/v1/ppp"
BASE_URL_PRODUTOS = "https://servicodados.ibge.gov.br/api/v1/produtos"
BASE_URL_PROGRID = "https://servicodados.ibge.gov.br/api/v1/progrid"
BASE_URL_PUBLICACOES = "https://servicodados.ibge.gov.br/api/v1/publicacoes"
BASE_URL_RBMC = "https://servicodados.ibge.gov.br/api/v1/rbmc"
BASE_URL_RMPG = "https://servicodados.ibge.gov.br/api/v1/rmpg"

# Timeout padrão para requisições HTTP
DEFAULT_TIMEOUT = 15.0  # segundos

def carregar_cache():
    """Carrega os dados do cache"""
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cache.json')
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def salvar_cache(cache):
    """Salva os dados no cache"""
    cache_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cache.json')
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cached_data(cache_key: str, expiry_seconds: int = 86400):
    """Obtém dados do cache se existirem e não estiverem expirados"""
    cache = carregar_cache()
    if cache_key in cache and datetime.now().timestamp() - cache.get(f"{cache_key}_timestamp", 0) < expiry_seconds:
        return cache[cache_key]
    return None

def save_to_cache(cache_key: str, data: Any):
    """Salva dados no cache com timestamp"""
    cache = carregar_cache()
    cache[cache_key] = data
    cache[f"{cache_key}_timestamp"] = datetime.now().timestamp()
    salvar_cache(cache)
    return data

def make_request(url: str, params: Dict = None):
    """Faz uma requisição HTTP com tratamento de erros e cache"""
    try:
        response = httpx.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        logger.error(f"Erro na requisição: {e}")
        raise
    except httpx.HTTPStatusError as e:
        logger.error(f"Erro HTTP {e.response.status_code}: {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise
