"""
Configurações centralizadas para URLs e chaves de APIs externas usadas no MCP-BR.
Assegure que as credenciais sensíveis sejam carregadas de variáveis de ambiente.
"""
import os

BASE_URL_PUBLICACOES = "https://servicodados.ibge.gov.br/api/v3"
BASE_URL_NOMES = "https://servicodados.ibge.gov.br/api/v2"
BASE_URL_CNAE = "https://servicodados.ibge.gov.br/api/v2"
BASE_URL_AGREGADOS = "https://servicodados.ibge.gov.br/api/v3/agregados"
# Adicione outras bases conforme necessário

# Exemplo de uso seguro de variáveis de ambiente para tokens
IBGE_API_KEY = os.getenv("IBGE_API_KEY", "")
DADOS_ABERTOS_TOKEN = os.getenv("DADOS_ABERTOS_TOKEN", "")

API_CONFIG = {
    "BASE_URL_PUBLICACOES": BASE_URL_PUBLICACOES,
    "BASE_URL_NOMES": BASE_URL_NOMES,
    "BASE_URL_CNAE": BASE_URL_CNAE,
    "BASE_URL_AGREGADOS": BASE_URL_AGREGADOS,
    "IBGE_API_KEY": IBGE_API_KEY,
    "DADOS_ABERTOS_TOKEN": DADOS_ABERTOS_TOKEN,
}
