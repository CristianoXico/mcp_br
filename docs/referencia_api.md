# Referência da API do Servidor MCP-BR

Este documento fornece uma referência detalhada da API do servidor MCP-BR, incluindo todas as ferramentas, recursos e seus parâmetros.

## Ferramentas (Tools)

### buscar_localidade

Busca localidades brasileiras (estados, municípios, etc.) pelo nome.

**Endpoint MCP**: `call_tool("buscar_localidade", parameters)`

**Parâmetros**:

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| nome | string | Sim | Nome da localidade a ser buscada |

**Exemplo de Requisição**:
```json
{
  "nome": "São Paulo"
}
```

**Exemplo de Resposta**:
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

**Códigos de Erro**:
- `"error": "Parâmetro 'nome' é obrigatório"` - O parâmetro nome não foi fornecido
- `"error": "Localidade não encontrada"` - Nenhuma localidade foi encontrada com o nome fornecido

### gerar_relatorio

Gera um relatório completo sobre uma localidade brasileira.

**Endpoint MCP**: `call_tool("gerar_relatorio", parameters)`

**Parâmetros**:

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| nome_localidade | string | Sim | Nome da localidade para gerar o relatório |
| formato | string | Não | Formato do relatório (texto, json). Padrão: "texto" |

**Exemplo de Requisição**:
```json
{
  "nome_localidade": "Rio de Janeiro",
  "formato": "texto"
}
```

**Exemplo de Resposta (formato texto)**:
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

**Exemplo de Resposta (formato json)**:
```json
{
  "nome": "Rio de Janeiro",
  "tipo": "municipio",
  "estado": "Rio de Janeiro",
  "sigla_estado": "RJ",
  "regiao": "Sudeste",
  "codigo_ibge": "3304557",
  "populacao": 6747815,
  "area": 1200.18,
  "densidade": 5622.57,
  "dados_socioeconomicos": {
    "pib": 364.5,
    "pib_per_capita": 54025.00,
    "idh": 0.799,
    "taxa_escolarizacao": 97.5,
    "taxa_desemprego": 14.2
  },
  "periodo_info": {
    "periodo": "mes",
    "data_referencia": "2025-05-01",
    "data_geracao": "2025-06-02 20:15:30"
  }
}
```

**Códigos de Erro**:
- `"error": "Parâmetro 'nome_localidade' é obrigatório"` - O parâmetro nome_localidade não foi fornecido
- `"error": "Localidade não encontrada"` - Nenhuma localidade foi encontrada com o nome fornecido
- `"error": "Formato inválido"` - O formato fornecido não é válido (deve ser "texto" ou "json")

### buscar_dados_demograficos

Busca dados demográficos de uma localidade pelo código IBGE.

**Endpoint MCP**: `call_tool("buscar_dados_demograficos", parameters)`

**Parâmetros**:

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| codigo_ibge | string | Sim | Código IBGE da localidade |

**Exemplo de Requisição**:
```json
{
  "codigo_ibge": "3550308"
}
```

**Exemplo de Resposta**:
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

**Códigos de Erro**:
- `"error": "Parâmetro 'codigo_ibge' é obrigatório"` - O parâmetro codigo_ibge não foi fornecido
- `"error": "Código IBGE inválido"` - O código IBGE fornecido não é válido
- `"error": "Dados demográficos não encontrados"` - Não foram encontrados dados demográficos para o código IBGE fornecido

### buscar_dados_socioeconomicos

Busca dados socioeconômicos de uma localidade pelo código IBGE.

**Endpoint MCP**: `call_tool("buscar_dados_socioeconomicos", parameters)`

**Parâmetros**:

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| codigo_ibge | string | Sim | Código IBGE da localidade |

**Exemplo de Requisição**:
```json
{
  "codigo_ibge": "3550308"
}
```

**Exemplo de Resposta**:
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

**Códigos de Erro**:
- `"error": "Parâmetro 'codigo_ibge' é obrigatório"` - O parâmetro codigo_ibge não foi fornecido
- `"error": "Código IBGE inválido"` - O código IBGE fornecido não é válido
- `"error": "Dados socioeconômicos não encontrados"` - Não foram encontrados dados socioeconômicos para o código IBGE fornecido

## Recursos (Resources)

### Sobre o MCP-BR

**URI**: `file://docs/sobre.md`

**Método MCP**: `read_resource("file://docs/sobre.md")`

**Descrição**: Informações sobre o projeto MCP-BR, suas funcionalidades e fontes de dados.

**Tipo de Conteúdo**: `text/markdown`

### Exemplos de Uso

