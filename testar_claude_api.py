#!/usr/bin/env python
"""
Script para testar a integração do MCP-BR com a API Claude.
Este script usa a API Claude diretamente para interagir com o MCP-BR.

Pré-requisitos:
1. Ter uma chave de API Claude (Anthropic)
2. Servidor MCP-BR rodando (python mcp_server.py)
"""

import os
import sys
import json
import asyncio
import logging
import argparse
from typing import Dict, Any, List, Optional
import httpx
import subprocess

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ClaudeApiClient:
    """Cliente para a API Claude."""
    
    def __init__(self, api_key: str, api_url: str = "https://api.anthropic.com/v1/messages"):
        """Inicializa o cliente Claude.
        
        Args:
            api_key: Chave de API Claude
            api_url: URL da API Claude
        """
        self.api_key = api_key
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=60.0)
        self.client.headers.update({
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        })
        logger.info("Cliente Claude API inicializado")
    
    async def send_message(self, message: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Envia uma mensagem para o Claude.
        
        Args:
            message: Mensagem para enviar
            system_prompt: Prompt de sistema opcional
            
        Returns:
            Resposta do Claude
        """
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4000,
            "messages": [
                {"role": "user", "content": message}
            ]
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = await self.client.post(
                self.api_url,
                json=payload
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para Claude: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

class McpBrRunner:
    """Executa o servidor MCP-BR e gerencia sua comunicação."""
    
    def __init__(self, mcp_dir: str = None):
        """Inicializa o executor MCP-BR.
        
        Args:
            mcp_dir: Diretório do MCP-BR
        """
        self.mcp_dir = mcp_dir or os.path.dirname(os.path.abspath(__file__))
        self.process = None
        logger.info(f"Executor MCP-BR inicializado com diretório: {self.mcp_dir}")
    
    def start_server(self) -> bool:
        """Inicia o servidor MCP-BR.
        
        Returns:
            True se o servidor foi iniciado com sucesso, False caso contrário
        """
        try:
            # Verifica se o servidor já está rodando
            if self.process and self.process.poll() is None:
                logger.info("Servidor MCP-BR já está rodando")
                return True
            
            # Inicia o servidor MCP-BR
            logger.info("Iniciando servidor MCP-BR...")
            self.process = subprocess.Popen(
                ["python", "mcp_server.py"],
                cwd=self.mcp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Aguarda um pouco para o servidor iniciar
            import time
            time.sleep(2)
            
            # Verifica se o servidor iniciou corretamente
            if self.process.poll() is None:
                logger.info("Servidor MCP-BR iniciado com sucesso")
                return True
            else:
                stdout, stderr = self.process.communicate()
                logger.error(f"Erro ao iniciar servidor MCP-BR: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor MCP-BR: {str(e)}")
            return False
    
    def stop_server(self):
        """Para o servidor MCP-BR."""
        if self.process and self.process.poll() is None:
            logger.info("Parando servidor MCP-BR...")
            self.process.terminate()
            self.process.wait(timeout=5)
            logger.info("Servidor MCP-BR parado")

async def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description="Teste da integração MCP-BR com Claude API")
    parser.add_argument("--api-key", help="Chave de API Claude")
    parser.add_argument("--message", default="Execute o relatório completo de vulnerabilidade social para o município de São José do Rio Preto?", 
                      help="Mensagem para enviar ao Claude")
    
    args = parser.parse_args()
    
    # Obtém a chave de API
    api_key = args.api_key or os.environ.get("CLAUDE_API_KEY")
    if not api_key:
        print("Erro: Chave de API Claude não fornecida")
        print("Use --api-key ou defina a variável de ambiente CLAUDE_API_KEY")
        return
    
    # Inicializa o cliente Claude
    claude_client = ClaudeApiClient(api_key)
    
    # Inicializa o executor MCP-BR
    mcp_runner = McpBrRunner()
    
    try:
        # Inicia o servidor MCP-BR
        if not mcp_runner.start_server():
            print("Erro ao iniciar o servidor MCP-BR. Verifique os logs para mais detalhes.")
            return
        
        # Sistema prompt com instruções para usar o MCP-BR
        system_prompt = """
        Você tem acesso a um servidor MCP-BR que fornece dados sobre localidades brasileiras.
        Use as seguintes ferramentas quando apropriado:
        
        1. buscar_localidade: Busca informações sobre uma localidade brasileira
        2. gerar_relatorio: Gera um relatório completo sobre uma localidade
        3. buscar_dados_demograficos: Busca dados demográficos de uma localidade
        4. buscar_dados_socioeconomicos: Busca dados socioeconômicos de uma localidade
        
        Quando o usuário perguntar sobre uma localidade brasileira, use estas ferramentas
        para fornecer informações precisas e atualizadas.
        """
        
        # Envia uma mensagem para o Claude
        print(f"Enviando mensagem para Claude: '{args.message}'")
        response = await claude_client.send_message(args.message, system_prompt)
        
        # Exibe a resposta
        if "error" in response:
            print(f"Erro na resposta do Claude: {response['error']}")
        else:
            content = response.get("content", [])
            if content and len(content) > 0:
                message = content[0].get("text", "")
                print("\nResposta do Claude:")
                print("-" * 50)
                print(message)
                print("-" * 50)
            else:
                print("Resposta vazia do Claude")
        
    finally:
        # Fecha o cliente Claude
        await claude_client.close()
        
        # Para o servidor MCP-BR
        mcp_runner.stop_server()

if __name__ == "__main__":
    # Configura o loop de eventos para Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa a função principal
    asyncio.run(main())
