#!/usr/bin/env python
"""
Script para executar a ferramenta de vulnerabilidade social diretamente.
Permite testar a funcionalidade sem precisar do servidor MCP completo.

Uso:
    python executar_vulnerabilidade_social.py <municipio> [ano]

Exemplo:
    python executar_vulnerabilidade_social.py "São Paulo" 2023
"""

import sys
import json
import asyncio
import logging
from tools.vulnerabilidade_social import obter_vulnerabilidade_social

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Função principal para executar a ferramenta de vulnerabilidade social."""
    # Verifica os argumentos da linha de comando
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <municipio> [ano]")
        print(f"Exemplo: {sys.argv[0]} 'São Paulo' 2023")
        sys.exit(1)

    # Obtém os parâmetros
    municipio = sys.argv[1]
    ano = int(sys.argv[2]) if len(sys.argv) > 2 else 2023

    # Exibe informações sobre a consulta
    print(f"Consultando dados de vulnerabilidade social para {municipio} (ano: {ano})...")
    print("Este processo pode levar alguns segundos...")

    try:
        # Obtém os dados de vulnerabilidade social
        resultado = await obter_vulnerabilidade_social(municipio, ano)
        
        # Formata o resultado como JSON para melhor visualização
        resultado_formatado = json.dumps(resultado, indent=2, ensure_ascii=False)
        
        # Exibe o resultado
        print("\nResultado da consulta:")
        print(resultado_formatado)
        
        # Salva o resultado em um arquivo JSON
        nome_arquivo = f"vulnerabilidade_{municipio.replace(' ', '_').lower()}_{ano}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(resultado_formatado)
        
        print(f"\nOs resultados também foram salvos no arquivo: {nome_arquivo}")
        
    except Exception as e:
        logger.error(f"Erro ao executar a ferramenta: {str(e)}")
        print(f"Erro ao executar a ferramenta: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Configura o loop de eventos para Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa a função principal
    asyncio.run(main())
