# Desafio Bootcamp

Este repositório contém uma suíte de testes automatizados em Python para a API `https://compassuol.serverest.dev/`.

## Visão Geral

O objetivo é validar a API ServeRest por meio de testes de aceitação e verificação de comportamento em:

- cadastro, busca, atualização e exclusão de usuários
- autenticação de usuários
- cadastro e atualização de produtos com autorização de administrador
- validações de erro e comportamento de segurança

## Estrutura do Repositório

- `tests/test_api_compass.py` - suíte de testes principal
- `PLANO-DE-TESTES.md` - plano de testes completo

## Requisitos

- Python 3.10+ (ou compatível)
- `requests`
- `pytest`
- `pytest-cov`

> É recomendado executar os testes em um ambiente virtual isolado.

## Instalação

No diretório do projeto:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests pytest pytest-cov
```

## Como rodar os testes

### Executar toda a suíte

```bash
pytest tests/test_api_compass.py -v
```

### Executar um teste específico

```bash
pytest tests/test_api_compass.py::TestLogin::test_login -v
```

### Executar cobertura

```bash
pytest --cov=tests --cov-report=term-missing tests/test_api_compass.py -q
```

## Metodologia de cobertura

A cobertura foi calculada com `pytest-cov` usando a métrica de cobertura de instruções (statement coverage).

Comando utilizado:

```bash
pytest --cov=tests --cov-report=term-missing tests/test_api_compass.py -q
```

## Resultado de cobertura

- Cobertura total atingida: **86%**

## Cenários cobertos

A suíte atual cobre:

- cadastro de usuário
- login válido e inválido
- busca de usuário por ID
- atualização de usuário
- exclusão de usuário
- listagem de produtos
- cadastro de produto sem token
- cadastro de produto com token de administrador
- busca de produto por ID
- atualização de produto com token de administrador

## Cenários fora de cobertura

Os seguintes cenários ainda não estão cobertos pela suíte atual:

- caminhos alternativos de falha em `criar_login()` e `obter_token_administrador()`, como retries por `503` ou falha de criação de usuário
- caminho de retry de `criar_produto_com_token()` para `401` e `503` quando a API está instável
- `excluir_produto()` no arquivo `tests/test_api_compass.py` não está executado porque o método não começa com `test_`
- exclusão de produto via API com token de administrador
- validação de nome duplicado para produtos

Esses pontos representam oportunidades para aumentar a cobertura e testar mais profundamente o comportamento de falha da API.

## Organização dos testes em `tests/test_api_compass.py`

- `TestUsuarioCadastro`
  - `test_get_users`
  - `test_cadastrar_usuario`
  - `test_cadastrar_usuario_duplicado`
  - `test_cadastrar_usuario_com_campos_vazios`

- `TestLogin`
  - `test_login`
  - `test_login_senha_errada`
  - `test_login_com_email_inexistente`
  - `test_login_com_campos_vazios`

- `TestUsuarioOperacoes`
  - `test_buscar_usuario_por_id`
  - `test_buscar_usuario_por_id_invalido`
  - `test_atualizar_usuario`
  - `test_deletar_usuario`

- `TestProduto`
  - `test_get_produtos`
  - `test_cadastrar_produto_sem_token`
  - `test_cadastrar_produto_com_token`
  - `test_buscar_produto_por_id`
  - `test_atualizar_produto`

## Notas adicionais

- `tests/test_api_compass.py` usa `requests` para executar chamadas reais à API.
- A suite valida tanto fluxos de sucesso quanto casos de erro esperados.
- A cobertura pode ser estendida adicionando testes para exclusão de produto, criação de carrinho e comportamento de produto duplicado.

## Referências

- Plano de testes: `PLANO-DE-TESTES.md`

---

**Última atualização:** 2026-06-15
