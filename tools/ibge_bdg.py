"""
Façade do domínio BDG (Banco de Dados Geodésicos) do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio BDG.

- Funções utilitárias de acesso à API: ibge_bdg_api.py
- Handlers MCP: ibge_bdg_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_bdg_handlers.py.
"""

from .ibge_bdg_handlers import *
