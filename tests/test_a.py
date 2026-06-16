# utils/gerador_dados.py
import random
import string
import time
import requests

URL = "https://compassuol.serverest.dev/"


def http_request(method, path, json=None, headers=None, max_attempts=3, wait_seconds=1):
    for attempt in range(1, max_attempts + 1):
        response = requests.request(method, URL + path, json=json, headers=headers)
        if response.status_code != 503:
            return response
        if attempt < max_attempts:
            time.sleep(wait_seconds)
    return response

def gerar_email():
    usuario = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{usuario}@teste.com"


def usuario():
    return {
        "nome": "Andrei",
        "email": gerar_email(),
        "password": "a",
        "administrador": "true"
    }


def criar_usuario():
    user = usuario()
    response = http_request("post", "usuarios", json=user)
    return user, response


def criar_login(max_attempts=3, wait_seconds=1):
    for attempt in range(1, max_attempts + 1):
        user, create_resp = criar_usuario()
        if create_resp.status_code != 201:
            if attempt < max_attempts:
                time.sleep(wait_seconds)
                continue
            raise AssertionError(f"Falha ao criar usuário para login: {create_resp.status_code}")

        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = http_request("post", "login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("authorization")
            if token:
                return token
        if attempt < max_attempts:
            time.sleep(wait_seconds)

    raise AssertionError("Não foi possível efetuar login com sucesso após várias tentativas")


def obter_token_administrador(max_attempts=3, wait_seconds=1):
    admin_credentials = {
        "email": "fulano@qa.com",
        "password": "teste"
    }
    for attempt in range(1, max_attempts + 1):
        response = http_request("post", "login", json=admin_credentials)
        if response.status_code == 200:
            token = response.json().get("authorization")
            if token:
                return token
        if attempt < max_attempts:
            time.sleep(wait_seconds)
    raise AssertionError("Não foi possível obter token de administrador após várias tentativas")


def criar_produto_com_token(produto, max_attempts=3, wait_seconds=1):
    token = obter_token_administrador()
    headers = {"Authorization": token}
    for attempt in range(1, max_attempts + 1):
        response = http_request("post", "produtos", json=produto, headers=headers)
        if response.status_code not in (503, 401):
            return response
        if attempt < max_attempts:
            time.sleep(wait_seconds)
    return response


class TestUsuarioCadastro:
    def test_get_users(self):
        response = requests.get(URL + "usuarios")
        assert response.status_code == 200
        assert response.json()["quantidade"] > 0
        print(response.json())

    def test_cadastrar_usuario(self):
        _, response = criar_usuario()
        assert response.status_code == 201

    def test_cadastrar_usuario_duplicado(self):
        user, _ = criar_usuario()
        response = http_request("post", "usuarios", json=user)
        assert response.status_code in (201, 400)
        if response.status_code == 400:
            assert response.json().get("message") in (
                "Este email já está sendo usado",
                "E-mail já cadastrado"
            )

    def test_cadastrar_usuario_com_campos_vazios(self):
        user = {
            "nome": "",
            "email": "",
            "password": "",
            "administrador": ""
        }
        response = requests.post(URL + "usuarios", json=user)
        assert response.status_code == 400


class TestLogin:
    def test_login(self):
        token = criar_login()
        assert token

    def test_login_senha_errada(self):
        user, _ = criar_usuario()
        login_data = {
            "email": user["email"],
            "password": "senhaerrada"
        }
        response = http_request("post", "login", json=login_data)
        assert response.status_code == 401

    def test_login_com_email_inexistente(self):
        user, _ = criar_usuario()
        login_data = {
            "email": "invalido@teste.com",
            "password": user["password"]
        }
        response = http_request("post", "login", json=login_data)
        assert response.status_code == 401

    def test_login_com_campos_vazios(self):
        login_data = {
            "email": "",
            "password": ""
        }
        response = http_request("post", "login", json=login_data)
        assert response.status_code == 400


class TestUsuarioOperacoes:
    def test_buscar_usuario_por_id(self):
        response = requests.get(URL + "usuarios")
        assert response.status_code == 200
        usuarios = response.json()["usuarios"]
        user_id = usuarios[0]["_id"]
        response = requests.get(URL + f"usuarios/{user_id}")
        assert response.status_code == 200
        assert response.json()["_id"] == user_id

    def test_buscar_usuario_por_id_invalido(self):
        response = requests.get(URL + "usuarios/1234567890")
        assert response.status_code == 400

    def test_atualizar_usuario(self):
        response = requests.get(URL + "usuarios")
        assert response.status_code == 200
        usuarios = response.json()["usuarios"]
        user_id = usuarios[0]["_id"]
        updated_user = {
            "nome": "Andrei Freitas",
            "email": gerar_email(),
            "password": "a",
            "administrador": "true"
        }
        response = requests.put(URL + f"usuarios/{user_id}", json=updated_user)
        assert response.status_code == 200
        assert response.json()["message"] in (
            "Registro de usuário alterado com sucesso",
            "Registro alterado com sucesso"
        )

    def test_deletar_usuario(self):
        _, create_resp = criar_usuario()
        assert create_resp.status_code == 201
        created_id = create_resp.json().get("_id")
        assert created_id

        del_resp = requests.delete(URL + f"usuarios/{created_id}")
        assert del_resp.status_code == 200
        assert del_resp.json().get("message") in (
            "Usuário excluído com sucesso",
            "Registro excluído com sucesso",
            "Nenhum registro excluído"
        )

class TestProduto:
    def test_get_produtos(self):
        response = http_request("get", "produtos")
        assert response.status_code == 200
        assert response.json()["quantidade"] > 0

    def test_cadastrar_produto_sem_token(self):
        produto = {
            "nome": "Produto Teste Sem Token",
            "preco": 100,
            "descricao": "Descrição do produto teste sem token",
            "quantidade": 10
        }
        response = http_request("post", "produtos", json=produto)
        assert response.status_code == 401
        assert "Token de acesso ausente" in response.json().get("message", "")

    def test_cadastrar_produto_com_token(self):
        produto = {
            "nome": "Produto Teste Com Token",
            "preco": 100,
            "descricao": "Descrição do produto teste com token",
            "quantidade": 10
        }
        response = criar_produto_com_token(produto)
        assert response.status_code == 201

    def test_buscar_produto_por_id(self):
        response = http_request("get", "produtos")
        assert response.status_code == 200
        produtos = response.json()["produtos"]
        produto_id = produtos[0]["_id"]
        response = http_request("get", f"produtos/{produto_id}")
        assert response.status_code == 200
        assert response.json()["_id"] == produto_id

    def test_atualizar_produto(self):
        response = http_request("get", "produtos")
        assert response.status_code == 200
        produtos = response.json()["produtos"]
        produto_id = produtos[0]["_id"]
        updated_produto = {
            "nome": "Produto Teste Atualizado",
            "preco": 150,
            "descricao": "Descrição atualizada do produto teste",
            "quantidade": 5
        }
        response = http_request(
            "put",
            f"produtos/{produto_id}",
            json=updated_produto,
            headers={"Authorization": obter_token_administrador()}
        )
        assert response.status_code == 200
        assert response.json()["message"] in (
            "Registro de produto alterado com sucesso",
            "Registro alterado com sucesso"
        )

    def excluir_produto(self):
        produto = {
            "nome": "Produto para Deletar",
            "preco": 50,
            "descricao": "Produto que será deletado",
            "quantidade": 1
        }
        create_resp = requests.post(URL + "produtos", json=produto)
        assert create_resp.status_code == 201
        created_id = create_resp.json().get("_id")
        assert created_id

        del_resp = requests.delete(URL + f"produtos/{created_id}")
        assert del_resp.status_code == 200
        assert del_resp.json().get("message") in (
            "Produto excluído com sucesso",
            "Registro excluído com sucesso"
        )