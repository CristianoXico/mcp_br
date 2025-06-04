"""
Handlers MCP para operações com a API ProGrid do IBGE.
Importa funções utilitárias de ibge_progrid_api.py e implementa lógica adicional se necessário.
"""

from .ibge_progrid_api import *

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_celulas",
    "obter_celula",
    "listar_celulas_por_nivel",
    "listar_celulas_por_uf",
    "listar_celulas_por_municipio",
    "listar_niveis_progrid",
    "obter_nivel_progrid",
]
