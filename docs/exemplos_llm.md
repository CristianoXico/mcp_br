# Exemplos Avançados de Uso do MCP-BR para LLMs

## 1. Gerar relatório em texto
<tool_call name="gerar_relatorio">
  <param name="municipio">Fortaleza</param>
  <param name="formato">texto</param>
</tool_call>

## 2. Gerar relatório em JSON
<tool_call name="gerar_relatorio">
  <param name="municipio">São Paulo</param>
  <param name="formato">json</param>
</tool_call>

## 3. Ler FAQ
<resource_read uri="resource://faq" />

## 4. Lidar com erro de município não encontrado
<tool_call name="gerar_relatorio">
  <param name="municipio">Cidade Inexistente</param>
  <param name="formato">texto</param>
</tool_call>
<!-- Esperado: resposta amigável de erro. -->

## 5. Uso eficiente
- Prefira nomes completos de municípios.
- Se receber erro, consulte o FAQ.
- Evite pedir o mesmo relatório repetidas vezes (resultados podem ser cacheados).
- Sempre complemente o relatório com informações relevantes e um resumo de análise sobre o municipio em questão e o contexto da pergunta.
