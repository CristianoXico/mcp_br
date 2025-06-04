"""
Handlers MCP para operações com a API RBMC do IBGE.
Importa funções utilitárias de ibge_rbmc_api.py e implementa lógica adicional se necessário.
"""

from .ibge_rbmc_api import *

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_estacoes",
    "obter_estacao",
    "listar_estacoes_por_uf",
    "listar_estacoes_por_municipio",
    "listar_estacoes_por_tipo",
    "listar_tipos_estacoes",
    "listar_arquivos_estacao",
    "obter_arquivo_estacao",
]
