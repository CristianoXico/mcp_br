#!/usr/bin/env python
"""
Script principal para busca de informações sobre localidades (municípios, cidades, estados, regiões)
utilizando as APIs do Portal da Transparência e outras fontes de dados.

Uso:
    python buscar_localidade.py <nome_localidade> [--formato texto|json] [--no-save]
    
Exemplos:
    python buscar_localidade.py "São Paulo"
    python buscar_localidade.py "Nordeste" --formato json
    python buscar_localidade.py "MG" --no-save
    python buscar_localidade.py "MG" --periodo mes --data 2022-01-01
"""

import asyncio
import argparse
import sys
import os
import logging
from datetime import datetime
from tools.busca_localidade import buscar_info_localidade, main as busca_main
from tools.relatorio_localidade import main as relatorio_main

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    parser = argparse.ArgumentParser(
        description="Busca informações sobre localidades utilizando as APIs do Portal da Transparência",
        epilog="""
        Exemplos:
          python buscar_localidade.py "São Paulo"
          python buscar_localidade.py "Nordeste" --formato json
          python buscar_localidade.py "MG" --no-save
          python buscar_localidade.py "MG" --periodo mes --data 2022-01-01
        """
    )
    parser.add_argument("localidade", help="Nome da localidade (município, cidade, estado ou região)")
    parser.add_argument("--formato", choices=["texto", "json"], default="texto", 
                        help="Formato de saída (texto ou json)")
    parser.add_argument("--no-save", action="store_true", 
                        help="Não salvar o relatório em arquivo")
    parser.add_argument("--simples", action="store_true", 
                        help="Exibir apenas informações básicas, sem gerar relatório completo")
    parser.add_argument("--periodo", choices=["dia", "mes", "ano"], default="mes", 
                        help="Tipo de período para análise (dia, mes, ano)")
    parser.add_argument("--data", help="Data de referência no formato YYYY-MM-DD (padrão: data atual)")
    parser.add_argument("--periodo-valor", help="Valor específico do período: YYYY-MM-DD para dia, YYYY-MM para mês, YYYY para ano")
    
    args = parser.parse_args()
    
    try:
        if args.simples:
            await busca_main(args.localidade)
        else:
            await relatorio_main(args.localidade, args.formato, not args.no_save, args.periodo, args.data, args.periodo_valor)
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        return 1
    except Exception as e:
        logger.error(f"Erro ao processar a localidade '{args.localidade}': {e}", exc_info=True)
        print(f"\nErro ao processar a localidade '{args.localidade}':")
        print(f"  {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    # Verifica se o diretório 'data' existe, se não, cria
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Verifica se o diretório 'relatorios' existe, se não, cria
    relatorios_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorios")
    os.makedirs(relatorios_dir, exist_ok=True)
    
    sys.exit(asyncio.run(main()))
