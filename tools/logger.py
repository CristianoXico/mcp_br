"""
Logger centralizado para o projeto MCP-BR.
Facilita logs padronizados e reutilizáveis em todos os módulos.
"""
import logging
import sys

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)

def get_logger(name: str = "mcp_br"):
    return logging.getLogger(name)
