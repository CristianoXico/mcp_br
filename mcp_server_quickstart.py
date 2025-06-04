#!/usr/bin/env python
"""
Servidor MCP (Model Context Protocol) para o projeto MCP-BR.
Implementação seguindo o guia de início rápido oficial.
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading
import functools

from mcp.server import Server
from mcp import Tool, Resource
from mcp import stdio_server
from collections import Counter
import os

# Importando as funções do projeto
from tools.relatorio_localidade import gerar_relatorio_completo, exibir_relatorio_texto
from tools.busca_localidade import (
    buscar_info_localidade, 
    buscar_dados_demograficos,
    buscar_dados_socioeconomicos
)
from tools.vulnerabilidade_social import obter_vulnerabilidade_social

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/mcp_server.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mcp-br-server")

# Definindo as ferramentas (tools)
tools = [
    Tool(
        name="buscar_localidade",
        description="Busca localidades brasileiras (estados, municípios, etc.) pelo nome",
        inputSchema={
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome da localidade a ser buscada"
                },
                "tipo": {
                    "type": "string",
                    "description": "Tipo de localidade (municipio, estado, regiao)",
                    "enum": ["municipio", "estado", "regiao"]
                }
            },
            "required": ["nome"]
        }
    ),
    Tool(
        name="vulnerabilidade_social",
        description="Obtém indicadores de vulnerabilidade social para um município brasileiro",
        inputSchema={
            "type": "object",
            "properties": {
                "municipio": {
                    "type": "string",
                    "description": "Nome do município"
                },
                "ano": {
                    "type": "integer",
                    "description": "Ano de referência dos dados",
                    "default": 2023
                }
            },
            "required": ["municipio"]
        }
    ),
    Tool(
        name="relatorio_localidade",
        description="Gera um relatório completo sobre uma localidade brasileira",
        inputSchema={
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome da localidade"
                },
                "tipo": {
                    "type": "string",
                    "description": "Tipo de localidade (municipio, estado, regiao)",
                    "enum": ["municipio", "estado", "regiao"],
                    "default": "municipio"
                },
                "formato": {
                    "type": "string",
                    "description": "Formato do relatório",
                    "enum": ["texto", "json"],
                    "default": "texto"
                }
            },
            "required": ["nome"]
        }
    )
]

# Definindo os recursos (resources)
resources = [
    Resource(
        name="guia_uso",
        uri="resource://guia_uso",
        description="Guia de uso do MCP-BR",
        mimeType="text/markdown"
    ),
    Resource(
        name="exemplos",
        uri="resource://exemplos",
        description="Exemplos de uso do MCP-BR",
        mimeType="text/markdown"
    ),
    Resource(
        name="guia_llm",
        uri="resource://guia_llm",
        description="Guia de uso do MCP-BR para LLMs",
        mimeType="text/markdown"
    ),
    Resource(
        name="faq",
        uri="resource://faq",
        description="Perguntas frequentes sobre o MCP-BR",
        mimeType="text/markdown"
    ),
    Resource(
        name="usage_report",
        uri="resource://usage_report",
        description="Relatório de uso das ferramentas MCP-BR",
        mimeType="text/plain"
    )
]

# Conteúdo dos recursos
def generate_usage_report():
    return f"Relatório de uso gerado em {datetime.now()}\n{dict(tool_usage_counter)}"

recursos_conteudo = {
    "resource://guia_uso": """
# Guia de Uso do MCP-BR

O MCP-BR é um servidor que fornece acesso a dados sobre localidades brasileiras, incluindo informações demográficas, socioeconômicas e indicadores de vulnerabilidade social.
""",
    "resource://exemplos": """
# Exemplos de Uso do MCP-BR

