#!/usr/bin/env python
"""
Script de demonstração para testar a integração do MCP-BR com uma LLM.
Este script simula como uma LLM poderia interagir com o servidor MCP-BR
através do adaptador LLM.

Pré-requisitos:
1. Servidor MCP-BR rodando (python server.py)
2. Adaptador LLM rodando (python llm_adapter.py)
"""

import sys
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
import httpx

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LlmMcpClient:
    """Cliente para simular uma LLM interagindo com o adaptador MCP-BR."""
    
    def __init__(self, adapter_url: str = "http://localhost:8080"):
        """Inicializa o cliente LLM.
        
        Args:
            adapter_url: URL base do adaptador LLM
        """
        self.adapter_url = adapter_url
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"Cliente LLM inicializado com URL do adaptador: {adapter_url}")
    
    async def query(self, method: str, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Envia uma consulta ao adaptador LLM.
        
        Args:
            method: Método MCP a ser chamado
            params: Parâmetros para o método
            context: Contexto adicional para a LLM
            
        Returns:
            Resposta do adaptador LLM
        """
        payload = {
            "method": method,
            "params": params
        }
        
        if context:
            payload["context"] = context
        
        logger.info(f"Enviando consulta LLM: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            response = await self.client.post(
                f"{self.adapter_url}/llm/query",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Resposta recebida do adaptador LLM")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao consultar adaptador LLM: {str(e)}")
            return {"error": str(e)}
    
    async def list_methods(self) -> List[str]:
        """Lista os métodos disponíveis no servidor MCP.
        
        Returns:
            Lista de métodos disponíveis
        """
        try:
            response = await self.client.get(f"{self.adapter_url}/llm/methods")
            response.raise_for_status()
            result = response.json()
            
            return result.get("methods", [])
            
        except Exception as e:
            logger.error(f"Erro ao listar métodos: {str(e)}")
            return []
    
    async def check_health(self) -> bool:
        """Verifica a saúde do adaptador LLM.
        
        Returns:
            True se o adaptador estiver saudável, False caso contrário
        """
        try:
            response = await self.client.get(f"{self.adapter_url}/health")
            response.raise_for_status()
            result = response.json()
            
            return result.get("status") == "healthy"
            
        except Exception as e:
            logger.error(f"Erro ao verificar saúde do adaptador: {str(e)}")
            return False
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

async def simular_conversa_llm():
    """Simula uma conversa com uma LLM usando o adaptador MCP-BR."""
    client = LlmMcpClient()
    
    try:
        # Verifica a saúde do adaptador
        healthy = await client.check_health()
        if not healthy:
            logger.error("O adaptador LLM não está saudável. Verifique se ele está rodando.")
            return
        
        logger.info("Adaptador LLM está saudável.")
        
        # Lista os métodos disponíveis
        methods = await client.list_methods()
        logger.info(f"Métodos disponíveis: {methods}")
        
        # Exemplo 1: Buscar informações sobre um município
        print("\n--- Exemplo 1: Buscar informações sobre um município ---")
        response = await client.query(
            method="buscar_localidade",
            params={"nome": "São Paulo", "tipo": "municipio"},
            context={"user_query": "Quais são as informações sobre São Paulo?"}
        )
        
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        # Exemplo 2: Obter dados de vulnerabilidade social
        print("\n--- Exemplo 2: Obter dados de vulnerabilidade social ---")
        response = await client.query(
            method="vulnerabilidade_social",
            params={"municipio": "Rio de Janeiro", "ano": 2023},
            context={"user_query": "Qual é a situação de vulnerabilidade social no Rio de Janeiro?"}
        )
        
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        # Exemplo 3: Obter relatório de localidade
        print("\n--- Exemplo 3: Obter relatório de localidade ---")
        response = await client.query(
            method="relatorio_localidade",
            params={"nome": "Belo Horizonte", "tipo": "municipio", "formato": "resumido"},
            context={"user_query": "Faça um relatório sobre Belo Horizonte."}
        )
        
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
    finally:
        await client.close()

async def main():
    """Função principal."""
    print("=== Teste de Integração MCP-BR com LLM ===")
    print("Este script simula como uma LLM poderia interagir com o MCP-BR.")
    print("Certifique-se de que o servidor MCP-BR e o adaptador LLM estão rodando.")
    
    await simular_conversa_llm()

if __name__ == "__main__":
    # Configura o loop de eventos para Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa a função principal
    asyncio.run(main())
