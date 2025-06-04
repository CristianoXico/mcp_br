"""
Façade do domínio ProGrid do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio ProGrid.

- Funções utilitárias de acesso à API: ibge_progrid_api.py
- Handlers MCP: ibge_progrid_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_progrid_handlers.py.
"""

from .ibge_progrid_handlers import *
