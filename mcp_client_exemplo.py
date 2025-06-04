"""Cliente MCP de exemplo para testar o servidor MCP-BR.

Este script demonstra como conectar-se ao servidor MCP-BR e utilizar suas funcionalidades.
"""

import asyncio
import json
import logging
import subprocess
import sys
from typing import Dict, Any, Optional, List, Tuple

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-br-client")

class McpBrClient:
    """Cliente simples para o servidor MCP-BR usando JSON-RPC diretamente."""
    
    def __init__(self):
        """Inicializa o cliente MCP-BR."""
        self.server_process = None
        self.request_id = 0
    
    async def connect(self):
        """Inicia o servidor MCP-BR como um subprocesso."""
        logger.info("Iniciando o servidor MCP-BR...")
        self.server_process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        logger.info("Servidor MCP-BR iniciado")
    
    async def disconnect(self):
        """Encerra o processo do servidor MCP-BR."""
        logger.info("Desconectando do servidor MCP-BR...")
        
        if self.server_process:
            logger.info("Encerrando processo do servidor...")
            self.server_process.terminate()
            await asyncio.sleep(0.5)
            if self.server_process.poll() is None:
                logger.warning("Servidor não encerrou normalmente, forçando encerramento...")
                self.server_process.kill()
            logger.info("Processo do servidor encerrado")
    
    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Envia uma requisição JSON-RPC para o servidor MCP-BR.
        
        Args:
            method: Método a ser chamado.
            params: Parâmetros para o método.
        
        Returns:
            A resposta do servidor.
        """
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        
        # Enviar a requisição
        request_str = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_str.encode())
        self.server_process.stdin.flush()
        
        # Ler a resposta
        response_str = self.server_process.stdout.readline().decode().strip()
        response = json.loads(response_str)
        
        # Verificar se há erro
        if "error" in response:
            error = response["error"]
            logger.error(f"Erro na requisição: {error}")
            raise Exception(f"Erro na requisição: {error}")
        
        return response["result"]
    
    async def initialize(self) -> Dict[str, Any]:
        """Inicializa a conexão com o servidor MCP-BR."""
        logger.info("Inicializando conexão com o servidor MCP-BR...")
        return await self._send_request("initialize", {
            "capabilities": {}
        })
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Lista as ferramentas disponíveis no servidor MCP-BR."""
        logger.info("Listando ferramentas disponíveis...")
        result = await self._send_request("list_tools", {})
        return result.get("tools", [])
    
    async def call_tool(self, name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Chama uma ferramenta no servidor MCP-BR.
        
        Args:
            name: Nome da ferramenta a ser chamada.
            parameters: Parâmetros para a chamada da ferramenta.
        
        Returns:
            O resultado da chamada da ferramenta.
        """
        logger.info(f"Chamando ferramenta {name} com parâmetros {parameters}...")
        result = await self._send_request("call_tool", {
            "name": name,
            "parameters": parameters
        })
        return result.get("result", {})
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Lista os recursos disponíveis no servidor MCP-BR."""
        logger.info("Listando recursos disponíveis...")
        result = await self._send_request("list_resources", {})
        return result.get("resources", [])
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Lê um recurso do servidor MCP-BR.
        
        Args:
            uri: URI do recurso a ser lido.
        
        Returns:
            O conteúdo do recurso.
        """
        logger.info(f"Lendo recurso {uri}...")
        result = await self._send_request("read_resource", {
            "uri": uri
        })
        return result.get("contents", {})

async def main():
    """Função principal para testar o cliente MCP-BR."""
    client = McpBrClient()
    
    try:
        # Conectar ao servidor MCP-BR
        await client.connect()
        
        # Inicializar a conexão
        await client.initialize()
        
        # Listar as ferramentas disponíveis
        tools = await client.list_tools()
        tool_names = [tool.get("name") for tool in tools]
        logger.info(f"Ferramentas disponíveis: {tool_names}")
        
        # Testar a ferramenta buscar_localidade
        logger.info("\n--- Testando buscar_localidade ---")
        resultado_busca = await client.call_tool("buscar_localidade", {"nome": "São Paulo"})
        logger.info(f"Resultado da busca: {json.dumps(resultado_busca, indent=2, ensure_ascii=False)}")
        
        # Testar a ferramenta gerar_relatorio
        logger.info("\n--- Testando gerar_relatorio (formato texto) ---")
        relatorio_texto = await client.call_tool("gerar_relatorio", {
            "nome_localidade": "Rio de Janeiro",
            "formato": "texto"
        })
        logger.info(f"Relatório (texto): {relatorio_texto.get('content', '')}")
        
        logger.info("\n--- Testando gerar_relatorio (formato json) ---")
        relatorio_json = await client.call_tool("gerar_relatorio", {
            "nome_localidade": "Rio de Janeiro",
            "formato": "json"
        })
        logger.info(f"Relatório (json): {json.dumps(relatorio_json.get('content', {}), indent=2, ensure_ascii=False)}")
        
        # Listar os recursos disponíveis
        resources = await client.list_resources()
        resource_names = [resource.get("name") for resource in resources]
        logger.info(f"\nRecursos disponíveis: {resource_names}")
        
        # Ler os recursos
        logger.info("\n--- Lendo recurso 'Sobre o MCP-BR' ---")
        sobre = await client.read_resource("file://docs/sobre.md")
        logger.info(f"Conteúdo do recurso: {sobre.get('content', '')[:100]}...")
        
        logger.info("\n--- Lendo recurso 'Exemplos de Uso' ---")
        exemplos = await client.read_resource("file://docs/exemplos.md")
        logger.info(f"Conteúdo do recurso: {exemplos.get('content', '')[:100]}...")
        
    except Exception as e:
        logger.error(f"Erro ao testar o cliente MCP-BR: {e}")
    finally:
        # Desconectar do servidor MCP-BR
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
