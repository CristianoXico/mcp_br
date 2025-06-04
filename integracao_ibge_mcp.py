"""
Integração das APIs do IBGE com o servidor MCP-BR
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importa as APIs do IBGE
from tools.ibge_localidades import *
from tools.ibge_agregados import *
from tools.ibge_malhas import *
from tools.ibge_metadados import *
from tools.ibge_cnae import *
from tools.ibge_nomes import *
from tools.ibge_censos import *

# Importa a biblioteca MCP
try:
    from mcp import Tool, Resource, Server, InputSchema
except ImportError:
    logger.error("Biblioteca MCP não encontrada. Instale-a com 'pip install mcp'")
    raise

# Esquemas de entrada para as ferramentas
SCHEMA_LOCALIDADE = InputSchema({
    "type": "object",
    "properties": {
        "codigo": {"type": "string", "description": "Código da localidade (município, UF, região, etc.)"}
    },
    "required": ["codigo"]
})

SCHEMA_NOME = InputSchema({
    "type": "object",
    "properties": {
        "nome": {"type": "string", "description": "Nome a ser pesquisado"}
    },
    "required": ["nome"]
})

SCHEMA_RANKING_NOMES = InputSchema({
    "type": "object",
    "properties": {
        "localidade": {"type": "string", "description": "Código da localidade (BR, UF, etc.)"},
        "sexo": {"type": "string", "description": "Filtro por sexo (M ou F)"},
        "decada": {"type": "string", "description": "Filtro por década (1930, 1940, etc.)"}
    }
})

SCHEMA_AGREGADO = InputSchema({
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "ID do agregado"}
    },
    "required": ["id"]
})

SCHEMA_CONSULTA_AGREGADO = InputSchema({
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "ID do agregado"},
        "variaveis": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs das variáveis"},
        "localidades": {"type": "array", "items": {"type": "string"}, "description": "Lista de IDs das localidades"},
        "classificacoes": {"type": "object", "description": "Classificações para filtrar os dados"}
    },
    "required": ["id", "variaveis"]
})

SCHEMA_MALHA = InputSchema({
    "type": "object",
    "properties": {
        "localidade": {"type": "string", "description": "Código da localidade"},
        "resolucao": {"type": "string", "description": "Resolução da malha (baixa, media, alta)"},
        "formato": {"type": "string", "description": "Formato da malha (geojson, topojson, svg)"},
        "qualidade": {"type": "string", "description": "Qualidade da malha (minima, intermediaria, maxima)"}
    },
    "required": ["localidade"]
})

SCHEMA_MALHA_ANO = InputSchema({
    "type": "object",
    "properties": {
        "ano": {"type": "string", "description": "Ano da malha"},
        "localidade": {"type": "string", "description": "Código da localidade"},
        "resolucao": {"type": "string", "description": "Resolução da malha (baixa, media, alta)"},
        "formato": {"type": "string", "description": "Formato da malha (geojson, topojson, svg)"},
        "qualidade": {"type": "string", "description": "Qualidade da malha (minima, intermediaria, maxima)"}
    },
    "required": ["ano", "localidade"]
})

SCHEMA_PESQUISA = InputSchema({
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "ID da pesquisa"}
    },
    "required": ["id"]
})

SCHEMA_CNAE = InputSchema({
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": "ID do item CNAE"}
    },
    "required": ["id"]
})

SCHEMA_PESQUISA_CNAE = InputSchema({
    "type": "object",
    "properties": {
        "termo": {"type": "string", "description": "Termo a ser pesquisado"}
    },
    "required": ["termo"]
})

# Definição das ferramentas do MCP
class FerramentasIBGE:
    """Classe com as ferramentas do IBGE para o servidor MCP"""
    
    @staticmethod
    def criar_ferramentas() -> List[Tool]:
        """Cria e retorna a lista de ferramentas do IBGE para o servidor MCP"""
        ferramentas = []
        
        # Ferramentas de Localidades
        ferramentas.extend([
            Tool(
                name="ibge_listar_regioes",
                description="Lista todas as regiões do Brasil",
                handler=lambda _: listar_regioes()
            ),
            Tool(
                name="ibge_listar_estados",
                description="Lista todos os estados do Brasil",
                handler=lambda _: listar_estados()
            ),
            Tool(
                name="ibge_listar_municipios",
                description="Lista todos os municípios do Brasil",
                handler=lambda _: listar_municipios()
            ),
            Tool(
                name="ibge_buscar_municipio_por_codigo",
                description="Busca um município pelo seu código IBGE",
                input_schema=SCHEMA_LOCALIDADE,
                handler=lambda params: buscar_municipio_por_codigo(params["codigo"])
            ),
            Tool(
                name="ibge_buscar_municipio_por_nome",
                description="Busca um município pelo seu nome",
                input_schema=SCHEMA_NOME,
                handler=lambda params: buscar_municipio_por_nome(params["nome"])
            ),
            Tool(
                name="ibge_buscar_area_territorial",
                description="Busca a área territorial de um município",
                input_schema=SCHEMA_LOCALIDADE,
                handler=lambda params: buscar_area_territorial(params["codigo"])
            )
        ])
        
        # Ferramentas de Agregados
        ferramentas.extend([
            Tool(
                name="ibge_listar_agregados",
                description="Lista todos os agregados disponíveis",
                handler=lambda _: listar_agregados()
            ),
            Tool(
                name="ibge_obter_agregado_por_id",
                description="Obtém detalhes de um agregado pelo seu ID",
                input_schema=SCHEMA_AGREGADO,
                handler=lambda params: obter_agregado_por_id(params["id"])
            ),
            Tool(
                name="ibge_consultar_agregado",
                description="Consulta dados de um agregado",
                input_schema=SCHEMA_CONSULTA_AGREGADO,
                handler=lambda params: consultar_agregado(
                    id_agregado=params["id"],
                    variaveis=params["variaveis"],
                    localidades=params.get("localidades"),
                    classificacoes=params.get("classificacoes")
                )
            )
        ])
        
        # Ferramentas de Malhas
        ferramentas.extend([
            Tool(
                name="ibge_obter_malha",
                description="Obtém a malha territorial de uma localidade",
                input_schema=SCHEMA_MALHA,
                handler=lambda params: obter_malha(
                    localidade=params["localidade"],
                    resolucao=params.get("resolucao"),
                    formato=params.get("formato"),
                    qualidade=params.get("qualidade")
                )
            ),
            Tool(
                name="ibge_obter_malha_por_ano",
                description="Obtém a malha territorial de uma localidade por ano",
                input_schema=SCHEMA_MALHA_ANO,
                handler=lambda params: obter_malha_por_ano(
                    ano=params["ano"],
                    localidade=params["localidade"],
                    resolucao=params.get("resolucao"),
                    formato=params.get("formato"),
                    qualidade=params.get("qualidade")
                )
            )
        ])
        
        return ferramentas
