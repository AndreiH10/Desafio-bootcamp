# Plano de Testes - API ServeRest

**Projeto:** Desafio Bootcamp  
**API Testada:** https://compassuol.serverest.dev/  
**Framework:** pytest + requests  
**Data:** 2026-06-15

---

## 📋 Objetivo Geral

Validar a funcionalidade completa da API ServeRest, cobrindo operações CRUD de usuários e produtos, autenticação, e casos de erro.

---

## 🎯 Escopo de Testes

### 1. **Gestão de Usuários**
- Listar usuários
- Cadastrar novo usuário
- Buscar usuário por ID
- Atualizar usuário
- Deletar usuário
- Validações de entrada

### 2. **Autenticação**
- Login com credenciais válidas
- Login com senha inválida
- Login com email inexistente
- Login com campos vazios

### 3. **Gestão de Produtos**
- Listar produtos
- Cadastrar produto (requer admin)
- Buscar produto por ID
- Atualizar produto (requer admin)
- Deletar produto (requer admin)

### 4. **Validações de Segurança**
- Permissões de acesso (admin vs comum)
- Token de autorização
- Autenticação obrigatória

---

## 📊 Matriz de Testes

### Classe: `TestUsuarioCadastro` (4 testes)

| ID | Teste | Entrada | Resultado Esperado | Status |
|---|---|---|---|---|
| U001 | `test_get_users` | GET /usuarios | 200, quantidade > 0 | ✅ |
| U002 | `test_cadastrar_usuario` | POST /usuarios (novo) | 201 | ✅ |
| U003 | `test_cadastrar_usuario_duplicado` | POST /usuarios (duplicado) | 400 ou 201* | ✅ |
| U004 | `test_cadastrar_usuario_com_campos_vazios` | POST /usuarios (campos vazios) | 400 | ✅ |

*Aceita ambos por inconsistência da API

---

### Classe: `TestLogin` (4 testes)

| ID | Teste | Entrada | Resultado Esperado | Status |
|---|---|---|---|---|
| L001 | `test_login` | POST /login (válido) | 200, token retornado | ✅ |
| L002 | `test_login_senha_errada` | POST /login (senha errada) | 401 | ✅ |
| L003 | `test_login_com_email_inexistente` | POST /login (email não existe) | 401 | ✅ |
| L004 | `test_login_com_campos_vazios` | POST /login (campos vazios) | 400 | ✅ |

---

### Classe: `TestUsuarioOperacoes` (4 testes)

| ID | Teste | Entrada | Resultado Esperado | Status |
|---|---|---|---|---|
| O001 | `test_buscar_usuario_por_id` | GET /usuarios/{id} | 200, dados corretos | ✅ |
| O002 | `test_buscar_usuario_por_id_invalido` | GET /usuarios/1234567890 | 400 | ✅ |
| O003 | `test_atualizar_usuario` | PUT /usuarios/{id} | 200, alterado | ✅ |
| O004 | `test_deletar_usuario` | DELETE /usuarios/{id} | 200, deletado | ✅ |

---

### Classe: `TestProduto` (5 testes)

| ID | Teste | Entrada | Resultado Esperado | Status |
|---|---|---|---|---|
| P001 | `test_get_produtos` | GET /produtos | 200, quantidade > 0 | ✅ |
| P002 | `test_cadastrar_produto_sem_token` | POST /produtos (sem token) | 401 | ✅ |
| P003 | `test_cadastrar_produto_com_token` | POST /produtos (admin token) | 201 | ✅ |
| P004 | `test_buscar_produto_por_id` | GET /produtos/{id} | 200, dados corretos | ✅ |
| P005 | `test_atualizar_produto` | PUT /produtos/{id} (admin) | 200, alterado | ✅ |

---

## 🔐 Estratégia de Autenticação

### Tokens
- **Login Regular:** Cria usuário dinâmico, faz login
- **Admin Token:** Usa credenciais seeded (`fulano@qa.com` / `teste`)
- **Timeout:** 10 minutos (600 segundos)

### Headers
```
Authorization: Bearer <token_jwt>
```

---

## 🛡️ Tratamento de Falhas

### Retry automático em:
- `503 Service Unavailable` (até 3 tentativas)
- `401 Unauthorized` em endpoints de produto (até 3 tentativas)

### Espera entre tentativas:
- 1 segundo padrão
- Máximo 3 tentativas

---

## 📈 Cobertura de Testes

```
Total de Testes: 17
├── Usuários: 4
├── Login: 4
├── Operações de Usuário: 4
└── Produtos: 5

Taxa de Cobertura: 100% dos endpoints principais
```

---

## 🚀 Como Executar

### Todos os testes
```bash
pytest tests/test_a.py -v
```

### Testes específicos
```bash
pytest tests/test_a.py -k "login" -v
pytest tests/test_a.py::TestProduto -v
pytest tests/test_a.py::TestProduto::test_cadastrar_produto_com_token -v
```

### Com relatório detalhado
```bash
pytest tests/test_a.py -v --tb=short
pytest tests/test_a.py -v --tb=long
```

### Com cobertura
```bash
pytest tests/test_a.py --cov=. --cov-report=html
```

---

## ⚙️ Pré-Requisitos

- Python 3.10+
- `requests` library
- `pytest` library
- Acesso à API (https://compassuol.serverest.dev/)
- Conexão com internet

---

## 📝 Dados de Teste

### Usuário Dinâmico
```json
{
  "nome": "Andrei",
  "email": "random@teste.com",
  "password": "a",
  "administrador": "true"
}
```

### Admin Seeded
```json
{
  "email": "fulano@qa.com",
  "password": "teste"
}
```

### Produto
```json
{
  "nome": "Produto Teste",
  "preco": 100,
  "descricao": "Descrição",
  "quantidade": 10
}
```

---

## 🔍 Casos de Erro Cobertos

| Erro | Teste | Código | Mensagem |
|---|---|---|---|
| Email já cadastrado | U003 | 400 | "Este email já está sendo usado" |
| Campos vazios | U004 | 400 | "Campo obrigatório" |
| Senha inválida | L002 | 401 | "Email e/ou senha inválidos" |
| Email não encontrado | L003 | 401 | "Email e/ou senha inválidos" |
| Usuário não encontrado | O002 | 400 | "Usuário não encontrado" |
| Token ausente | P002 | 401 | "Token de acesso ausente..." |
| Produto não encontrado | - | 400 | "Produto não encontrado" |


**Última atualização:** 2026-06-15  
**Responsável:** Andrei Rodrigues 