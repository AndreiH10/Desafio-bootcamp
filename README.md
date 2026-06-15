# Desafio Bootcamp

Este repositório contém uma suíte de testes automatizados em Python para a API `https://compassuol.serverest.dev/`.

## Conteúdo

- `tests/test_a.py`: conjunto de testes que cobrem cadastro, login, busca, atualização e exclusão de usuários.

## Requisitos

- Python 3.10+ (ou compatível)
- Biblioteca `requests`

> É recomendado executar os testes em um ambiente virtual isolado.

## Instalação

No diretório do projeto:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests
```

## Como rodar os testes

Execute os testes com `pytest` no arquivo `tests/test_a.py`:

```bash
pytest tests/test_a.py
```

Para rodar um teste específico, use o caminho da função:

```bash
pytest tests/test_a.py::test_login
```

## Estrutura de testes

O arquivo `tests/test_a.py` inclui casos para:

- `test_get_users`
- `test_cadastrar_usuario`
- `test_cadastrar_usuario_duplicado`
- `test_cadastrar_usuario_com_campos_vazios`
- `test_login`
- `test_login_com_credenciais_invalidas`
- `test_buscar_usuario_por_id`
- `test_buscar_usuario_por_id_invalido`
- `test_atualizar_usuario`
- `test_deletar_usuario`

## Observações

- O teste de exclusão cria e apaga um usuário novo para evitar conflitos com usuários existentes.
- Se você usar um ambiente virtual diferente, adapte os comandos de ativação conforme o seu shell.
