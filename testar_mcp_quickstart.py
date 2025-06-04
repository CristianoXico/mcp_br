#!/usr/bin/env python
"""
Script para testar o servidor MCP-BR simplificado.
Este script se conecta ao servidor MCP-BR e testa suas funcionalidades.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, List, Any, Optional

import httpx

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-br-tester")

class McpClient:
    """Cliente para o servidor MCP."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """Inicializa o cliente MCP.
        
        Args:
            server_url: URL do servidor MCP
        """
        self.server_url = server_url
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"Cliente MCP inicializado com URL: {server_url}")
    
    async def list_tools(self) -> Dict[str, Any]:
        """Lista as ferramentas disponíveis no servidor MCP.
        
        Returns:
            Lista de ferramentas disponíveis
        """
        try:
            response = await self.client.post(
                f"{self.server_url}/mcp/v1",
                json={
                    "jsonrpc": "2.0",
                    "method": "mcp.list_tools",
                    "params": {},
                    "id": 1
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao listar ferramentas: {str(e)}")
            return {"error": str(e)}
    
    async def list_resources(self) -> Dict[str, Any]:
        """Lista os recursos disponíveis no servidor MCP.
        
        Returns:
            Lista de recursos disponíveis
        """
        try:
            response = await self.client.post(
                f"{self.server_url}/mcp/v1",
                json={
                    "jsonrpc": "2.0",
                    "method": "mcp.list_resources",
                    "params": {},
                    "id": 2
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao listar recursos: {str(e)}")
            return {"error": str(e)}
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Chama uma ferramenta no servidor MCP.
        
        Args:
            tool_name: Nome da ferramenta
            params: Parâmetros para a ferramenta
            
        Returns:
            Resultado da chamada da ferramenta
        """
        try:
            response = await self.client.post(
                f"{self.server_url}/mcp/v1",
                json={
                    "jsonrpc": "2.0",
                    "method": "mcp.call_tool",
                    "params": {
                        "name": tool_name,
                        "parameters": params
                    },
                    "id": 3
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao chamar ferramenta {tool_name}: {str(e)}")
            return {"error": str(e)}
    
    async def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Lê um recurso do servidor MCP.
        
        Args:
            resource_uri: URI do recurso
            
        Returns:
            Conteúdo do recurso
        """
        try:
            response = await self.client.post(
                f"{self.server_url}/mcp/v1",
                json={
                    "jsonrpc": "2.0",
                    "method": "mcp.read_resource",
                    "params": {
                        "uri": resource_uri
                    },
                    "id": 4
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao ler recurso {resource_uri}: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

async def main():
    """Função principal."""
    # Inicializa o cliente MCP
    mcp_client = McpClient()
    
    try:
        # Lista as ferramentas disponíveis
        print("\n=== Listando ferramentas disponíveis ===")
        tools_response = await mcp_client.list_tools()
        if "error" in tools_response:
            print(f"Erro ao listar ferramentas: {tools_response['error']}")
        else:
            tools = tools_response.get("result", {}).get("tools", [])
            print(f"Encontradas {len(tools)} ferramentas:")
            for tool in tools:
                print(f"- {tool.get('name')}: {tool.get('description')}")
        
        # Lista os recursos disponíveis
        print("\n=== Listando recursos disponíveis ===")
        resources_response = await mcp_client.list_resources()
        if "error" in resources_response:
            print(f"Erro ao listar recursos: {resources_response['error']}")
        else:
            resources = resources_response.get("result", {}).get("resources", [])
            print(f"Encontrados {len(resources)} recursos:")
            for resource in resources:
                print(f"- {resource.get('name')}: {resource.get('description')}")
        
        # Testa a ferramenta buscar_municipio
        print("\n=== Testando a ferramenta buscar_municipio ===")
        municipio_response = await mcp_client.call_tool("buscar_municipio", {"nome": "São Paulo"})
        if "error" in municipio_response:
            print(f"Erro ao buscar município: {municipio_response['error']}")
        else:
            result = municipio_response.get("result", {})
            print(f"Resultado da busca por 'São Paulo':")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Testa a ferramenta calcular
        print("\n=== Testando a ferramenta calcular ===")
        calc_response = await mcp_client.call_tool("calcular", {"expressao": "2 + 2"})
        if "error" in calc_response:
            print(f"Erro ao calcular: {calc_response['error']}")
        else:
            result = calc_response.get("result", {})
            print(f"Resultado do cálculo '2 + 2': {result}")
        
        # Lê um recurso
        print("\n=== Lendo o recurso guia_uso ===")
        resource_response = await mcp_client.read_resource("https://mcp-br.local/docs/guia_uso")
        if "error" in resource_response:
            print(f"Erro ao ler recurso: {resource_response['error']}")
        else:
            result = resource_response.get("result", {})
            content = result.get("content", "")
            print(f"Conteúdo do recurso (primeiros 100 caracteres):")
            print(content[:100] + "..." if len(content) > 100 else content)
        
    finally:
        # Fecha o cliente MCP
        await mcp_client.close()

if __name__ == "__main__":
    # Configura o loop de eventos para Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa a função principal
    asyncio.run(main())
