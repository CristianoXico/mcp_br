# Documentação do Servidor MCP-BR

## Visão Geral

O servidor MCP-BR implementa o protocolo Model Context Protocol (MCP) para expor as funcionalidades do projeto MCP-BR, permitindo que modelos de linguagem e outros clientes MCP interajam com dados sobre localidades brasileiras, incluindo informações demográficas, socioeconômicas e indicadores municipais.

## Requisitos

- Python 3.8+
- Pacote MCP versão 1.9.2 ou superior
- Dependências do projeto MCP-BR (conforme listadas em `requirements.txt`)

## Arquitetura

O servidor MCP-BR é implementado no arquivo `mcp_server.py` e segue a seguinte arquitetura:

1. **Definição de Ferramentas (Tools)**: Expõe funcionalidades do projeto como ferramentas MCP
2. **Definição de Recursos (Resources)**: Fornece documentação e informações adicionais
3. **Handlers**: Implementa a lógica para listar e chamar ferramentas, listar e ler recursos
4. **Servidor**: Inicializa e executa o servidor MCP usando comunicação via stdio

## Ferramentas Disponíveis

O servidor MCP-BR expõe as seguintes ferramentas:

### 1. buscar_localidade

Busca localidades brasileiras (estados, municípios, etc.) pelo nome.

**Parâmetros**:
- `nome` (string, obrigatório): Nome da localidade a ser buscada

**Exemplo de uso**:
```json
{
  "nome": "São Paulo"
}
```

**Retorno**:
Informações sobre a localidade encontrada, incluindo tipo (município, estado, região), código IBGE, população, etc.

### 2. gerar_relatorio

Gera um relatório completo sobre uma localidade brasileira.

**Parâmetros**:
- `nome_localidade` (string, obrigatório): Nome da localidade para gerar o relatório
- `formato` (string, opcional): Formato do relatório (texto, json). Padrão: "texto"

**Exemplo de uso**:
```json
{
  "nome_localidade": "Rio de Janeiro",
  "formato": "texto"
}
```

**Retorno**:
Um relatório detalhado sobre a localidade, incluindo dados demográficos, socioeconômicos e indicadores.

### 3. buscar_dados_demograficos

Busca dados demográficos de uma localidade pelo código IBGE.

**Parâmetros**:
- `codigo_ibge` (string, obrigatório): Código IBGE da localidade

**Exemplo de uso**:
```json
{
  "codigo_ibge": "3550308"
}
```

**Retorno**:
Dados demográficos da localidade, incluindo população, densidade demográfica, etc.

### 4. buscar_dados_socioeconomicos

Busca dados socioeconômicos de uma localidade pelo código IBGE.

**Parâmetros**:
- `codigo_ibge` (string, obrigatório): Código IBGE da localidade

**Exemplo de uso**:
```json
{
  "codigo_ibge": "3550308"
}
```

**Retorno**:
Dados socioeconômicos da localidade, incluindo PIB, IDH, renda per capita, etc.

## Recursos Disponíveis

O servidor MCP-BR expõe os seguintes recursos:

### 1. Sobre o MCP-BR

URI: `file://docs/sobre.md`

Contém informações gerais sobre o projeto MCP-BR, suas funcionalidades e fontes de dados.

### 2. Exemplos de Uso

URI: `file://docs/exemplos.md`

Contém exemplos de como usar as ferramentas do MCP-BR.

## Implementação

### Classe McpBrServer

A classe `McpBrServer` é responsável por gerenciar os handlers do servidor MCP. Ela implementa os seguintes métodos:

- `setup_handlers()`: Registra os handlers para ferramentas e recursos
- `list_tools()`: Lista as ferramentas disponíveis
- `call_tool(name, parameters)`: Chama uma ferramenta com os parâmetros fornecidos
- `list_resources()`: Lista os recursos disponíveis
- `read_resource(uri)`: Lê o conteúdo de um recurso

### Função main()

A função `main()` é responsável por inicializar e executar o servidor MCP. Ela:

1. Configura o servidor MCP-BR
2. Inicializa o servidor usando stdio
3. Executa o servidor para processar mensagens

## Execução

Para iniciar o servidor MCP-BR, execute o seguinte comando:

```bash
python mcp_server.py
```

O servidor será iniciado e estará pronto para receber conexões de clientes MCP.

## Integração com Clientes MCP

Os clientes MCP podem se conectar ao servidor MCP-BR via stdio e utilizar as ferramentas e recursos disponíveis. Consulte a documentação do cliente MCP específico para obter instruções sobre como se conectar ao servidor.

## Depuração

O servidor MCP-BR registra informações de log no console. Para aumentar o nível de detalhamento dos logs, modifique a configuração de logging no arquivo `mcp_server.py`.
