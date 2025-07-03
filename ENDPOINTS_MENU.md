# Cardápio de Endpoints Integrados MCP-BR

Este arquivo documenta todos os principais endpoints já integrados no MCP-BR, organizados por domínio/tema. O objetivo é servir como referência para LLMs e usuários sobre quais informações estão disponíveis e como consultá-las.

## Como utilizar este cardápio
- Cada item lista: **nome da função**, **descrição do que retorna**, **parâmetros principais** e **exemplo de chamada**.
- Para consumir estes dados, utilize as funções Python correspondentes, geralmente disponíveis nos módulos da pasta `tools/`.

---

## Transparência (Portal da Transparência)

### Auxílio Emergencial
- **listar_auxilios_emergenciais(pagina: int = 1, tamanhoPagina: int = 10) -> list**
  - Lista os beneficiários do Auxílio Emergencial.
  - **Parâmetros:**
    - `pagina` (int, opcional): Página da consulta (default: 1)
    - `tamanhoPagina` (int, opcional): Quantidade de resultados por página (default: 10)
  - **Exemplo de chamada:**
    ```python
    resultado = listar_auxilios_emergenciais(pagina=1, tamanhoPagina=5)
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    [
      {"nome": "Maria da Silva", "cpf": "***.123.456-**", "municipio": "Campinas", "valor": 600.0},
      {"nome": "João Souza", "cpf": "***.987.654-**", "municipio": "Campinas", "valor": 600.0}
    ]
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Dados indisponíveis ou parâmetro inválido."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 400: Parâmetros inválidos
    - 500: Erro interno/indisponibilidade do serviço
  - **Dicas de uso:**
    - Utilize paginação para grandes volumes de dados.
    - O CPF pode vir parcialmente mascarado por questões de privacidade.

### Bolsa Família / Auxílio Brasil
- **listar_bolsa_familia(pagina: int = 1, tamanhoPagina: int = 10) -> list**
  - Lista os beneficiários do Bolsa Família / Auxílio Brasil.
  - **Parâmetros:**
    - `pagina` (int, opcional): Página da consulta (default: 1)
    - `tamanhoPagina` (int, opcional): Quantidade de resultados por página (default: 10)
  - **Exemplo de chamada:**
    ```python
    resultado = listar_bolsa_familia(pagina=1, tamanhoPagina=5)
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    [
      {"nome": "Ana Pereira", "nis": "12345678900", "municipio": "São Paulo", "valor": 400.0},
      {"nome": "Carlos Lima", "nis": "98765432100", "municipio": "São Paulo", "valor": 400.0}
    ]
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Dados indisponíveis ou parâmetro inválido."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 400: Parâmetros inválidos
    - 500: Erro interno/indisponibilidade do serviço
  - **Dicas de uso:**
    - Utilize paginação para grandes volumes de dados.
    - O NIS identifica unicamente o beneficiário.

### Servidores Públicos Federais
- **listar_servidores(pagina: int = 1, tamanhoPagina: int = 10) -> list**
  - Lista servidores públicos federais.
  - **Parâmetros:**
    - `pagina` (int, opcional): Página da consulta (default: 1)
    - `tamanhoPagina` (int, opcional): Quantidade de resultados por página (default: 10)
  - **Exemplo de chamada:**
    ```python
    resultado = listar_servidores(pagina=1, tamanhoPagina=5)
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    [
      {"nome": "José Almeida", "cpf": "***.321.654-**", "cargo": "Analista", "orgao": "Ministério da Economia"},
      {"nome": "Paula Souza", "cpf": "***.654.321-**", "cargo": "Técnico", "orgao": "Ministério da Saúde"}
    ]
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Dados indisponíveis ou parâmetro inválido."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 400: Parâmetros inválidos
    - 500: Erro interno/indisponibilidade do serviço
  - **Dicas de uso:**
    - O CPF vem mascarado por questões de privacidade.
    - Use filtros adicionais (por órgão, cargo, etc.) se disponíveis.

### Contratos do Governo Federal
- **listar_contratos(pagina: int = 1, tamanhoPagina: int = 10) -> list**
  - Lista contratos do governo federal.
  - **Parâmetros:**
    - `pagina` (int, opcional): Página da consulta (default: 1)
    - `tamanhoPagina` (int, opcional): Quantidade de resultados por página (default: 10)
  - **Exemplo de chamada:**
    ```python
    resultado = listar_contratos(pagina=1, tamanhoPagina=5)
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    [
      {"id": "12345", "orgao": "Ministério da Educação", "objeto": "Aquisição de livros", "valor": 15000.0},
      {"id": "67890", "orgao": "Ministério da Saúde", "objeto": "Compra de equipamentos", "valor": 50000.0}
    ]
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Dados indisponíveis ou parâmetro inválido."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 400: Parâmetros inválidos
    - 500: Erro interno/indisponibilidade do serviço
  - **Dicas de uso:**
    - Utilize paginação para grandes volumes de dados.
    - Use filtros por órgão, objeto ou período se disponíveis.

