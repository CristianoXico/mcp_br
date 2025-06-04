"""
Handlers MCP para operações com a API de Metadados Estatísticos do IBGE.
Importa funções utilitárias de ibge_metadados_api.py e implementa lógica adicional se necessário.
"""

from .ibge_metadados_api import *

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_fontes",
    "listar_pesquisas",
    "listar_periodos_pesquisa",
    "obter_metadados_pesquisa_periodo",
    "listar_agregados_pesquisa_periodo",
    "obter_agregado",
    "listar_variaveis_agregado",
    "obter_variavel",
    "listar_classificacoes_agregado",
    "listar_niveis_classificacao",
    "listar_categorias_nivel",
    "obter_categoria",
    "listar_dominios",
    "listar_variaveis",
    "listar_unidades_medida",
    "listar_conceitos",
]
