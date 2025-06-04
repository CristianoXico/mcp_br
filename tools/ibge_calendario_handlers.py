"""
Handlers MCP para operações com o Calendário do IBGE.
Importa funções utilitárias de ibge_calendario_api.py e implementa lógica adicional se necessário.
"""

from typing import List, Dict
from .ibge_calendario_api import (
    listar_eventos,
    obter_evento,
    listar_eventos_por_tipo,
    listar_eventos_por_produto,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_eventos",
    "obter_evento",
    "listar_eventos_por_tipo",
    "listar_eventos_por_produto",
]
