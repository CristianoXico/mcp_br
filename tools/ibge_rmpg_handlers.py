"""
Handlers MCP para operações com a API RMPG do IBGE.
Importa funções utilitárias de ibge_rmpg_api.py e implementa lógica adicional se necessário.
"""

from .ibge_rmpg_api import *

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_estacoes",
    "obter_estacao",
    "listar_estacoes_por_uf",
    "listar_estacoes_por_municipio",
    "listar_estacoes_por_status",
    "listar_status_estacoes",
    "listar_dados_estacao",
    "obter_dado_estacao",
]
