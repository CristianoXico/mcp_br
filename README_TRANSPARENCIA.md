# Integração com o Portal da Transparência

Este módulo implementa a integração com as APIs do Portal da Transparência do Governo Federal Brasileiro.

## Características

- Acesso a todas as APIs do Portal da Transparência
- Implementação assíncrona com `httpx` e `asyncio`
- Cache local para evitar requisições repetidas
- Tratamento robusto de erros com fallback para dados de exemplo
- Limitador de taxa (rate limiter) para respeitar as restrições da API

## Limitações de Requisições

O Portal da Transparência impõe limites no número de requisições por minuto:

- **Período das 6:00 às 23:59**: 90 requisições por minuto
- **Período das 00:00 às 5:59**: 300 requisições por minuto

O módulo implementa um rate limiter que automaticamente:

1. Controla o número de requisições por minuto
2. Aguarda o tempo necessário entre requisições
3. Pausa a execução quando o limite é atingido
4. Ajusta automaticamente o limite com base no horário atual

## APIs Implementadas

### Auxílios Emergenciais
- `listar_auxilios_emergenciais()`: Lista beneficiários do Auxílio Emergencial
- `buscar_auxilios_por_municipio(codigoIbge)`: Busca beneficiários por município
- `buscar_auxilios_por_cpf_cnpj(cpfCnpj)`: Busca beneficiários por CPF/CNPJ

### Bolsa Família / Auxílio Brasil
- `listar_bolsa_familia()`: Lista beneficiários do Bolsa Família
- `buscar_bolsa_familia_por_municipio(codigoIbge, mesAno)`: Busca beneficiários por município
- `buscar_bolsa_familia_por_cpf_nis(cpfNis)`: Busca beneficiários por CPF/NIS

### Servidores
- `listar_servidores()`: Lista servidores públicos federais
- `buscar_servidor_por_cpf(cpf)`: Busca servidor por CPF
- `buscar_remuneracao_servidor(id, mesAno)`: Busca remuneração de servidor

### Contratos
- `listar_contratos()`: Lista contratos do governo federal
- `buscar_contrato_por_id(id)`: Busca contrato por ID
- `buscar_contratos_por_orgao(codigoOrgao)`: Busca contratos por órgão

### Licitações
- `listar_licitacoes()`: Lista licitações do governo federal
- `buscar_licitacao_por_id(id)`: Busca licitação por ID
- `buscar_licitacoes_por_orgao(codigoOrgao)`: Busca licitações por órgão

### CEIS (Cadastro de Empresas Inidôneas e Suspensas)
- `listar_ceis()`: Lista empresas no CEIS
- `buscar_ceis_por_cnpj(cnpj)`: Busca empresa no CEIS por CNPJ
- `buscar_ceis_por_nome(nomeEmpresa)`: Busca empresa no CEIS por nome

### CNEP (Cadastro Nacional de Empresas Punidas)
- `listar_cnep()`: Lista empresas no CNEP
- `buscar_cnep_por_cnpj(cnpj)`: Busca empresa no CNEP por CNPJ
- `buscar_cnep_por_nome(nomeEmpresa)`: Busca empresa no CNEP por nome

### Despesas
- `listar_despesas()`: Lista despesas do governo federal
- `buscar_despesa_por_id(id)`: Busca despesa por ID
- `buscar_despesas_por_orgao(codigoOrgao)`: Busca despesas por órgão

### Órgãos
- `listar_orgaos()`: Lista órgãos do governo federal
- `buscar_orgao_por_codigo(codigo)`: Busca órgão por código

### Emendas Parlamentares
- `listar_emendas()`: Lista emendas parlamentares
- `buscar_emenda_por_id(id)`: Busca emenda por ID
- `buscar_emendas_por_autor(autor)`: Busca emendas por autor

## Exemplo de Uso

```python
import asyncio
from tools.transparencia import listar_orgaos, buscar_contratos_por_orgao

async def exemplo():
    # Lista todos os órgãos do governo federal
    orgaos = await listar_orgaos()
    print(f"Total de órgãos: {len(orgaos.get('data', []))}")
    
    # Busca contratos do Ministério da Educação (código 26000)
    contratos = await buscar_contratos_por_orgao("26000")
    print(f"Total de contratos: {contratos.get('totalRegistros', 0)}")
    
    # Exibe os primeiros contratos
    for contrato in contratos.get('data', [])[:3]:
        print(f"Contrato: {contrato.get('objeto')} - Valor: R$ {contrato.get('valor')}")

# Executa o exemplo
asyncio.run(exemplo())
```

## Testes

Para executar os testes:

```bash
python -m pytest test_transparencia.py -v
```

Os testes incluem verificações para todas as principais APIs e demonstram o funcionamento do rate limiter.
