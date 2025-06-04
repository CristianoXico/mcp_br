"""
Handlers MCP para operações com a API de Malhas do IBGE.
Importa funções utilitárias de ibge_malhas_api.py e implementa lógica adicional se necessário.
"""

from typing import Dict
from .ibge_malhas_api import (
    obter_malha,
    obter_malha_por_ano,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "obter_malha",
    "obter_malha_por_ano",
]
