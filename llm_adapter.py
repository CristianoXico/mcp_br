#!/usr/bin/env python
"""
Adaptador para integrar o servidor MCP-BR com Large Language Models (LLMs).
Este script permite que uma LLM acesse as funcionalidades do MCP-BR através
de chamadas JSON-RPC, fornecendo uma interface simplificada.

Uso:
    1. Inicie o servidor MCP-BR em um terminal separado
    2. Execute este script para iniciar o adaptador
    3. Conecte sua LLM ao adaptador usando a API fornecida
"""

import os
import sys
import json
import asyncio
import logging
import argparse
from typing import Dict, Any, List, Optional, Union
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modelos Pydantic para validação
class LlmRequest(BaseModel):
    """Modelo para requisições da LLM."""
    method: str = Field(..., description="Método MCP a ser chamado")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parâmetros para o método")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Contexto adicional para a LLM")

class LlmResponse(BaseModel):
    """Modelo para respostas para a LLM."""
    result: Any = Field(..., description="Resultado da chamada ao método MCP")
    error: Optional[str] = Field(default=None, description="Mensagem de erro, se houver")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadados adicionais")

# Configuração do cliente HTTP
class McpClient:
    """Cliente para comunicação com o servidor MCP-BR."""
    
    def __init__(self, mcp_url: str = "http://localhost:8000/jsonrpc"):
        """Inicializa o cliente MCP.
        
        Args:
            mcp_url: URL do endpoint JSON-RPC do servidor MCP
        """
        self.mcp_url = mcp_url
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"Cliente MCP inicializado com URL: {mcp_url}")
    
    async def call_method(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Chama um método no servidor MCP.
        
        Args:
            method: Nome do método a ser chamado
            params: Parâmetros para o método
            
        Returns:
            Resposta do servidor MCP
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        
        logger.info(f"Chamando método MCP: {method} com parâmetros: {params}")
        
        try:
            response = await self.client.post(
                self.mcp_url,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                logger.error(f"Erro na chamada MCP: {result['error']}")
                return {"error": result["error"]}
            
            return {"result": result.get("result")}
            
        except Exception as e:
            logger.error(f"Erro ao chamar método MCP: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

# Criação da aplicação FastAPI
app = FastAPI(
    title="MCP-BR LLM Adapter",
    description="Adaptador para integrar o servidor MCP-BR com Large Language Models",
    version="1.0.0"
)

# Adiciona middleware CORS para permitir chamadas de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente MCP global
mcp_client = None

@app.on_event("startup")
async def startup():
    """Inicializa o cliente MCP na inicialização da aplicação."""
    global mcp_client
    mcp_url = os.environ.get("MCP_URL", "http://localhost:8000/jsonrpc")
    mcp_client = McpClient(mcp_url)
    logger.info("Adaptador LLM iniciado e conectado ao servidor MCP")

@app.on_event("shutdown")
async def shutdown():
    """Fecha o cliente MCP ao encerrar a aplicação."""
    global mcp_client
    if mcp_client:
        await mcp_client.close()
    logger.info("Adaptador LLM encerrado")

@app.post("/llm/query", response_model=LlmResponse)
async def llm_query(request: LlmRequest) -> LlmResponse:
    """Endpoint para consultas da LLM ao servidor MCP.
    
    Args:
        request: Requisição da LLM contendo método e parâmetros
        
    Returns:
        Resposta formatada para a LLM
    """
    global mcp_client
    
    if not mcp_client:
        raise HTTPException(status_code=500, detail="Cliente MCP não inicializado")
    
    # Chama o método no servidor MCP
    result = await mcp_client.call_method(request.method, request.params)
    
    # Formata a resposta para a LLM
    if "error" in result:
        return LlmResponse(
            result=None,
            error=result["error"],
            metadata={"context": request.context}
        )
    
    return LlmResponse(
        result=result["result"],
        metadata={
            "method": request.method,
            "params": request.params,
            "context": request.context
        }
    )

@app.get("/llm/methods")
async def list_methods() -> Dict[str, List[str]]:
    """Lista os métodos disponíveis no servidor MCP.
    
    Returns:
        Lista de métodos disponíveis
    """
    # Métodos conhecidos do MCP-BR
    methods = [
        "buscar_localidade",
        "relatorio_localidade",
        "dados_transparencia",
        "vulnerabilidade_social"
    ]
    
    return {"methods": methods}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Endpoint para verificar a saúde do adaptador.
    
    Returns:
        Status do adaptador
    """
    return {"status": "healthy", "service": "mcp-br-llm-adapter"}

def main():
    """Função principal para executar o adaptador."""
    parser = argparse.ArgumentParser(description="Adaptador MCP-BR para LLMs")
    parser.add_argument("--host", default="127.0.0.1", help="Host para o servidor")
    parser.add_argument("--port", type=int, default=8080, help="Porta para o servidor")
    parser.add_argument("--mcp-url", default="http://localhost:8000/jsonrpc", help="URL do servidor MCP-BR")
    
    args = parser.parse_args()
    
    # Define a URL do MCP como variável de ambiente
    os.environ["MCP_URL"] = args.mcp_url
    
    # Inicia o servidor
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
