"""
Façade do domínio Países do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Países.

- Funções utilitárias de acesso à API: ibge_paises_api.py
- Handlers MCP: ibge_paises_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_paises_handlers.py.
"""

from .ibge_paises_handlers import *