**URI**: `file://docs/exemplos.md`

**Método MCP**: `read_resource("file://docs/exemplos.md")`

**Descrição**: Exemplos de como usar as ferramentas do MCP-BR.

**Tipo de Conteúdo**: `text/markdown`

## Métodos do Protocolo MCP

### list_tools

Lista todas as ferramentas disponíveis no servidor MCP-BR.

**Método MCP**: `list_tools()`

**Parâmetros**: Nenhum

**Exemplo de Resposta**:
```json
{
  "tools": [
    {
      "name": "buscar_localidade",
      "description": "Busca localidades brasileiras (estados, municípios, etc.) pelo nome",
      "inputSchema": {
        "type": "object",
        "properties": {
          "nome": {
            "type": "string",
            "description": "Nome da localidade a ser buscada"
          }
        },
        "required": ["nome"]
      }
    },
    {
      "name": "gerar_relatorio",
      "description": "Gera um relatório completo sobre uma localidade brasileira",
      "inputSchema": {
        "type": "object",
        "properties": {
          "nome_localidade": {
            "type": "string",
            "description": "Nome da localidade para gerar o relatório"
          },
          "formato": {
            "type": "string",
            "description": "Formato do relatório (texto, json)",
            "enum": ["texto", "json"],
            "default": "texto"
          }
        },
        "required": ["nome_localidade"]
      }
    },
    ...
  ]
}
```

### call_tool

Chama uma ferramenta específica com os parâmetros fornecidos.

**Método MCP**: `call_tool(name, parameters)`

**Parâmetros**:
- `name` (string): Nome da ferramenta a ser chamada
- `parameters` (object): Parâmetros para a chamada da ferramenta

**Exemplo de Requisição**:
```json
{
  "name": "buscar_localidade",
  "parameters": {
    "nome": "São Paulo"
  }
}
```

**Exemplo de Resposta**:
```json
{
  "result": {
    "content": {
      "tipo": "municipio",
      "nome": "São Paulo",
      "estado": "SP",
      "codigo_ibge": "3550308",
      "populacao": 12325232,
      "area": 1521.11,
      "densidade": 8100.33,
      "regiao": "Sudeste"
    },
    "content_type": "application/json"
  }
}
```

### list_resources

Lista todos os recursos disponíveis no servidor MCP-BR.

**Método MCP**: `list_resources()`

**Parâmetros**: Nenhum

**Exemplo de Resposta**:
```json
{
  "resources": [
    {
      "uri": "file://docs/sobre.md",
      "name": "Sobre o MCP-BR",
      "description": "Informações sobre o projeto MCP-BR",
      "mimeType": "text/markdown"
    },
    {
      "uri": "file://docs/exemplos.md",
      "name": "Exemplos de Uso",
      "description": "Exemplos de como usar as ferramentas do MCP-BR",
      "mimeType": "text/markdown"
    }
  ]
}
```

### read_resource

Lê o conteúdo de um recurso específico.

**Método MCP**: `read_resource(uri)`

**Parâmetros**:
- `uri` (string): URI do recurso a ser lido

**Exemplo de Requisição**:
```json
{
  "uri": "file://docs/sobre.md"
}
```

**Exemplo de Resposta**:
```json
{
  "contents": {
    "content": "# MCP-BR\n\nO MCP-BR é um projeto que fornece informações sobre localidades brasileiras...",
    "content_type": "text/markdown"
  }
}
```

## Códigos de Status e Erros

O servidor MCP-BR pode retornar os seguintes códigos de erro:

| Código | Descrição |
|--------|-----------|
| `"error": "Ferramenta '{name}' não encontrada"` | A ferramenta solicitada não existe |
| `"error": "Parâmetro 'X' é obrigatório"` | Um parâmetro obrigatório não foi fornecido |
| `"error": "Recurso '{uri}' não encontrado"` | O recurso solicitado não existe |
| `"error": "Localidade não encontrada"` | A localidade solicitada não foi encontrada |
| `"error": "Código IBGE inválido"` | O código IBGE fornecido não é válido |
| `"error": "Formato inválido"` | O formato solicitado não é válido |

## Limitações e Considerações

- O servidor MCP-BR é projetado para comunicação via stdio, o que o torna adequado para integração com modelos de linguagem e outros clientes MCP.
- As respostas podem variar em tamanho, especialmente para relatórios de localidades grandes.
- O servidor não implementa autenticação ou autorização, portanto, deve ser usado em ambientes confiáveis.
- As consultas a dados demográficos e socioeconômicos podem levar algum tempo para serem processadas, dependendo da complexidade dos dados solicitados.
