"""
Façade do domínio Calendário do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Calendário.

- Funções utilitárias de acesso à API: ibge_calendario_api.py
- Handlers MCP: ibge_calendario_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_calendario_handlers.py.
"""

from .ibge_calendario_handlers import *

# O bloco abaixo estava fora de função/classe e causava erro de indentação.
# Se for uma função utilitária, deve estar dentro de uma função. Caso contrário, manter comentado.

# try:
#     url = f"{BASE_URL_CALENDARIO}/eventos/produtos/{id_produto}"
#     # Parâmetros da consulta
#     params = {}
#     if data_inicio:
#         params["data"] = data_inicio
#         if data_fim:
#             params["data"] += f",{data_fim}"
#     # Faz a requisição
#     eventos = make_request(url, params)
#     return save_to_cache(cache_key, eventos)
# try:
#     url = f"{BASE_URL_CALENDARIO}/eventos/tipos"
#     tipos = make_request(url)
#     return save_to_cache(cache_key, tipos)
# except Exception as e:
#     logger.error(f"Erro ao listar tipos de eventos: {e}")
#     return []
