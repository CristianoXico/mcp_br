"""
Utilitários de cache para uso em handlers e APIs do MCP-BR.
- Carregamento e salvamento de cache em JSON
- Funções auxiliares para cache em memória e arquivo
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional
import threading

_CACHE_LOCK = threading.Lock()
_CACHE_MEM = {}

CACHE_FILE = Path("data/cache_mcp_br.json")
CACHE_FILE.parent.mkdir(exist_ok=True)

def get_cached_data(key: str) -> Optional[Any]:
    with _CACHE_LOCK:
        if not _CACHE_MEM and CACHE_FILE.exists():
            try:
                _CACHE_MEM.update(json.loads(CACHE_FILE.read_text(encoding='utf-8')))
            except Exception:
                pass
        return _CACHE_MEM.get(key)

def save_to_cache(key: str, value: Any) -> Any:
    with _CACHE_LOCK:
        _CACHE_MEM[key] = value
        try:
            CACHE_FILE.write_text(json.dumps(_CACHE_MEM, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass
        return value

def clear_cache():
    with _CACHE_LOCK:
        _CACHE_MEM.clear()
        try:
            CACHE_FILE.unlink(missing_ok=True)
        except Exception:
            pass