---

## IBGE (Instituto Brasileiro de Geografia e Estatística)

### Localidades
- **buscar_municipio_por_codigo(codigo_municipio: str) -> dict**
  - Busca informações detalhadas de um município pelo código IBGE.
  - **Parâmetros:**
    - `codigo_municipio` (str): Código IBGE do município. Exemplo: "3509502".
  - **Exemplo de chamada:**
    ```python
    resultado = buscar_municipio_por_codigo("3509502")
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    {
      "id": 3509502,
      "nome": "Campinas",
      "microrregiao": {
        "id": 3501,
        "nome": "Campinas",
        "mesorregiao": {
          "id": 3501,
          "nome": "Campinas",
          "UF": {"id": 35, "sigla": "SP", "nome": "São Paulo"}
        }
      },
      "regiao-imediata": {"id": 350005, "nome": "Campinas"},
      "regiao-intermediaria": {"id": 3508, "nome": "Campinas"}
    }
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Município não encontrado para o código informado."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 404: Município não encontrado
    - 500: Erro interno/indisponibilidade do serviço IBGE
  - **Possíveis erros:**
    - Código inválido (não numérico ou inexistente)
    - Município não encontrado
    - Falha de conexão com a API IBGE
    - Limite de requisições excedido
  - **Dicas de uso:**
    - O código IBGE é sempre numérico e pode ser obtido com `listar_municipios()` ou pelo nome usando `buscar_municipio_por_nome()`.
    - Para evitar bloqueios, respeite limites de requisições e utilize cache/localstorage quando possível.
    - Em caso de erro de rede, tente novamente após alguns segundos.

- **buscar_municipio_por_nome(nome_municipio: str) -> list**
  - Busca informações detalhadas de um município pelo nome.
  - **Parâmetros:**
    - `nome_municipio` (str): Nome oficial do município. Exemplo: "Campinas".
  - **Exemplo de chamada:**
    ```python
    resultado = buscar_municipio_por_nome("Campinas")
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    [
      {
        "id": 3509502,
        "nome": "Campinas",
        "microrregiao": {
          "id": 3501,
          "nome": "Campinas",
          "mesorregiao": {
            "id": 3501,
            "nome": "Campinas",
            "UF": {"id": 35, "sigla": "SP", "nome": "São Paulo"}
          }
        },
        "regiao-imediata": {"id": 350005, "nome": "Campinas"},
        "regiao-intermediaria": {"id": 3508, "nome": "Campinas"}
      }
    ]
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Município não encontrado para o nome informado."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 404: Município não encontrado
    - 500: Erro interno/indisponibilidade do serviço IBGE
  - **Possíveis erros:**
    - Nome inexistente
    - Nome ambíguo (pode retornar mais de um município)
    - Falha de conexão com a API IBGE
    - Limite de requisições excedido
  - **Dicas de uso:**
    - O nome deve ser oficial e pode ser obtido em listagens do IBGE.
    - Retorna lista de municípios; use o campo "id" para obter detalhes únicos.
    - Em caso de erro de rede, tente novamente após alguns segundos.
    - Para nomes genéricos, refine a busca com UF ou outros filtros se disponível.

  - **Parâmetros:**
    - `nome_municipio` (str): Nome oficial do município. Exemplo: "Campinas".
  - **Exemplo de chamada:**
    ```python
    resultado = buscar_municipio_por_nome("Campinas")
    print(resultado)
    ```
  - **Exemplo de resposta (sucesso):**
    ```json
    {
      "id": 3509502,
      "nome": "Campinas",
      "microrregiao": {
        "id": 3501,
        "nome": "Campinas",
        "mesorregiao": {
          "id": 3501,
          "nome": "Campinas",
          "UF": {"id": 35, "sigla": "SP", "nome": "São Paulo"}
        }
      },
      "regiao-imediata": {"id": 350005, "nome": "Campinas"},
      "regiao-intermediaria": {"id": 3508, "nome": "Campinas"}
    }
    ```
  - **Exemplo de resposta (erro):**
    ```json
    {"erro": "Município não encontrado para o nome informado."}
    ```
  - **Status HTTP esperados:**
    - 200: Sucesso
    - 404: Município não encontrado
    - 500: Erro interno/indisponibilidade do serviço IBGE
  - **Possíveis erros:**
    - Nome inexistente ou grafia incorreta
    - Município não encontrado
    - Falha de conexão com a API IBGE
    - Limite de requisições excedido
  - **Dicas de uso:**
    - O nome deve ser oficial e pode ser consultado na lista de municípios (`listar_municipios()`).
    - Para nomes ambíguos ou repetidos, refine a busca informando o estado (quando disponível na função).
    - Utilize cache/localstorage para evitar consultas repetidas e respeitar limites de requisição.
    - Em caso de erro de rede, tente novamente após alguns segundos.

  - Parâmetros: `nome_municipio` (ex: "Campinas")
  - Exemplo: `buscar_municipio_por_nome("Campinas")`

