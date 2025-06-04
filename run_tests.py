#!/usr/bin/env python
"""
Script para executar os testes automatizados do projeto MCP-BR.
"""

import unittest
import asyncio
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def run_tests():
    """Executa todos os testes do projeto."""
    # Descobre e carrega todos os testes
    test_dir = Path(__file__).parent / 'tests'
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(str(test_dir), pattern='test_*.py')

    # Configura o runner de testes
    test_runner = unittest.TextTestRunner(verbosity=2)
    
    # Executa os testes
    result = test_runner.run(test_suite)
    
    # Retorna código de saída baseado no resultado dos testes
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    # Configura o loop de eventos para testes assíncronos
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa os testes e sai com o código apropriado
    sys.exit(run_tests())
