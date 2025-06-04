import asyncio
import json
from tools.busca_localidade import buscar_estados, buscar_municipios, normalizar_texto

async def main():
    print("Buscando estados...")
    estados = await buscar_estados()
    
    # Imprime os primeiros 3 estados para verificar a estrutura
    print("Primeiros 3 estados:")
    for i, estado in enumerate(estados.get("data", [])[:3]):
        print(f"Estado {i+1}: {estado['nome']} ({estado['sigla']})")
        print(f"  Dados: {estado}")
    
    # Procura por São Paulo nos estados
    print("\nProcurando estado São Paulo...")
    for estado in estados.get("data", []):
        nome_estado = estado.get("nome", "")
        if "SAO PAULO" in nome_estado.upper() or "SP" == estado.get("sigla", ""):
            print(f"Estado encontrado: {estado}")
    
    print("\nBuscando municípios...")
    municipios = await buscar_municipios()
    
    # Imprime os primeiros 3 municípios para verificar a estrutura
    print("Primeiros 3 municípios:")
    for i, municipio in enumerate(municipios.get("data", [])[:3]):
        print(f"Município {i+1}: {municipio['nome']} - {municipio.get('uf', {}).get('sigla', '')}")
        print(f"  Dados: {municipio}")
    
    # Procura por São Paulo nos municípios
    print("\nProcurando município São Paulo...")
    for municipio in municipios.get("data", []):
        nome_municipio = municipio.get("nome", "")
        if "SAO PAULO" in nome_municipio.upper() and "SP" == municipio.get("uf", {}).get("sigla", ""):
            print(f"Município encontrado: {municipio}")
            break

if __name__ == "__main__":
    asyncio.run(main())
