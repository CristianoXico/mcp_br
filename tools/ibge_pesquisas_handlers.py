"""
Handlers MCP para Pesquisas do IBGE
Reexporta as funções utilitárias do módulo API, pronto para lógica MCP futura.
"""

from .ibge_pesquisas_api import (
    listar_pesquisas,
    obter_pesquisa,
    listar_periodos_pesquisa,
    obter_periodo_pesquisa,
    listar_resultados_pesquisa,
    obter_resultado_pesquisa,
    listar_indicadores_pesquisa,
    obter_indicador_pesquisa,
)
