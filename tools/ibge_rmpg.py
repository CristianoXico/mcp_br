"""
Façade do domínio RMPG do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio RMPG.

- Funções utilitárias de acesso à API: ibge_rmpg_api.py
- Handlers MCP: ibge_rmpg_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_rmpg_handlers.py.
"""

from .ibge_rmpg_handlers import *
