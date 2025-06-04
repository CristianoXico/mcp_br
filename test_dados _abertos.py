import asyncio
from tools.portal_dados_abertos import listar_dados_abertos, buscar_dados_por_id, listar_recursos, listar_grupos, listar_organizacoes, buscar_dados_por_tag
from tools.api_config import API_CONFIG
import httpx

async def test_listar_dados_abertos():
    print("\nTestando listar_dados_abertos...")
    dados = await listar_dados_abertos()
    assert isinstance(dados, list)
    assert len(dados) > 0
    print(f"Total de conjuntos de dados: {len(dados)}")

async def test_buscar_dados_por_id():
    print("\nTestando buscar_dados_por_id...")
    # Usando um ID de exemplo (pode precisar ser ajustado)
    id_dataset = "4e39805f-1710-431c-b65d-345436909861"
    detalhes = await buscar_dados_por_id(id_dataset)
    assert isinstance(detalhes, dict)
    assert "title" in detalhes
    print(f"Nome do conjunto: {detalhes.get('title', 'N/A')}")

async def test_listar_recursos():
    print("\nTestando listar_recursos...")
    # Usando um ID de exemplo (pode precisar ser ajustado)
    id_dataset = "4e39805f-1710-431c-b65d-345436909861"
    recursos = await listar_recursos(id_dataset)
    assert isinstance(recursos, list)
    print(f"Total de recursos: {len(recursos)}")

async def test_listar_grupos():
    print("\nTestando listar_grupos...")
    grupos = await listar_grupos()
    assert isinstance(grupos, list)
    assert len(grupos) > 0
    print(f"Total de grupos: {len(grupos)}")

async def test_listar_organizacoes():
    print("\nTestando listar_organizacoes...")
    orgs = await listar_organizacoes()
    assert isinstance(orgs, list)
    assert len(orgs) > 0
    print(f"Total de organizações: {len(orgs)}")

async def test_buscar_dados_por_tag():
    print("\nTestando buscar_dados_por_tag...")
    resultados = await buscar_dados_por_tag("saude")
    assert isinstance(resultados, list)
    print(f"Total de resultados: {len(resultados)}")

async def main():
    print("\nIniciando testes do Portal de Dados Abertos")
    
    # Configurar header com token
    httpx.Client.headers = httpx.Headers({
        "Authorization": f"Bearer {API_CONFIG['dados_abertos_token']}"
    })
    
    # Executar todos os testes
    await test_listar_dados_abertos()
    await test_buscar_dados_por_id()
    await test_listar_recursos()
    await test_listar_grupos()
    await test_listar_organizacoes()
    await test_buscar_dados_por_tag()

if __name__ == "__main__":
    asyncio.run(main())
