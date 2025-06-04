"""
Handlers MCP para operações com a API de Notícias do IBGE.
Importa funções utilitárias de ibge_noticias_api.py e implementa lógica adicional se necessário.
"""

from .ibge_noticias_api import *

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_noticias",
    "obter_noticia",
    "listar_noticias_por_tipo",
    "listar_noticias_por_produto",
    "pesquisar_noticias",
    "listar_tipos_noticias",
]
