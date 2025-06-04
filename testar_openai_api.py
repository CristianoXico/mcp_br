import os
import sys
import argparse
import asyncio
import subprocess
import time
import openai

MCP_SERVER_CMD = [sys.executable, "mcp_server_quickstart.py"]

PROMPT_MCP = """
Você é um assistente conectado ao MCP-BR, um servidor de contexto que oferece ferramentas para consultar dados de municípios brasileiros, gerar relatórios e acessar recursos de documentação. Use as ferramentas disponíveis para responder perguntas sobre localidades brasileiras.

Exemplo de chamada de ferramenta:
<tool_call name="gerar_relatorio">
  <param name="municipio">São José do Rio Preto</param>
  <param name="formato">texto</param>
</tool_call>

Exemplo de leitura de recurso:
<resource_read uri="resource://guia_llm" />

Quando precisar de dados, use as ferramentas ou recursos do MCP-BR. Sempre explique sua resposta ao usuário.
"""

def start_mcp_server():
    proc = subprocess.Popen(MCP_SERVER_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Aguarda o servidor subir
    return proc

def stop_mcp_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', type=str, default=os.getenv("OPENAI_API_KEY"), help="Chave da API OpenAI.")
    parser.add_argument('--model', type=str, default="gpt-4o", help="Modelo OpenAI a ser usado.")
    parser.add_argument('--prompt', type=str, default=None, help="Prompt customizado.")
    args = parser.parse_args()

    if not args.api_key:
        print("Erro: forneça a chave da API OpenAI via --api-key ou variável OPENAI_API_KEY.")
        sys.exit(1)

    openai.api_key = args.api_key
    proc = start_mcp_server()
    print("Servidor MCP-BR iniciado para testes com OpenAI.")

    try:
        prompt = args.prompt if args.prompt else PROMPT_MCP + "\nGere um relatório de vulnerabilidade social para o município de Fortaleza no formato texto."
        print("Prompt enviado ao modelo:\n", prompt)
        response = openai.ChatCompletion.create(
            model=args.model,
            messages=[{"role": "system", "content": "Você é um assistente MCP-BR."},
                      {"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800
        )
        print("\nResposta do modelo:\n", response["choices"][0]["message"]["content"])
    finally:
        stop_mcp_server(proc)
        print("Servidor MCP-BR encerrado.")

if __name__ == "__main__":
    main()
