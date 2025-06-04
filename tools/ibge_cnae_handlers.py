"""
Handlers MCP para operações com o domínio CNAE do IBGE.
Importa funções utilitárias de ibge_cnae_api.py e implementa lógica adicional se necessário.
"""

from typing import List, Dict
from .ibge_cnae_api import (
    listar_secoes,
    obter_secao,
    listar_divisoes,
    obter_divisao,
    listar_grupos,
    obter_grupo,
    listar_classes,
    obter_classe,
    listar_subclasses,
    obter_subclasse,
    pesquisar_cnae,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_secoes",
    "obter_secao",
    "listar_divisoes",
    "obter_divisao",
    "listar_grupos",
    "obter_grupo",
    "listar_classes",
    "obter_classe",
    "listar_subclasses",
    "obter_subclasse",
    "pesquisar_cnae",
]