- Buscar município: {\"nome\": \"São Paulo\"}
- Gerar relatório: {\"municipio\": \"São José do Rio Preto\", \"formato\": \"texto\"}
""",
    "resource://guia_llm": open(os.path.join("docs", "guia_llm.md"), encoding="utf-8").read() if os.path.exists(os.path.join("docs", "guia_llm.md")) else "Guia LLM não encontrado.",
    "resource://faq": open(os.path.join("docs", "faq.md"), encoding="utf-8").read() if os.path.exists(os.path.join("docs", "faq.md")) else "FAQ não encontrado.",
    "resource://usage_report": generate_usage_report,
    "resource://exemplos_llm": open(os.path.join("docs", "exemplos_llm.md"), encoding="utf-8").read() if os.path.exists(os.path.join("docs", "exemplos_llm.md")) else "Exemplos avançados não encontrados."
}

server = Server(
    name="MCP-BR Server",
    version="1.0.0",
    instructions="Servidor MCP para dados sobre localidades brasileiras"
)


# Monitoramento simples de uso de ferramentas
tool_usage_counter = Counter()

# Definindo os handlers para o servidor MCP
class McpBrServer:
    def __init__(self, server):
        self.server = server
        self.setup_handlers()
        
    def setup_handlers(self):
        # Registrar os handlers para as ferramentas
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        self.server.list_resources = self.list_resources
        self.server.read_resource = self.read_resource
        # Registrando handlers com cache/rate/fallback
        server.register_tool_handler("buscar_municipio", cache_and_rate_limit(tool_cache, 'tool')(buscar_municipio_handler))
        server.register_tool_handler("calcular", cache_and_rate_limit(tool_cache, 'tool')(calcular_handler))
        server.register_tool_handler("gerar_relatorio", cache_and_rate_limit(tool_cache, 'tool')(gerar_relatorio_handler))
        server.register_resource_handler(read_resource_handler)
    
    async def list_tools(self):
        logger.info("Listando ferramentas disponíveis")
        return tools
    
    async def call_tool(self, name, params):
        logger.info(f"Chamando ferramenta: {name}")
        handler = {
            "buscar_municipio": cache_and_rate_limit(tool_cache, 'tool')(buscar_municipio_handler),
            "calcular": cache_and_rate_limit(tool_cache, 'tool')(calcular_handler),
            "gerar_relatorio": cache_and_rate_limit(tool_cache, 'tool')(gerar_relatorio_handler)
        }.get(name)
        if handler:
            return await handler(params)
        logger.warning(f"Handler não encontrado para ferramenta: {name}")
        return {"erro": f"Ferramenta '{name}' não encontrada."}
    
    async def list_resources(self):
        logger.info("Listando recursos disponíveis")
        return resources
    
    async def read_resource(self, uri):
        logger.info(f"Lendo recurso: {uri}")
        content = recursos_conteudo.get(uri)
        if content:
            return {"content": content}
        logger.warning(f"Recurso '{uri}' não encontrado.")
        return {"erro": f"Recurso '{uri}' não encontrado."}
                
    async def call_tool(self, name, parameters):
        logger.info(f"Chamando ferramenta: {name} com parâmetros: {parameters}")
        
        try:
            if name == "buscar_localidade":
                nome = parameters.get("nome")
                tipo = parameters.get("tipo", "municipio")
                
                if not nome:
                    return {"error": "Parâmetro 'nome' é obrigatório"}
                
                resultados = await buscar_info_localidade(nome, tipo)
                return {
                    "result": {
                        "content": resultados,
                        "content_type": "application/json"
                    }
                }
                
            elif name == "vulnerabilidade_social":
                municipio = parameters.get("municipio")
                ano = parameters.get("ano", 2023)
                
                if not municipio:
                    return {"error": "Parâmetro 'municipio' é obrigatório"}
                
                resultados = await obter_vulnerabilidade_social(municipio, ano)
                return {
                    "result": {
                        "content": resultados,
                        "content_type": "application/json"
                    }
                }
                
            elif name == "relatorio_localidade":
                nome = parameters.get("nome")
                tipo = parameters.get("tipo", "municipio")
                formato = parameters.get("formato", "texto")
                
                if not nome:
                    return {"error": "Parâmetro 'nome' é obrigatório"}
                
                relatorio = await gerar_relatorio_completo(nome, tipo)
                
                if formato.lower() == "json":
                    return {
                        "result": {
                            "content": relatorio,
                            "content_type": "application/json"
                        }
                    }
                else:
                    texto_relatorio = exibir_relatorio_texto(relatorio)
                    return {
                        "result": {
                            "content": texto_relatorio,
                            "content_type": "text/plain"
                        }
                    }
                    
            else:
                return {"error": f"Ferramenta '{name}' não encontrada"}
                
        except Exception as e:
            logger.error(f"Erro ao executar ferramenta {name}: {e}")
            return {"error": str(e)}
    
    async def list_resources(self):
        logger.info("Listando recursos disponíveis")
        return {"resources": resources}
    
    async def read_resource(self, uri):
        logger.info(f"Lendo recurso: {uri}")
        
        try:
            if uri in recursos_conteudo:
                content = recursos_conteudo[uri]
                return {
                    "contents": {
                        "content": content,
                        "content_type": "text/markdown"
                    }
                }
            else:
                return {"error": f"Recurso '{uri}' não encontrado"}
                
        except Exception as e:
            logger.error(f"Erro ao ler recurso {uri}: {e}")
            return {"error": str(e)}

# Handler de geração de relatório
async def gerar_relatorio_handler(params):
    logger = logging.getLogger("mcp-br.gerar_relatorio")
    municipio = params.get("municipio")
    formato = params.get("formato", "texto")
    tool_usage_counter["gerar_relatorio"] += 1

    if not municipio or not isinstance(municipio, str):
        logger.warning(f"Parâmetro inválido: municipio={municipio}")
        return {"erro": "Parâmetro obrigatório 'municipio' ausente ou inválido."}
    try:
        # Simulação de geração de relatório real
        relatorio = f"Relatório de vulnerabilidade social para {municipio} (formato: {formato})."
        logger.info(f"Relatório gerado para {municipio} no formato {formato}")
        return {"relatorio": relatorio, "municipio": municipio, "formato": formato}
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}", exc_info=True)
        return {"erro": f"Erro interno ao gerar relatório para '{municipio}'."}

# --- CACHE DE RESULTADOS E RATE LIMITING ---
resource_cache = {}
tool_cache = {}
rate_limits = {
    'resource': {'limit': 10, 'interval': 60, 'calls': []}, # 10 chamadas/minuto
    'tool': {'limit': 15, 'interval': 60, 'calls': []},     # 15 chamadas/minuto
}
cache_lock = threading.Lock()

# Decorator para cache e rate limit
def cache_and_rate_limit(cache, rate_key):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            with cache_lock:
                # Rate limiting
                calls = rate_limits[rate_key]['calls']
                calls[:] = [t for t in calls if now-t < rate_limits[rate_key]['interval']]
                if len(calls) >= rate_limits[rate_key]['limit']:
                    logger.warning(f"Rate limit excedido para {rate_key}")
                    return {"erro": f"Limite de chamadas excedido para {rate_key}. Aguarde e tente novamente."}
                # Cache
                if key in cache:
                    logger.info(f"Cache hit para {rate_key}: {key}")
                    return cache[key]
                calls.append(now)
            # Fallback/robustez: tenta executar, senão retorna erro amigável
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Erro ao executar {func.__name__}: {e}")
                return {"erro": f"Erro interno ao processar {rate_key}. Por favor, tente novamente mais tarde."}
            with cache_lock:
                cache[key] = result
            return result
        return wrapper
    return decorator

# Handler de leitura de recursos
@cache_and_rate_limit(resource_cache, 'resource')
async def read_resource_handler(uri):
    logger = logging.getLogger("mcp-br.read_resource")
    content = recursos_conteudo.get(uri)
    if callable(content):
        content = content()
    if content:
        logger.info(f"Recurso '{uri}' lido com sucesso.")
        return {"content": content}
    logger.warning(f"Recurso '{uri}' não encontrado.")
    return {"erro": f"Recurso '{uri}' não encontrado."}

async def main():
    logger.info("Iniciando o servidor MCP-BR via stdio.")
    async with stdio_server() as (read_stream, write_stream):
        try:
            await server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=server.create_initialization_options()
            )
        finally:
            # Exemplo de relatório de uso ao encerrar
            logger.info(f"Uso das ferramentas durante a sessão: {dict(tool_usage_counter)}")

if __name__ == "__main__":
    asyncio.run(main())
