"""
Façade do domínio Pesquisas do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Pesquisas.

- Funções utilitárias de acesso à API: ibge_pesquisas_api.py
- Handlers MCP: ibge_pesquisas_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_pesquisas_handlers.py.
"""
from .ibge_pesquisas_handlers import *
