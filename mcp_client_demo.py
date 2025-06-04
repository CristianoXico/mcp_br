"""
Demonstração de cliente MCP para interagir com o servidor MCP-BR.

Este script demonstra como usar o cliente MCP para se conectar ao servidor MCP-BR
e utilizar suas ferramentas e recursos.
"""

import asyncio
import logging
from typing import Dict, Any, List

from mcp import stdio_client

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-br-client")

async def main():
    """Função principal para demonstrar o uso do cliente MCP."""
    # Criando o cliente MCP
    logger.info("Iniciando o cliente MCP...")
    
    # Configurando o servidor para o cliente stdio
    server_params = {
        "command": ["python", "mcp_server.py"],
        "cwd": None  # Usar o diretório atual
    }
    
    try:
        # Conectando ao servidor usando stdio_client
        logger.info("Conectando ao servidor MCP-BR...")
        async with stdio_client(server=server_params) as client:
            # Listando as ferramentas disponíveis
            logger.info("Listando ferramentas disponíveis:")
            tools_response = await client.send_request("tools/list", {})
            tools = tools_response.get("tools", [])
            for tool in tools:
                logger.info(f"- {tool['name']}: {tool['description']}")
            
            # Listando os recursos disponíveis
            logger.info("Listando recursos disponíveis:")
            resources_response = await client.send_request("resources/list", {})
            resources = resources_response.get("resources", [])
            for resource in resources:
                logger.info(f"- {resource['name']}: {resource['description']}")
            
            # Exemplo de uso da ferramenta buscar_localidade
            logger.info("Buscando localidade 'São Paulo'...")
            localidade_params = {
                "name": "buscar_localidade",
                "parameters": {"nome": "São Paulo"}
            }
            localidade_result = await client.send_request("tools/call", localidade_params)
            logger.info(f"Resultado da busca de localidade: {localidade_result.get('result', {}).get('content')}")
            
            # Exemplo de uso da ferramenta gerar_relatorio
            logger.info("Gerando relatório para 'São Paulo'...")
            relatorio_params = {
                "name": "gerar_relatorio",
                "parameters": {"nome_localidade": "São Paulo", "formato": "texto"}
            }
            relatorio_result = await client.send_request("tools/call", relatorio_params)
            
            # Exibindo um trecho do relatório (primeiras 10 linhas)
            relatorio_texto = relatorio_result.get('result', {}).get('content', '')
            if isinstance(relatorio_texto, str):
                linhas = relatorio_texto.split("\n")
                logger.info("Trecho do relatório:")
                for i, linha in enumerate(linhas[:10]):
                    logger.info(linha)
                logger.info(f"... (total de {len(linhas)} linhas)")
            
            # Lendo um recurso
            logger.info("Lendo o recurso 'Sobre o MCP-BR'...")
            sobre_params = {
                "uri": "file://docs/sobre.md"
            }
            sobre_resource = await client.send_request("resources/read", sobre_params)
            logger.info(f"Conteúdo do recurso (primeiras 5 linhas):")
            resource_content = sobre_resource.get('contents', {}).get('content', '')
            if isinstance(resource_content, str):
                linhas = resource_content.split("\n")
                for linha in linhas[:5]:
                    logger.info(linha)
                logger.info("...")
    
    except Exception as e:
        logger.error(f"Erro ao usar o cliente MCP: {e}")

if __name__ == "__main__":
    asyncio.run(main())
