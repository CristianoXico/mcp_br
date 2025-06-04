"""
Handlers MCP para IBGE-Produtos
Reexporta as funções utilitárias do módulo API, pronto para lógica MCP futura.
"""

from .ibge_produtos_api import (
    listar_produtos,
    obter_produto,
    listar_produtos_por_tipo,
    listar_produtos_por_tema,
    listar_tipos_produtos,
    obter_tipo_produto,
    listar_temas_produtos,
    obter_tema_produto,
)
