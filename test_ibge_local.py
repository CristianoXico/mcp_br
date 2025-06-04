# test_ibge_local.py
import asyncio
from tools.ibge import (
    buscar_populacao_por_codigo,
    buscar_populacao_por_nome,
    buscar_municipio_por_codigo,
    buscar_municipio_por_nome,
    listar_estados,
    listar_regioes,
    buscar_area_territorial,
    buscar_densidade_demografica,
    buscar_metadados,
    listar_variaveis,
    listar_unidades_medida,
    listar_conceitos,
    listar_fontes,
    listar_dominios
)

async def main():
    # Código do município de Campinas
    codigo_campinas = "3509502"
    nome_campinas = "Campinas"

    # Teste de população por código
    resultado_populacao_codigo = buscar_populacao_por_codigo(codigo_campinas)
    print("\nTeste de população por código:")
    print("Resultado:", resultado_populacao_codigo)

    # Teste de população por nome
    resultado_populacao_nome = buscar_populacao_por_nome(nome_campinas)
    print("\nTeste de população por nome:")
    print("Resultado:", resultado_populacao_nome)

    # Teste de busca de município por código
    resultado_municipio_codigo = buscar_municipio_por_codigo(codigo_campinas)
    print("\nTeste de busca de município por código:")
    print("Resultado:", resultado_municipio_codigo)

    # Teste de busca de município por nome
    resultado_municipio_nome = buscar_municipio_por_nome(nome_campinas)
    print("\nTeste de busca de município por nome:")
    print("Resultado:", resultado_municipio_nome)

    # Teste de listagem de estados
    resultado_estados = listar_estados()
    print("\nTeste de listagem de estados:")
    print("Número de estados:", len(resultado_estados))
    print("Primeiro estado:", resultado_estados[0])

    # Teste de listagem de regiões
    resultado_regioes = listar_regioes()
    print("\nTeste de listagem de regiões:")
    print("Número de regiões:", len(resultado_regioes))
    print("Primeira região:", resultado_regioes[0])

    # Teste de área territorial
    resultado_area = buscar_area_territorial(codigo_campinas)
    print("\nTeste de área territorial:")
    print("Resultado:", resultado_area)

    # Teste de densidade demográfica
    resultado_densidade = buscar_densidade_demografica(codigo_campinas)
    print("\nTeste de densidade demográfica:")
    print("Resultado:", resultado_densidade)

    # Teste de metadados
    resultado_metadados = await buscar_metadados("populacao", "2023")
    print("\nTeste de metadados:")
    print("Resultado:", resultado_metadados)

    # Teste de variáveis
    resultado_variaveis = listar_variaveis()
    print("\nTeste de listagem de variáveis:")
    print("Número de variáveis:", len(resultado_variaveis))
    print("Primeira variável:", resultado_variaveis[0])

    # Teste de unidades de medida
    resultado_unidades = listar_unidades_medida()
    print("\nTeste de listagem de unidades de medida:")
    print("Número de unidades:", len(resultado_unidades))
    print("Primeira unidade:", resultado_unidades[0])

    # Teste de conceitos
    resultado_conceitos = listar_conceitos()
    print("\nTeste de listagem de conceitos:")
    print("Número de conceitos:", len(resultado_conceitos))
    print("Primeiro conceito:", resultado_conceitos[0])

    # Teste de fontes
    resultado_fontes = listar_fontes()
    print("\nTeste de listagem de fontes:")
    print("Número de fontes:", len(resultado_fontes))
    print("Primeira fonte:", resultado_fontes[0])

    # Teste de domínios
    resultado_dominios = listar_dominios()
    print("\nTeste de listagem de domínios:")
    print("Número de domínios:", len(resultado_dominios))
    print("Primeiro domínio:", resultado_dominios[0])

if __name__ == "__main__":
    asyncio.run(main())