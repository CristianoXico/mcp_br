import httpx
import json
from pathlib import Path
from typing import Dict, Any, List
from config.api_config import API_CONFIG

HEADERS = {
    "Authorization": f"Bearer {API_CONFIG['dados_abertos_token']}",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-CKAN-API-Key": API_CONFIG['dados_abertos_token'],
    "Cookie": f"auth_tkt={API_CONFIG['dados_abertos_token']}"
}


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CACHE_PATH = DATA_DIR / "cache_dados_abertos.json"

# Pool de conexões HTTP (httpx.AsyncClient)
_async_client = None


async def get_async_client():
    global _async_client
    if _async_client is None:
        _async_client = httpx.AsyncClient(timeout=30.0)
    return _async_client


def carregar_cache() -> Dict:
    try:
        if CACHE_PATH.exists():
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        return {}
    except Exception as e:
        print(f"Erro ao carregar cache: {e}")
        return {}


def salvar_cache(data: Dict) -> None:
    try:
        CACHE_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as e:
        print(f"Erro ao salvar cache: {e}")


async def api_get(url: str, **kwargs) -> httpx.Response:
    client = await get_async_client()
    return await client.get(url, headers=HEADERS, **kwargs)


# Exemplo de função utilitária para listar pacotes
async def listar_datasets_raw() -> List[str]:
    url = "https://dados.gov.br/api/3/action/package_list"
    response = await api_get(url, follow_redirects=True)
    response.raise_for_status()
    data = response.json()
    return data.get("result", [])

