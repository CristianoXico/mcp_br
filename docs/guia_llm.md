# Guia de Uso do MCP-BR para LLMs

## Ferramentas disponíveis

### gerar_relatorio
- **Descrição:** Gera um relatório completo de vulnerabilidade social para um município brasileiro.
- **Parâmetros:**
  - `municipio` (string, obrigatório): Nome do município.
  - `formato` (string, opcional): "texto" ou "json". Padrão: "texto".
- **Exemplo de chamada:**
  ```json
  {
    "municipio": "São José do Rio Preto",
    "formato": "texto"
  }
  ```
- Use esta ferramenta para responder perguntas sobre vulnerabilidade social de municípios brasileiros.

## Boas práticas
- Sempre valide se o parâmetro `municipio` foi informado.
- Prefira respostas concisas e claras.
- Em caso de erro, retorne uma mensagem amigável ao usuário.
