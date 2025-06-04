#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
from tools.relatorio_localidade import gerar_relatorio_completo, exibir_relatorio_texto

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    print("Gerando relatório para São Paulo/SP...")
    relatorio = await gerar_relatorio_completo('São Paulo/SP')
    exibir_relatorio_texto(relatorio)
    
    print("\n\nGerando relatório para o estado de São Paulo...")
    relatorio_estado = await gerar_relatorio_completo('São Paulo')
    exibir_relatorio_texto(relatorio_estado)

if __name__ == "__main__":
    asyncio.run(main())
