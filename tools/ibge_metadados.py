"""
Façade do domínio Metadados Estatísticos do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Metadados Estatísticos.

- Funções utilitárias de acesso à API: ibge_metadados_api.py
- Handlers MCP: ibge_metadados_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_metadados_handlers.py.
"""

from .ibge_metadados_handlers import *
