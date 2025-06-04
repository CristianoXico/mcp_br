"""
Handlers MCP para operações com a API de Localidades do IBGE.
Importa funções utilitárias de ibge_localidades_api.py e implementa lógica adicional se necessário.
"""

from typing import List, Dict
from .ibge_localidades_api import (
    listar_regioes,
    listar_estados,
    listar_mesorregioes,
    listar_microrregioes,
    listar_municipios,
    buscar_municipio_por_codigo,
    buscar_municipio_por_nome,
    listar_distritos,
    listar_subdistritos,
    buscar_area_territorial,
)

# Aqui podem ser implementados handlers MCP customizados, se necessário.
# Por enquanto, apenas reexportamos as funções utilitárias para manter o padrão.

__all__ = [
    "listar_regioes",
    "listar_estados",
    "listar_mesorregioes",
    "listar_microrregioes",
    "listar_municipios",
    "buscar_municipio_por_codigo",
    "buscar_municipio_por_nome",
    "listar_distritos",
    "listar_subdistritos",
    "buscar_area_territorial",
]
