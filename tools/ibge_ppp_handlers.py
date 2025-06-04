"""
Handlers MCP para IBGE-PPP
Reexporta as funções utilitárias do módulo API, pronto para lógica MCP futura.
"""

from .ibge_ppp_api import (
    listar_processamentos,
    obter_processamento,
    listar_processamentos_por_status,
    listar_processamentos_por_usuario,
    listar_status_processamentos,
    obter_resultado_processamento,
)
