# Guia de Integração do Servidor MCP-BR

Este guia explica como integrar o servidor MCP-BR com outras aplicações e sistemas.

## Integração com Aplicações Python

### Usando o Cliente de Exemplo

O projeto inclui um cliente de exemplo (`mcp_client_exemplo.py`) que demonstra como se conectar ao servidor MCP-BR e utilizar suas funcionalidades. Este cliente pode ser usado como base para desenvolver sua própria integração.

```python
import asyncio
from mcp_client_exemplo import McpBrClient

async def exemplo():
    # Criar e conectar o cliente
    client = McpBrClient()
    await client.connect()
    
    try:
        # Chamar uma ferramenta
        resultado = await client.call_tool("buscar_localidade", {"nome": "São Paulo"})
        print(resultado)
    finally:
        # Desconectar o cliente
        await client.disconnect()

# Executar o exemplo
asyncio.run(exemplo())
```

### Integração Direta com a Biblioteca MCP

Se você preferir integrar diretamente com a biblioteca MCP, aqui está um exemplo de como fazer isso:

```python
import asyncio
import subprocess
import sys
from mcp.client import Client
from mcp import stdio_client

async def main():
    # Iniciar o servidor MCP-BR como um processo separado
    server_process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )
    
    try:
        # Conectar ao servidor via stdio
        read_stream, write_stream = await stdio_client(
            server_process.stdout, server_process.stdin
        )
        
        # Criar o cliente MCP
        client = Client()
        
        # Conectar o cliente ao transporte
        client.transport = (read_stream, write_stream)
        
        # Inicializar o cliente
        await client.initialize()
        
        # Usar as funcionalidades do servidor
        tools = await client.list_tools()
        print("Ferramentas disponíveis:", [tool.name for tool in tools])
        
        # Chamar uma ferramenta
        resultado = await client.call_tool("buscar_localidade", {"nome": "São Paulo"})
        print("Resultado:", resultado)
    finally:
        # Encerrar o processo do servidor
        server_process.terminate()
        await asyncio.sleep(0.5)
        if server_process.poll() is None:
            server_process.kill()

if __name__ == "__main__":
    asyncio.run(main())
```

## Integração com Modelos de Linguagem

### Configuração do Servidor para Modelos de Linguagem

Para integrar o servidor MCP-BR com modelos de linguagem, você precisa configurar o modelo para se comunicar com o servidor MCP. Isso geralmente envolve:

1. Iniciar o servidor MCP-BR
2. Configurar o modelo de linguagem para se conectar ao servidor
3. Permitir que o modelo utilize as ferramentas e recursos expostos pelo servidor

### Exemplo de Uso com Modelos de Linguagem

Aqui está um exemplo conceitual de como um modelo de linguagem pode interagir com o servidor MCP-BR:

```
Usuário: Quais são as informações disponíveis sobre a cidade de São Paulo?

Modelo: Vou buscar informações sobre São Paulo para você.

[O modelo chama a ferramenta buscar_localidade com o parâmetro "nome": "São Paulo"]

Modelo: São Paulo é o município mais populoso do Brasil, com aproximadamente 12,3 milhões de habitantes. É a capital do estado de São Paulo e está localizada na região Sudeste. O código IBGE da cidade é 3550308, e ela possui uma área de 1.521,11 km² com densidade demográfica de 8.100,33 hab/km².

Usuário: Pode me mostrar um relatório completo sobre a cidade?

Modelo: Claro, vou gerar um relatório completo sobre São Paulo.

[O modelo chama a ferramenta gerar_relatorio com os parâmetros "nome_localidade": "São Paulo", "formato": "texto"]

Modelo: Aqui está o relatório completo sobre São Paulo:

RELATÓRIO: São Paulo (SP)
=================================

INFORMAÇÕES GERAIS:
- Tipo: Município
- Estado: São Paulo (SP)
- Região: Sudeste
- Código IBGE: 3550308
- População: 12,325,232 habitantes
- Área: 1,521.11 km²
- Densidade Demográfica: 8,100.33 hab/km²

[... resto do relatório ...]
```

## Integração com Outras Linguagens

### Integração via Subprocess

Você pode integrar o servidor MCP-BR com aplicações escritas em outras linguagens usando comunicação via subprocess. Aqui está um exemplo conceitual em JavaScript:

```javascript
const { spawn } = require('child_process');
const readline = require('readline');

// Iniciar o servidor MCP-BR como um processo filho
const serverProcess = spawn('python', ['mcp_server.py'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

// Configurar leitura/escrita
const rl = readline.createInterface({
  input: serverProcess.stdout,
  output: serverProcess.stdin
});

// Enviar uma mensagem para o servidor
function sendMessage(message) {
  serverProcess.stdin.write(JSON.stringify(message) + '\n');
}

// Processar as respostas do servidor
rl.on('line', (line) => {
  const response = JSON.parse(line);
  console.log('Resposta do servidor:', response);
});

// Exemplo de uso
sendMessage({
  jsonrpc: '2.0',
  method: 'list_tools',
  id: 1
});

// Limpeza ao encerrar
process.on('exit', () => {
  serverProcess.kill();
});
```

