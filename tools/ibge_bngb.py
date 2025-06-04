"""
Façade do domínio BNGB (Banco de Nomes Geográficos do Brasil) do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio BNGB.

- Funções utilitárias de acesso à API: ibge_bngb_api.py
- Handlers MCP: ibge_bngb_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_bngb_handlers.py.
"""

from .ibge_bngb_handlers import *
