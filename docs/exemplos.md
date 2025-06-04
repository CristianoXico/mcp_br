# Exemplos de Uso do MCP-BR

Este documento contém exemplos de como utilizar as ferramentas disponíveis no servidor MCP-BR.

## Exemplos de Uso com Cliente MCP

### Buscar Localidade

Para buscar informações sobre uma localidade pelo nome:

```python
# Exemplo de chamada da ferramenta buscar_localidade
resultado = await client.call_tool("buscar_localidade", {"nome": "São Paulo"})
print(resultado)
```

Exemplo de resposta:
```json
{
  "tipo": "municipio",
  "nome": "São Paulo",
  "estado": "SP",
  "codigo_ibge": "3550308",
  "populacao": 12325232,
  "area": 1521.11,
  "densidade": 8100.33,
  "regiao": "Sudeste"
}
```

### Gerar Relatório

Para gerar um relatório completo sobre uma localidade:

```python
# Exemplo de chamada da ferramenta gerar_relatorio com formato texto
relatorio_texto = await client.call_tool("gerar_relatorio", {
    "nome_localidade": "Rio de Janeiro",
    "formato": "texto"
})
print(relatorio_texto)

# Exemplo de chamada da ferramenta gerar_relatorio com formato json
relatorio_json = await client.call_tool("gerar_relatorio", {
    "nome_localidade": "Rio de Janeiro",
    "formato": "json"
})
print(relatorio_json)
```

Exemplo de resposta em formato texto:
```
RELATÓRIO: Rio de Janeiro (RJ)
=================================

INFORMAÇÕES GERAIS:
- Tipo: Município
- Estado: Rio de Janeiro (RJ)
- Região: Sudeste
- Código IBGE: 3304557
- População: 6,747,815 habitantes
- Área: 1,200.18 km²
- Densidade Demográfica: 5,622.57 hab/km²

DADOS SOCIOECONÔMICOS:
- PIB: R$ 364.5 bilhões
- PIB per capita: R$ 54,025.00
- IDH: 0.799 (Alto)
- Taxa de Escolarização: 97.5%
- Taxa de Desemprego: 14.2%

...
```

### Buscar Dados Demográficos

Para buscar dados demográficos de uma localidade pelo código IBGE:

```python
# Exemplo de chamada da ferramenta buscar_dados_demograficos
dados = await client.call_tool("buscar_dados_demograficos", {"codigo_ibge": "3550308"})
print(dados)
```

Exemplo de resposta:
```json
{
  "codigo_ibge": "3550308",
  "nome": "São Paulo",
  "populacao": {
    "total": 12325232,
    "urbana": 12252023,
    "rural": 73209,
    "homens": 5924871,
    "mulheres": 6400361
  },
  "densidade": 8100.33,
  "area": 1521.11,
  "taxa_crescimento": 0.7,
  "piramide_etaria": {
    "0-14": 19.4,
    "15-29": 23.7,
    "30-59": 42.8,
    "60+": 14.1
  }
}
```

### Buscar Dados Socioeconômicos

Para buscar dados socioeconômicos de uma localidade pelo código IBGE:

```python
# Exemplo de chamada da ferramenta buscar_dados_socioeconomicos
dados = await client.call_tool("buscar_dados_socioeconomicos", {"codigo_ibge": "3550308"})
print(dados)
```

Exemplo de resposta:
```json
{
  "codigo_ibge": "3550308",
  "nome": "São Paulo",
  "pib": {
    "total": 699.3,
    "per_capita": 56571.39,
    "crescimento": 2.1
  },
  "idh": 0.805,
  "educacao": {
    "taxa_escolarizacao": 96.1,
    "ideb": 6.5
  },
  "trabalho": {
    "taxa_desemprego": 13.2,
    "renda_media": 1789.25
  },
  "saude": {
    "expectativa_vida": 76.3,
    "mortalidade_infantil": 11.2
  }
}
```

## Exemplos de Uso Direto das Funções

Se você estiver utilizando as funções diretamente no código Python, sem o servidor MCP, aqui estão alguns exemplos:

### Buscar Informações de Localidade

```python
from tools.busca_localidade import buscar_info_localidade

async def exemplo():
    info = await buscar_info_localidade("São Paulo")
    print(info)

# Execute a função assíncrona
import asyncio
asyncio.run(exemplo())
```

### Gerar Relatório Completo

```python
from tools.relatorio_localidade import gerar_relatorio_completo, exibir_relatorio_texto

async def exemplo():
    relatorio = await gerar_relatorio_completo("Rio de Janeiro")
    
    # Exibir como texto formatado
    texto = exibir_relatorio_texto(relatorio)
    print(texto)
    
    # Ou trabalhar com os dados em formato JSON
    print(relatorio)

# Execute a função assíncrona
import asyncio
asyncio.run(exemplo())
```

### Buscar Dados Demográficos

```python
from tools.busca_localidade import buscar_dados_demograficos

async def exemplo():
    # Código IBGE de São Paulo
    dados = await buscar_dados_demograficos("3550308")
    print(dados)

# Execute a função assíncrona
import asyncio
asyncio.run(exemplo())
```

### Buscar Dados Socioeconômicos

```python
from tools.busca_localidade import buscar_dados_socioeconomicos

async def exemplo():
    # Código IBGE de São Paulo
    dados = await buscar_dados_socioeconomicos("3550308")
    print(dados)

# Execute a função assíncrona
import asyncio
asyncio.run(exemplo())
```
