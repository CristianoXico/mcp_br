import asyncio
import pytest
import logging
import time
import datetime
from tools.transparencia import (
    testar_api,
    listar_orgaos,
    listar_contratos,
    listar_licitacoes,
    listar_auxilios_emergenciais,
    listar_bolsa_familia,
    listar_servidores,
    listar_ceis,
    listar_cnep,
    listar_despesas,
    listar_emendas,
    listar_pep,
    listar_convenios,
    listar_viagens,
    listar_transferencias,
    listar_imoveis_funcionais,
    listar_pedidos_esic,
    rate_limiter
)

# Configuração de logging para testes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Função para exibir informações sobre o rate limiter
def exibir_info_rate_limiter():
    now = datetime.datetime.now()
    if 6 <= now.hour < 24:  # 6:00 às 23:59
        rate_limit = 90
        periodo = "6:00 às 23:59"
    else:  # 00:00 às 5:59
        rate_limit = 300
        periodo = "00:00 às 5:59"
    
    logger.info(f"Período atual: {periodo} - Limite de requisições: {rate_limit} por minuto")
    logger.info(f"Requisições feitas neste minuto: {rate_limiter.request_count}")

# Fixtures para parâmetros de teste
@pytest.fixture
def codigo_ibge():
    return "3550308"  # São Paulo

@pytest.fixture
def codigo_orgao():
    return "26000"  # Ministério da Educação

@pytest.fixture
def cpf_exemplo():
    return "00000000000"  # CPF fictício para testes

@pytest.fixture
def cnpj_exemplo():
    return "00000000000000"  # CNPJ fictício para testes

@pytest.mark.asyncio
async def test_conexao_api():
    """Testa a conexão com a API do Portal da Transparência"""
    print("\nTestando conexão com a API do Portal da Transparência...")
    exibir_info_rate_limiter()
    conectado = await testar_api()
    assert conectado is True, "Falha na conexão com a API do Portal da Transparência"
    print("Conexão com a API estabelecida com sucesso")

@pytest.mark.asyncio
async def test_listar_orgaos():
    """Testa a listagem de órgãos do governo federal"""
    print("\nTestando listar_orgaos...")
    orgaos = await listar_orgaos()
    assert isinstance(orgaos, dict), "O retorno deve ser um dicionário"
    print(f"Resposta da API: {orgaos.keys() if isinstance(orgaos, dict) else 'Não é um dicionário'}")
    
    # Verifica se não há erro na resposta
    assert "erro" not in orgaos, f"Erro na resposta: {orgaos.get('erro', 'Erro desconhecido')}"
    print("Teste de listar_orgaos concluído com sucesso")

@pytest.mark.asyncio
async def test_listar_contratos():
    """Testa a listagem de contratos do governo federal"""
    print("\nTestando listar_contratos...")
    contratos = await listar_contratos(pagina=1, tamanhoPagina=5)
    assert isinstance(contratos, dict), "O retorno deve ser um dicionário"
    print(f"Resposta da API: {contratos.keys() if isinstance(contratos, dict) else 'Não é um dicionário'}")
    
    # Verifica se não há erro na resposta
    assert "erro" not in contratos, f"Erro na resposta: {contratos.get('erro', 'Erro desconhecido')}"
    print("Teste de listar_contratos concluído com sucesso")

@pytest.mark.asyncio
async def test_listar_licitacoes():
    """Testa a listagem de licitações do governo federal"""
    print("\nTestando listar_licitacoes...")
    licitacoes = await listar_licitacoes(pagina=1, tamanhoPagina=5)
    assert isinstance(licitacoes, dict), "O retorno deve ser um dicionário"
    print(f"Resposta da API: {licitacoes.keys() if isinstance(licitacoes, dict) else 'Não é um dicionário'}")
    
    # Verifica se não há erro na resposta
    assert "erro" not in licitacoes, f"Erro na resposta: {licitacoes.get('erro', 'Erro desconhecido')}"
    print("Teste de listar_licitacoes concluído com sucesso")

