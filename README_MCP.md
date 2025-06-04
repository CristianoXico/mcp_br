# MCP-BR: Integração com Model Context Protocol

## Visão Geral

Este documento descreve a integração do projeto MCP-BR com o Model Context Protocol (MCP), permitindo que modelos de linguagem e outros clientes MCP interajam com dados sobre localidades brasileiras.

## O que é o MCP?

O Model Context Protocol (MCP) é um protocolo que permite a comunicação entre modelos de linguagem e ferramentas externas. Ele define um padrão para expor funcionalidades como ferramentas (tools) e recursos (resources) que podem ser utilizados pelos modelos.

## Servidor MCP-BR

O servidor MCP-BR implementa o protocolo MCP para expor as funcionalidades do projeto MCP-BR, como busca de localidades, geração de relatórios e acesso a dados demográficos e socioeconômicos.

### Instalação

Para instalar as dependências necessárias para o servidor MCP-BR, execute:

```bash
pip install -r requirements.txt
```

### Execução

Para iniciar o servidor MCP-BR, execute:

```bash
python mcp_server.py
```

O servidor será iniciado e estará pronto para receber conexões de clientes MCP.

## Funcionalidades Expostas

O servidor MCP-BR expõe as seguintes funcionalidades:

### Ferramentas (Tools)

1. **buscar_localidade**: Busca localidades brasileiras (estados, municípios, etc.) pelo nome
2. **gerar_relatorio**: Gera um relatório completo sobre uma localidade brasileira
3. **buscar_dados_demograficos**: Busca dados demográficos de uma localidade pelo código IBGE
4. **buscar_dados_socioeconomicos**: Busca dados socioeconômicos de uma localidade pelo código IBGE

### Recursos (Resources)

1. **Sobre o MCP-BR**: Informações sobre o projeto MCP-BR
2. **Exemplos de Uso**: Exemplos de como usar as ferramentas do MCP-BR

## Documentação

Para mais informações sobre o servidor MCP-BR e suas funcionalidades, consulte:

- [Documentação do Servidor MCP-BR](docs/mcp_server.md)
- [Sobre o MCP-BR](docs/sobre.md)
- [Exemplos de Uso](docs/exemplos.md)

## Integração com Clientes MCP

### Exemplo de Cliente Python

Aqui está um exemplo simples de como utilizar o servidor MCP-BR com um cliente MCP em Python:

```python
import asyncio
from mcp.client import Client
from mcp import stdio_client

async def main():
    # Conectar ao servidor MCP-BR via stdio
    async with stdio_client() as (read_stream, write_stream):
        # Criar o cliente MCP
        client = Client()
        
        # Conectar o cliente ao transporte
        client.transport = (read_stream, write_stream)
        
        # Inicializar o cliente
        await client.initialize()
        
        # Listar as ferramentas disponíveis
        tools = await client.list_tools()
        print("Ferramentas disponíveis:", [tool.name for tool in tools])
        
        # Chamar a ferramenta buscar_localidade
        resultado = await client.call_tool("buscar_localidade", {"nome": "São Paulo"})
        print("Resultado da busca:", resultado)
        
        # Chamar a ferramenta gerar_relatorio
        relatorio = await client.call_tool("gerar_relatorio", {
            "nome_localidade": "Rio de Janeiro",
            "formato": "texto"
        })
        print("Relatório:", relatorio)
        
        # Listar os recursos disponíveis
        resources = await client.list_resources()
        print("Recursos disponíveis:", [resource.name for resource in resources])
        
        # Ler um recurso
        sobre = await client.read_resource("file://docs/sobre.md")
        print("Sobre o MCP-BR:", sobre)

if __name__ == "__main__":
    asyncio.run(main())
```

### Integração com Modelos de Linguagem

Os modelos de linguagem que implementam o protocolo MCP podem se conectar ao servidor MCP-BR e utilizar suas funcionalidades para obter informações sobre localidades brasileiras.

## Desenvolvimento

### Adicionando Novas Ferramentas

Para adicionar uma nova ferramenta ao servidor MCP-BR, siga os seguintes passos:

1. Implemente a função que será exposta como ferramenta
2. Adicione a ferramenta à lista `tools` no arquivo `mcp_server.py`, especificando seu nome, descrição e esquema de entrada
3. Implemente o handler para a ferramenta no método `call_tool` da classe `McpBrServer`

### Adicionando Novos Recursos

Para adicionar um novo recurso ao servidor MCP-BR, siga os seguintes passos:

1. Crie o conteúdo do recurso
2. Adicione o recurso à lista `resources` no arquivo `mcp_server.py`, especificando seu URI, nome, descrição e tipo MIME
3. Adicione o conteúdo do recurso ao dicionário `recursos_conteudo`

## Contribuição

Contribuições para a integração do MCP-BR com o protocolo MCP são bem-vindas. Se você deseja contribuir, por favor:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request
