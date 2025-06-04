"""
Módulo para acesso à API do Serviço de Posicionamento por Ponto Preciso (IBGE-PPP) do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/ppp?versao=1
"""

from .ibge_base import *

"""
Façade do domínio IBGE-PPP (Serviço de Posicionamento por Ponto Preciso).

Este módulo serve apenas como ponto de entrada padronizado para o domínio PPP.

- Funções utilitárias de acesso à API: ibge_ppp_api.py
- Handlers MCP: ibge_ppp_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_ppp_handlers.py.
"""

from .ibge_ppp_handlers import *
