"""
Façade do domínio Publicações do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Publicações.

- Funções utilitárias de acesso à API: ibge_publicacoes_api.py
- Handlers MCP: ibge_publicacoes_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_publicacoes_handlers.py.
"""

from .ibge_publicacoes_handlers import *
