"""
Façade do domínio RBMC do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio RBMC.

- Funções utilitárias de acesso à API: ibge_rbmc_api.py
- Handlers MCP: ibge_rbmc_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_rbmc_handlers.py.
"""

from .ibge_rbmc_handlers import *
