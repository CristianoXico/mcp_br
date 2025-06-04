"""
Handlers MCP para operações com o Banco de Dados Geodésicos (BDG) do IBGE.
Importa funções utilitárias de ibge_bdg_api.py e implementa lógica adicional se necessário.
"""

from typing import List, Dict
from .ibge_bdg_api import listar_estacoes, obter_estacao, listar_estacoes_por_tipo, listar_estacoes_por_uf

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_estacoes",
    "obter_estacao",
    "listar_estacoes_por_tipo",
    "listar_estacoes_por_uf",
]
