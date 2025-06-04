import asyncio
import sys
import os
import pytest

# Adiciona o diretório pai ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from config.api_config import API_CONFIG
from tools.portal_dados_abertos import (
    listar_dados_abertos, 
    buscar_dados_por_id, 
    listar_recursos, 
    listar_grupos, 
    listar_organizacoes, 
    buscar_dados_por_tag,
    listar_formatos,
    listar_licencas,
    buscar_dados_por_palavra_chave
)
import httpx

# Fixtures para os parâmetros necessários
@pytest.fixture
def id_dataset():
    return "dataset-1"  # ID de exemplo para testes

@pytest.fixture
def tag():
    return "saude"  # Tag de exemplo para testes

@pytest.fixture
def keyword():
    return "educacao"  # Palavra-chave de exemplo para testes

@pytest.mark.asyncio
async def test_listar_dados_abertos():
    print("\nTestando listar_dados_abertos...")
    dados = await listar_dados_abertos()
    assert isinstance(dados, list), "O retorno deve ser uma lista"
    print(f"Total de conjuntos de dados: {len(dados)}")
    
    # Verifica se os IDs são strings
    if dados:
        assert isinstance(dados[0], str), "Os elementos da lista devem ser strings (IDs)"
        print(f"Exemplo de ID: {dados[0]}")
        return dados[0]  # Retorna o primeiro ID para uso nos testes subsequentes
    return None

@pytest.mark.asyncio
async def test_buscar_dados_por_id(id_dataset: str):
    print("\nTestando buscar_dados_por_id...")
    detalhes = await buscar_dados_por_id(id_dataset)
    assert isinstance(detalhes, dict), "O retorno deve ser um dicionário"
    print(f"Nome do conjunto: {detalhes.get('title', 'N/A')}")
    print(f"Descrição: {detalhes.get('notes', 'N/A')}")
    return detalhes

@pytest.mark.asyncio
async def test_listar_recursos(id_dataset: str):
    print("\nTestando listar_recursos...")
    recursos = await listar_recursos(id_dataset)
    assert isinstance(recursos, list), "O retorno deve ser uma lista"
    print(f"Total de recursos: {len(recursos)}")
    return recursos

@pytest.mark.asyncio
async def test_listar_grupos():
    print("\nTestando listar_grupos...")
    grupos = await listar_grupos()
    assert isinstance(grupos, list), "O retorno deve ser uma lista"
    print(f"Total de grupos: {len(grupos)}")
    
    # Verifica se os grupos são strings (IDs)
    if grupos:
        assert isinstance(grupos[0], str), "Os elementos da lista devem ser strings (IDs)"
        print(f"Exemplo de ID de grupo: {grupos[0]}")
    else:
        print("Nenhum grupo encontrado")

@pytest.mark.asyncio
async def test_listar_organizacoes():
    print("\nTestando listar_organizacoes...")
    orgs = await listar_organizacoes()
    assert isinstance(orgs, list), "O retorno deve ser uma lista"
    print(f"Total de organizações: {len(orgs)}")
    
    # Verifica se as organizações são strings (IDs)
    if orgs:
        assert isinstance(orgs[0], str), "Os elementos da lista devem ser strings (IDs)"
        print(f"Exemplo de ID de organização: {orgs[0]}")
    else:
        print("Nenhuma organização encontrada")

@pytest.mark.asyncio
async def test_buscar_dados_por_tag(tag: str):
    print(f"\nTestando buscar_dados_por_tag com tag '{tag}'...")
    resultados = await buscar_dados_por_tag(tag)
    assert isinstance(resultados, list), "O retorno deve ser uma lista"
    print(f"Total de resultados: {len(resultados)}")
    
    # Verifica se os resultados têm a estrutura esperada
    if resultados:
        resultado = resultados[0]
        assert isinstance(resultado, dict), "Os resultados devem ser dicionários"
        print(f"Exemplo de resultado: {resultado.get('title', 'N/A')}")
    else:
        print("Nenhum resultado encontrado")

@pytest.mark.asyncio
async def test_listar_formatos():
    print("\nTestando listar_formatos...")
    formatos = await listar_formatos()
    assert isinstance(formatos, list), "O retorno deve ser uma lista"
    print(f"Total de formatos: {len(formatos)}")
    
    if formatos:
        print(f"Formatos disponíveis: {', '.join(formatos)}")
    else:
        print("Nenhum formato encontrado")

@pytest.mark.asyncio
async def test_listar_licencas():
    print("\nTestando listar_licencas...")
    licencas = await listar_licencas()
    assert isinstance(licencas, list), "O retorno deve ser uma lista"
    print(f"Total de licenças: {len(licencas)}")
    
    # Verifica se as licenças têm a estrutura esperada
    if licencas:
        licenca = licencas[0]
        assert isinstance(licenca, dict), "As licenças devem ser dicionários"
        print(f"Exemplo de licença: {licenca.get('title', 'N/A')}")
    else:
        print("Nenhuma licença encontrada")

@pytest.mark.asyncio
async def test_buscar_dados_por_palavra_chave(keyword: str):
    print(f"\nTestando buscar_dados_por_palavra_chave com palavra-chave '{keyword}'...")
    resultados = await buscar_dados_por_palavra_chave(keyword)
    assert isinstance(resultados, list), "O retorno deve ser uma lista"
    print(f"Total de resultados: {len(resultados)}")
    
    # Verifica se os resultados têm a estrutura esperada
    if resultados:
        resultado = resultados[0]
        assert isinstance(resultado, dict), "Os resultados devem ser dicionários"
        print(f"Exemplo de resultado: {resultado.get('title', 'N/A')}")
    else:
        print("Nenhum resultado encontrado")

async def main():
    print("\nIniciando testes do Portal de Dados Abertos")
    
    # Configurar header com token para todas as chamadas
    httpx.Client.headers = httpx.Headers({
        "Authorization": f"Bearer {API_CONFIG['dados_abertos_token']}"
    })
    
    # Primeiro, tenta obter um ID de conjunto de dados
    id_dataset = await test_listar_dados_abertos()
    
    if id_dataset:
        print("\nExecutando testes com conjunto de dados encontrado...")
        await test_buscar_dados_por_id(id_dataset)
        await test_listar_recursos(id_dataset)
        await test_listar_grupos()
        await test_listar_organizacoes()
        await test_buscar_dados_por_tag("saude")
    else:
        print("\nNenhum conjunto de dados encontrado para testar")
        print("\nExecutando testes que não dependem de conjunto de dados...")
        await test_listar_grupos()
        await test_listar_organizacoes()
        await test_buscar_dados_por_tag("saude")
        await test_listar_formatos()
        await test_listar_licencas()

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
