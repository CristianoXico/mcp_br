"""
Configurações centralizadas para URLs e chaves de APIs externas usadas no MCP-BR.
Assegure que as credenciais sensíveis sejam carregadas de variáveis de ambiente.
"""
import os

BASE_URL_PUBLICACOES = "https://servicodados.ibge.gov.br/api/v3"
BASE_URL_NOMES = "https://servicodados.ibge.gov.br/api/v2"
BASE_URL_CNAE = "https://servicodados.ibge.gov.br/api/v2"
# Adicione outras bases conforme necessário

# Exemplo de uso seguro de variáveis de ambiente para tokens
IBGE_API_KEY = os.getenv("IBGE_API_KEY", "")
DADOS_ABERTOS_TOKEN = os.getenv("DADOS_ABERTOS_TOKEN", "")