### Integração via API Web

Para uma integração mais flexível, você pode considerar criar uma camada de API Web sobre o servidor MCP-BR. Isso permitiria que aplicações em qualquer linguagem se comunicassem com o servidor via HTTP.

Aqui está um exemplo de como implementar uma API Web usando Flask:

```python
from flask import Flask, request, jsonify
import asyncio
import json
from mcp_client_exemplo import McpBrClient

app = Flask(__name__)
client = None

@app.route('/api/tools', methods=['GET'])
def list_tools():
    tools = asyncio.run(client.list_tools())
    return jsonify([{
        'name': tool.name,
        'description': tool.description
    } for tool in tools])

@app.route('/api/tools/<name>', methods=['POST'])
def call_tool(name):
    parameters = request.json
    result = asyncio.run(client.call_tool(name, parameters))
    return jsonify(result)

@app.route('/api/resources', methods=['GET'])
def list_resources():
    resources = asyncio.run(client.list_resources())
    return jsonify([{
        'uri': resource.uri,
        'name': resource.name,
        'description': resource.description
    } for resource in resources])

@app.route('/api/resources/<path:uri>', methods=['GET'])
def read_resource(uri):
    uri = f"file://{uri}"
    content = asyncio.run(client.read_resource(uri))
    return jsonify(content)

if __name__ == '__main__':
    # Inicializar o cliente MCP-BR
    client = McpBrClient()
    asyncio.run(client.connect())
    
    # Iniciar o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # Desconectar o cliente ao encerrar
    asyncio.run(client.disconnect())
```

## Considerações de Segurança

Ao integrar o servidor MCP-BR com outras aplicações, considere as seguintes práticas de segurança:

1. **Validação de Entrada**: Valide todos os parâmetros recebidos antes de passá-los para o servidor MCP-BR
2. **Controle de Acesso**: Implemente mecanismos de autenticação e autorização se a API for exposta publicamente
3. **Limitação de Taxa**: Considere implementar limitação de taxa para evitar sobrecarga do servidor
4. **Logs e Monitoramento**: Mantenha logs detalhados das chamadas e monitore o uso do servidor

## Solução de Problemas

### Problemas Comuns e Soluções

1. **Erro de Conexão**:
   - Verifique se o servidor MCP-BR está em execução
   - Confirme que as portas ou pipes estão configurados corretamente

2. **Erro ao Chamar Ferramentas**:
   - Verifique se os parâmetros estão corretos e completos
   - Consulte os logs do servidor para obter mais detalhes sobre o erro

3. **Desempenho Lento**:
   - Considere otimizar as consultas ou implementar cache para resultados frequentes
   - Verifique se há gargalos de recursos (CPU, memória, rede)

### Logs e Depuração

O servidor MCP-BR registra informações de log que podem ser úteis para depuração. Por padrão, os logs são enviados para o console, mas você pode configurar o logging para gravar em um arquivo:

```python
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log"
)
```

## Exemplos Avançados

### Processamento em Lote

Se você precisa processar muitas localidades, considere implementar um processamento em lote para melhorar o desempenho:

```python
async def processar_lote(client, localidades):
    resultados = []
    for localidade in localidades:
        resultado = await client.call_tool("buscar_localidade", {"nome": localidade})
        resultados.append(resultado)
    return resultados
```

### Integração com Banco de Dados

Você pode integrar o servidor MCP-BR com um banco de dados para armazenar e consultar resultados:

```python
import sqlite3
import json

# Conectar ao banco de dados
conn = sqlite3.connect('localidades.db')
cursor = conn.cursor()

# Criar tabela para armazenar resultados
cursor.execute('''
CREATE TABLE IF NOT EXISTS localidades (
    nome TEXT PRIMARY KEY,
    dados TEXT,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Função para buscar ou atualizar dados
async def buscar_ou_atualizar(client, nome_localidade):
    # Verificar se já temos dados recentes
    cursor.execute('SELECT dados FROM localidades WHERE nome = ? AND data_atualizacao > datetime("now", "-1 day")', (nome_localidade,))
    resultado = cursor.fetchone()
    
    if resultado:
        # Usar dados do cache
        return json.loads(resultado[0])
    else:
        # Buscar novos dados
        dados = await client.call_tool("buscar_localidade", {"nome": nome_localidade})
        
        # Armazenar no banco de dados
        cursor.execute('INSERT OR REPLACE INTO localidades (nome, dados) VALUES (?, ?)',
                      (nome_localidade, json.dumps(dados)))
        conn.commit()
        
        return dados
```

## Próximos Passos

Após integrar o servidor MCP-BR com sua aplicação, considere os seguintes próximos passos:

1. **Testes Automatizados**: Desenvolva testes automatizados para garantir que a integração continue funcionando conforme esperado
2. **Monitoramento**: Implemente monitoramento para acompanhar o desempenho e a disponibilidade do servidor
3. **Documentação**: Mantenha a documentação atualizada com exemplos específicos para sua integração
4. **Feedback**: Colete feedback dos usuários para identificar áreas de melhoria
