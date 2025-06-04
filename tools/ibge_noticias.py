"""
Façade do domínio Notícias do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Notícias.

- Funções utilitárias de acesso à API: ibge_noticias_api.py
- Handlers MCP: ibge_noticias_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_noticias_handlers.py.
"""

from .ibge_noticias_handlers import *
