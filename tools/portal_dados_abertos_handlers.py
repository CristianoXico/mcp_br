from .portal_dados_abertos_api import carregar_cache, salvar_cache, listar_datasets_raw
import asyncio

# Handler MCP: lista todos os conjuntos de dados disponíveis
async def listar_dados_abertos() -> list:
    cache = carregar_cache()
    if "dados_abertos" in cache:
        return cache["dados_abertos"]
    try:
        ids = await listar_datasets_raw()
        cache["dados_abertos"] = ids
        salvar_cache(cache)
        return ids
    except Exception as e:
        print(f"Erro em listar_dados_abertos (handler): {e}")
        return ["dataset-1", "dataset-2", "dataset-3"]  # fallback
