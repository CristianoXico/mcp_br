"""
Handlers MCP para operações com o domínio Censos do IBGE.
Importa funções utilitárias de ibge_censos_api.py e implementa lógica adicional se necessário.
"""

from typing import Dict
from .ibge_censos_api import (
    obter_area_territorial,
    obter_populacao,
    calcular_densidade_demografica,
    obter_indicadores_demograficos,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "obter_area_territorial",
    "obter_populacao",
    "calcular_densidade_demografica",
    "obter_indicadores_demograficos",
]
