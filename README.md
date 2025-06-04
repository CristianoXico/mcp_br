# MCP-BR

Projeto modular para integração de APIs do IBGE e outros serviços públicos via Model Context Protocol (MCP), compatível com Anthropic Claude Desktop/API e outros LLMs.

## Arquitetura

- **Modularização**: Cada domínio (ex: publicações, nomes) separado em:
  - `<dominio>_api.py`: Funções utilitárias para acesso à API externa (requisições HTTP, pooling, cache, autenticação).
  - `<dominio>_handlers.py`: Handlers MCP e lógica de negócio, usando os utilitários.
  - `<dominio>.py`: Façade/importador, apenas importa os handlers e documenta o padrão.
- **Utilitários centralizados**:
  - `cache_utils.py`: Cache thread-safe persistente.
  - `api_config.py`: URLs e tokens de APIs, usando variáveis de ambiente.
  - `logger.py`: Logger padronizado para todos os módulos.

## Exemplo de uso (handlers MCP)

```python
from tools.ibge_publicacoes import listar_publicacoes
result = listar_publicacoes(quantidade=5, pagina=1)

from tools.ibge_nomes import pesquisar_nomes
nomes = pesquisar_nomes("João")
```

## Configuração

- Configure variáveis de ambiente para tokens/URLs sensíveis:
  - `IBGE_API_KEY`, `DADOS_ABERTOS_TOKEN`, etc.
- Veja `api_config.py` para detalhes.

## Testes

- Testes de integração: `testar_apis_ibge.py` executa handlers e salva resultados.
- Recomenda-se criar testes unitários para cada handler/utilitário em `tests/`.

## Como contribuir

1. Siga o padrão de modularização para novos domínios.
2. Use sempre os utilitários centralizados de cache, configuração e logger.
3. Documente handlers e APIs com docstrings claras.
4. Adicione exemplos de uso e testes ao contribuir.

## Padrão Anthropic/MCP

- Estrutura compatível com Claude Desktop/API e outros LLMs via MCP.
- Configuração automática via `mcp.json` (se aplicável).
- Handlers retornam erros amigáveis, logs detalhados e uso eficiente de cache.

---

Para dúvidas ou sugestões, abra uma issue ou entre em contato com os mantenedores.
