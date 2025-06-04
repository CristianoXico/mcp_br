"""
Handlers MCP para Países do IBGE
Reexporta as funções utilitárias do módulo API, pronto para lógica MCP futura.
"""

from .ibge_paises_api import (
    listar_paises,
    obter_pais,
    listar_paises_por_continente,
    listar_paises_por_bloco,
    listar_continentes,
    obter_continente,
    listar_blocos,
    obter_bloco,
)
