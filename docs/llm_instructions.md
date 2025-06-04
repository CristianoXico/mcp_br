# Instruções para LLMs utilizando o MCP-BR

Este documento fornece instruções e exemplos para modelos de linguagem (LLMs) sobre como utilizar o servidor MCP-BR para acessar dados sobre localidades brasileiras, vulnerabilidade social e informações governamentais.

## Capacidades do MCP-BR

O MCP-BR é um servidor que fornece acesso a dados brasileiros através de uma API JSON-RPC. Ele oferece as seguintes funcionalidades:

1. **Busca de localidades brasileiras** (estados, municípios, regiões)
2. **Relatórios detalhados sobre localidades** (dados demográficos, socioeconômicos)
3. **Dados de transparência governamental** (auxílios, convênios, transferências)
4. **Indicadores de vulnerabilidade social** (saúde, educação, saneamento, segurança)
5. **Dados geográficos e estatísticos do IBGE**

## Métodos Disponíveis

### 1. `buscar_localidade`

Busca informações sobre uma localidade brasileira.

**Parâmetros:**
- `nome` (string): Nome da localidade a ser buscada
- `tipo` (string, opcional): Tipo de localidade ("municipio", "estado", "regiao")
- `uf` (string, opcional): Sigla do estado para filtrar municípios

**Exemplo:**
```json
{
  "method": "buscar_localidade",
  "params": {
    "nome": "São Paulo",
    "tipo": "municipio"
  }
}
```

**Quando usar:** Quando o usuário perguntar sobre informações básicas de um município, estado ou região brasileira.

### 2. `relatorio_localidade`

Gera um relatório detalhado sobre uma localidade.

**Parâmetros:**
- `nome` (string): Nome da localidade
- `tipo` (string): Tipo de localidade ("municipio", "estado", "regiao")
- `formato` (string, opcional): Formato do relatório ("completo", "resumido")
- `ano` (integer, opcional): Ano de referência dos dados

**Exemplo:**
```json
{
  "method": "relatorio_localidade",
  "params": {
    "nome": "Rio de Janeiro",
    "tipo": "municipio",
    "formato": "resumido"
  }
}
```

**Quando usar:** Quando o usuário solicitar informações detalhadas ou um relatório sobre uma localidade brasileira.

### 3. `dados_transparencia`

Obtém dados do Portal da Transparência para uma localidade.

**Parâmetros:**
- `municipio` (string): Nome do município
- `tipo_dado` (string): Tipo de dado ("auxilio", "bolsa_familia", "convenios", "transferencias")
- `ano` (integer, opcional): Ano de referência

**Exemplo:**
```json
{
  "method": "dados_transparencia",
  "params": {
    "municipio": "Salvador",
    "tipo_dado": "bolsa_familia",
    "ano": 2023
  }
}
```

**Quando usar:** Quando o usuário perguntar sobre dados de programas sociais, convênios ou transferências para um município.

### 4. `vulnerabilidade_social`

Obtém indicadores de vulnerabilidade social para um município.

**Parâmetros:**
- `municipio` (string): Nome do município
- `ano` (integer, opcional): Ano de referência (padrão: 2023)

**Exemplo:**
```json
{
  "method": "vulnerabilidade_social",
  "params": {
    "municipio": "Recife",
    "ano": 2023
  }
}
```

**Quando usar:** Quando o usuário perguntar sobre indicadores sociais, pobreza, educação, saúde, saneamento, segurança ou emprego em um município brasileiro.

## Estratégias para Uso Eficiente

1. **Determine a intenção do usuário** antes de escolher qual método chamar
2. **Extraia parâmetros específicos** da pergunta do usuário (nomes de municípios, anos, tipos de dados)
3. **Use o método mais específico** para a pergunta (não use `relatorio_localidade` se `buscar_localidade` for suficiente)
4. **Combine dados de múltiplas chamadas** quando necessário para responder perguntas complexas
5. **Formate os resultados** de maneira clara e concisa para o usuário

## Exemplos de Perguntas e Respostas

### Exemplo 1: Informação básica sobre município

**Pergunta do usuário:** "Qual é a população de Belo Horizonte?"

**Ação da LLM:** Chamar `buscar_localidade` com `nome="Belo Horizonte"` e `tipo="municipio"`

**Resposta:** "Belo Horizonte tem uma população estimada de 2.521.564 habitantes segundo os dados mais recentes do IBGE."

### Exemplo 2: Vulnerabilidade social

**Pergunta do usuário:** "Como está a situação de pobreza em Fortaleza?"

**Ação da LLM:** Chamar `vulnerabilidade_social` com `municipio="Fortaleza"`

**Resposta:** "Em Fortaleza, há aproximadamente 82.500 famílias em situação de vulnerabilidade e 36.200 pessoas em extrema pobreza. O programa Bolsa Família atende 45.300 famílias com um benefício médio de R$ 612,50."

### Exemplo 3: Dados de transparência

**Pergunta do usuário:** "Quanto Curitiba recebeu de transferências federais em 2023?"

**Ação da LLM:** Chamar `dados_transparencia` com `municipio="Curitiba"`, `tipo_dado="transferencias"` e `ano=2023`

**Resposta:** "Em 2023, Curitiba recebeu R$ 1,2 bilhões em transferências federais, sendo 45% para saúde, 30% para educação e 25% para outras áreas."

## Tratamento de Erros

Se o MCP-BR retornar um erro ou não conseguir encontrar os dados solicitados:

1. **Informe ao usuário** sobre a indisponibilidade dos dados
2. **Sugira alternativas** (outros municípios, períodos ou tipos de dados)
3. **Ofereça informações gerais** sobre o tópico quando dados específicos não estiverem disponíveis

## Considerações Éticas

1. **Não invente dados** quando eles não estiverem disponíveis
2. **Cite a fonte dos dados** (MCP-BR, IBGE, Portal da Transparência)
3. **Indique o período** a que os dados se referem
4. **Explique limitações** dos dados quando relevante
