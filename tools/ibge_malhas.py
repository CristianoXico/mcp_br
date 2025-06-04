"""
Façade do domínio Malhas do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Malhas.

- Funções utilitárias de acesso à API: ibge_malhas_api.py
- Handlers MCP: ibge_malhas_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_malhas_handlers.py.
"""

from .ibge_malhas_handlers import *