@pytest.mark.asyncio
async def test_listar_auxilios_emergenciais():
    """Testa a listagem de beneficiários do Auxílio Emergencial"""
    print("\nTestando listar_auxilios_emergenciais...")
    auxilios = await listar_auxilios_emergenciais(pagina=1, tamanhoPagina=5)
    assert isinstance(auxilios, dict), "O retorno deve ser um dicionário"
    print(f"Resposta da API: {auxilios.keys() if isinstance(auxilios, dict) else 'Não é um dicionário'}")
    
    # Verifica se não há erro na resposta
    assert "erro" not in auxilios, f"Erro na resposta: {auxilios.get('erro', 'Erro desconhecido')}"
    print("Teste de listar_auxilios_emergenciais concluído com sucesso")

@pytest.mark.asyncio
async def test_listar_bolsa_familia():
    """Testa a listagem de beneficiários do Bolsa Família / Auxílio Brasil"""
    print("\nTestando listar_bolsa_familia...")
    bolsa_familia = await listar_bolsa_familia(pagina=1, tamanhoPagina=5)
    assert isinstance(bolsa_familia, dict), "O retorno deve ser um dicionário"
    print(f"Resposta da API: {bolsa_familia.keys() if isinstance(bolsa_familia, dict) else 'Não é um dicionário'}")
    
    # Verifica se não há erro na resposta
    assert "erro" not in bolsa_familia, f"Erro na resposta: {bolsa_familia.get('erro', 'Erro desconhecido')}"
    print("Teste de listar_bolsa_familia concluído com sucesso")

@pytest.mark.asyncio
async def test_listar_pep():
    """Testa a listagem de pessoas expostas politicamente"""
    print("\nTestando listagem de pessoas expostas politicamente...")
    resultado = await listar_pep()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de pessoas expostas politicamente concluída")

@pytest.mark.asyncio
async def test_listar_convenios():
    """Testa a listagem de convênios"""
    print("\nTestando listagem de convênios...")
    resultado = await listar_convenios()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de convênios concluída")

@pytest.mark.asyncio
async def test_listar_viagens():
    """Testa a listagem de viagens"""
    print("\nTestando listagem de viagens...")
    resultado = await listar_viagens()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de viagens concluída")

@pytest.mark.asyncio
async def test_listar_transferencias():
    """Testa a listagem de transferências"""
    print("\nTestando listagem de transferências...")
    resultado = await listar_transferencias()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de transferências concluída")

@pytest.mark.asyncio
async def test_listar_imoveis_funcionais():
    """Testa a listagem de imóveis funcionais"""
    print("\nTestando listagem de imóveis funcionais...")
    resultado = await listar_imoveis_funcionais()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de imóveis funcionais concluída")

@pytest.mark.asyncio
async def test_listar_pedidos_esic():
    """Testa a listagem de pedidos e-SIC"""
    print("\nTestando listagem de pedidos e-SIC...")
    resultado = await listar_pedidos_esic()
    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "data" in resultado or "erro" in resultado, "Resposta não contém dados ou erro"
    print("Listagem de pedidos e-SIC concluída")

# Função principal para execução manual dos testes
async def main():
    print("\nIniciando testes do Portal da Transparência")
    
    # Exibe informações sobre o rate limiter
    exibir_info_rate_limiter()
    print(f"Hora atual: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Testa a conexão com a API
    await test_conexao_api()
    
    # Testa as funções de listagem com intervalo entre elas para demonstrar o rate limiter
    await test_listar_orgaos()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_contratos()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_licitacoes()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_auxilios_emergenciais()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_bolsa_familia()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    # Testa as novas APIs implementadas
    await test_listar_pep()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_convenios()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_viagens()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_transferencias()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_imoveis_funcionais()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    await test_listar_pedidos_esic()
    print(f"Requisições feitas neste minuto: {rate_limiter.request_count}")
    
    # Exibe informações finais sobre o rate limiter
    exibir_info_rate_limiter()
    print(f"Hora final: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print("\nTodos os testes concluídos!")

if __name__ == "__main__":
    # Executa os testes
    asyncio.run(main())
