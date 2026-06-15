# utils/gerador_dados.py
import random
import string
import requests

URL = "https://compassuol.serverest.dev/"


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
    response = requests.post(URL + "usuarios", json=user)
    return user, response


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
        response = requests.post(URL + "usuarios", json=user)
        assert response.status_code == 400

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
        user, _ = criar_usuario()
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(URL + "login", json=login_data)
        assert response.status_code == 200
        assert response.json().get("authorization")

    def test_login_com_credenciais_invalidas(self):
        login_data = {
            "email": "invalido@teste.com",
            "password": "invalido"
        }
        response = requests.post(URL + "login", json=login_data)
        assert response.status_code == 401


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
            "Registro excluído com sucesso"
        )