### Nomes
- **api_get_nomes(nome: str) -> list**
  - Retorna estatísticas e dados sobre nomes próprios no Brasil.
  - Parâmetros: `nome` (ex: "Maria")
  - Exemplo: `api_get_nomes("Maria")`

### Agregados
- **api_get_agregados(id_agregado: str) -> dict**
  - Retorna dados agregados do IBGE por código.
  - Parâmetros: `id_agregado`
  - Exemplo: `api_get_agregados("6579")`

---

## Portal da Transparência
- **buscar_auxilios_por_municipio(codigo_municipio: str) -> list**
  - Lista auxílios pagos em determinado município.
- **buscar_bolsa_familia_por_municipio(codigo_municipio: str) -> list**
  - Lista pagamentos do Bolsa Família por município.
- **buscar_contratos_por_orgao(orgao: str) -> list**
  - Lista contratos de um órgão público.

---

## Dados Abertos
- **listar_dados_abertos() -> list**
  - Lista todos os conjuntos de dados abertos disponíveis.
- **buscar_dados_por_id(id_dataset: str) -> dict**
  - Busca detalhes de um dataset por ID.
- **listar_recursos(id_dataset: str) -> list**
  - Lista recursos (arquivos, APIs) de um dataset.
- **listar_grupos() -> list**
  - Lista grupos temáticos de datasets.
- **listar_organizacoes() -> list**
  - Lista organizações fornecedoras de dados.
- **buscar_dados_por_tag(tag: str) -> list**
  - Busca datasets por tag.

---

## Vulnerabilidade Social
- **analisar_vulnerabilidade(municipio: str) -> dict**
  - Analisa indicadores sociais e econômicos de um município.

---

## Educação, Saúde, Saneamento, Segurança, Empresas
- Cada domínio possui funções análogas para busca por município, listagem de indicadores, séries históricas, etc.
- Consulte os módulos: `educacao.py`, `sus.py`, `snis.py`, `seguranca.py`, `cnpj.py` para detalhes.

---

## Observações
- Este cardápio é um guia de alto nível. Para detalhes de parâmetros, consulte os docstrings das funções ou a documentação inline de cada módulo.
- Novos endpoints podem ser adicionados conforme a evolução do projeto.
