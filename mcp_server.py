"""Servidor MCP (Model Context Protocol) para o projeto MCP-BR.

Este servidor expõe as funcionalidades de relatórios de localidades brasileiras
através do protocolo MCP, permitindo que modelos de linguagem interajam com os dados.
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any

from mcp.server import Server
from mcp import Tool, Resource
from mcp import stdio_server

# Importando as funções do projeto
from tools.relatorio_localidade import gerar_relatorio_completo, exibir_relatorio_texto
from tools.busca_localidade import (
    buscar_info_localidade, 
    buscar_dados_demograficos,
    buscar_dados_socioeconomicos,
    buscar_indicadores_municipais
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
                }
            },
            "required": ["nome"]
        }
    ),
    Tool(
        name="gerar_relatorio",
        description="Gera um relatório completo sobre uma localidade brasileira",
        inputSchema={
            "type": "object",
            "properties": {
                "nome_localidade": {
                    "type": "string",
                    "description": "Nome da localidade para gerar o relatório"
                },
                "formato": {
                    "type": "string",
                    "description": "Formato do relatório (texto, json)",
                    "enum": ["texto", "json"],
                    "default": "texto"
                }
            },
            "required": ["nome_localidade"]
        }
    ),
    Tool(
        name="buscar_dados_demograficos",
        description="Busca dados demográficos de uma localidade pelo código IBGE",
        inputSchema={
            "type": "object",
            "properties": {
                "codigo_ibge": {
                    "type": "string",
                    "description": "Código IBGE da localidade"
                }
            },
            "required": ["codigo_ibge"]
        }
    ),
    Tool(
        name="buscar_dados_socioeconomicos",
        description="Busca dados socioeconômicos de uma localidade pelo código IBGE",
        inputSchema={
            "type": "object",
            "properties": {
                "codigo_ibge": {
                    "type": "string",
                    "description": "Código IBGE da localidade"
                }
            },
            "required": ["codigo_ibge"]
        }
    )
]

# Definindo os recursos (resources)
resources = [
    Resource(
        uri="file://docs/sobre.md",
        name="Sobre o MCP-BR",
        description="Informações sobre o projeto MCP-BR",
        mimeType="text/markdown"
    ),
    Resource(
        uri="file://docs/exemplos.md",
        name="Exemplos de Uso",
        description="Exemplos de como usar as ferramentas do MCP-BR",
        mimeType="text/markdown"
    )
]

# Conteúdo dos recursos
recursos_conteudo = {
    "file://docs/sobre.md": """# MCP-BR

O MCP-BR é um projeto que fornece informações sobre localidades brasileiras, incluindo dados demográficos, socioeconômicos e indicadores municipais.

## Funcionalidades

- Busca de localidades por nome
- Geração de relatórios detalhados sobre localidades
- Acesso a dados demográficos e socioeconômicos
- Indicadores municipais

## Fontes de Dados

- IBGE (Instituto Brasileiro de Geografia e Estatística)
- Portal da Transparência
- Outros portais de dados abertos governamentais
""",
    
    "file://docs/exemplos.md": """# Exemplos de Uso do MCP-BR

## Buscar Localidade

```python
resultado = await buscar_localidade("São Paulo")
```

## Gerar Relatório

```python
relatorio = await gerar_relatorio("Rio de Janeiro", formato="texto")
```

## Buscar Dados Demográficos

```python
dados = await buscar_dados_demograficos("3550308")  # Código IBGE de São Paulo
```

## Buscar Dados Socioeconômicos

```python
dados = await buscar_dados_socioeconomicos("3550308")  # Código IBGE de São Paulo
```
"""
}

# Criando o servidor MCP
server = Server(
    name="MCP-BR Server",
    version="1.0.0",
    instructions="Servidor MCP para relatórios de localidades brasileiras"
)

# Implementando os handlers para o servidor MCP
class McpBrServer:
    def __init__(self, server):
        self.server = server
        self.setup_handlers()
        
    def setup_handlers(self):
        # Registrar os handlers para as ferramentas
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        
        # Registrar os handlers para os recursos
        self.server.list_resources = self.list_resources
        self.server.read_resource = self.read_resource
    
    async def list_tools(self):
        logger.info("Listando ferramentas disponíveis")
        return {"tools": tools}
    
    async def call_tool(self, name, parameters):
        logger.info(f"Chamando ferramenta: {name} com parâmetros: {parameters}")
        
        try:
            if name == "buscar_localidade":
                nome = parameters.get("nome")
                if not nome:
                    return {"error": "Parâmetro 'nome' é obrigatório"}
                
                resultados = await buscar_info_localidade(nome)
                return {
                    "result": {
                        "content": resultados,
                        "content_type": "application/json"
                    }
                }
                
            elif name == "gerar_relatorio":
                nome_localidade = parameters.get("nome_localidade")
                formato = parameters.get("formato", "texto")
                
                if not nome_localidade:
                    return {"error": "Parâmetro 'nome_localidade' é obrigatório"}
                
                relatorio = await gerar_relatorio_completo(nome_localidade)
                
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
                    
            elif name == "buscar_dados_demograficos":
                codigo_ibge = parameters.get("codigo_ibge")
                if not codigo_ibge:
                    return {"error": "Parâmetro 'codigo_ibge' é obrigatório"}
                    
                dados = await buscar_dados_demograficos(codigo_ibge)
                return {
                    "result": {
                        "content": dados,
                        "content_type": "application/json"
                    }
                }
                
            elif name == "buscar_dados_socioeconomicos":
                codigo_ibge = parameters.get("codigo_ibge")
                if not codigo_ibge:
                    return {"error": "Parâmetro 'codigo_ibge' é obrigatório"}
                    
                dados = await buscar_dados_socioeconomicos(codigo_ibge)
                return {
                    "result": {
                        "content": dados,
                        "content_type": "application/json"
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

async def main():
    """Função principal para iniciar o servidor MCP."""
    logger.info("Iniciando o servidor MCP-BR...")
    
    # Configurar o servidor MCP-BR
    mcp_br_server = McpBrServer(server)
    
    # Iniciar o servidor usando stdio
    async with stdio_server() as (read_stream, write_stream):
        try:
            # Inicializar o servidor com as opções de inicialização
            logger.info("Inicializando o servidor MCP-BR...")
            initialization_options = server.create_initialization_options()
            
            # Executar o servidor
            logger.info("Servidor MCP-BR iniciado e pronto para receber conexões")
            await server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=initialization_options
            )
            
        except KeyboardInterrupt:
            logger.info("Encerrando o servidor MCP-BR...")
        except Exception as e:
            logger.error(f"Erro no servidor MCP-BR: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(main())
