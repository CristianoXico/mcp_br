"""
Handlers MCP para operações com o Banco de Nomes Geográficos do Brasil (BNGB) do IBGE.
Importa funções utilitárias de ibge_bngb_api.py e implementa lógica adicional se necessário.
"""

from typing import List, Dict
from .ibge_bngb_api import (
    pesquisar_nomes_geograficos,
    obter_nome_geografico,
    listar_tipos_nomes_geograficos,
    listar_nomes_geograficos_por_tipo,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "pesquisar_nomes_geograficos",
    "obter_nome_geografico",
    "listar_tipos_nomes_geograficos",
    "listar_nomes_geograficos_por_tipo",
]
