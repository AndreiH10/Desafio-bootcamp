# utils/gerador_dados.py
import random
import string
import requests

URL = "https://compassuol.serverest.dev/"

def test_get_users():
    response = requests.get(URL + "usuarios")
    assert response.status_code == 200
    assert response.json()["quantidade"] > 0
    print(response.json())

def gerar_email():
    usuario = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{usuario}@teste.com"

def usuario():
    return{
        "nome": "Andrei",
        "email": gerar_email(),
        "password": "a",
        "administrador": "true"
    }

def test_cadastrar_usuario():
    response = requests.post(URL + "usuarios", json=usuario())
    assert response.status_code == 201

def test_cadastrar_usuario_duplicado():
    user = usuario()
    requests.post(URL + "usuarios", json=user)
    response = requests.post(URL + "usuarios", json=user)
    assert response.status_code == 400

def test_cadastrar_usuario_com_campos_vazios():
    user = {
        "nome": "",
        "email": "",
        "password": "",
        "administrador": ""
    }
    response = requests.post(URL + "usuarios", json=user)
    assert response.status_code == 400

def test_login():
    user = usuario()
    requests.post(URL + "usuarios", json=user)
    login_data = {
        "email": user["email"],
        "password": user["password"]
    }
    response = requests.post(URL + "login", json=login_data)
    assert response.status_code == 200
    # A API retorna o token no corpo da resposta em `authorization`
    assert response.json().get("authorization")

def test_login_com_credenciais_invalidas():
    login_data = {
        "email": "invalido@teste.com",
        "password": "invalido"
    }
    response = requests.post(URL + "login", json=login_data)
    assert response.status_code == 401
    
def test_buscar_usuario_por_id():
    response = requests.get(URL + "usuarios")
    assert response.status_code == 200
    usuarios = response.json()["usuarios"]
    user_id = usuarios[0]["_id"]
    response = requests.get(URL + f"usuarios/{user_id}")
    assert response.status_code == 200
    assert response.json()["_id"] == user_id

def test_buscar_usuario_por_id_invalido():
    response = requests.get(URL + "usuarios/1234567890")
    assert response.status_code == 400

def test_atualizar_usuario():
    response = requests.get(URL + "usuarios")
    assert response.status_code == 200
    usuarios = response.json()["usuarios"]
    user_id = usuarios[0]["_id"]
    updated_user = {
        "nome": "Andrei Silva",
        "email": gerar_email(),
        "password": "a",
        "administrador": "true"
    }
    response = requests.put(URL + f"usuarios/{user_id}", json=updated_user)
    assert response.status_code == 200
    assert response.json()["message"] == "Registro de usuário alterado com sucesso"

def test_deletar_usuario():
    # Criar um usuário novo para garantir que não há carrinho atrelado
    new_user = usuario()
    create_resp = requests.post(URL + "usuarios", json=new_user)
    assert create_resp.status_code == 201
    created_id = create_resp.json().get("_id")
    assert created_id

    # Agora deletar o usuário criado
    del_resp = requests.delete(URL + f"usuarios/{created_id}")
    assert del_resp.status_code == 200
    assert del_resp.json().get("message") in ("Usuário excluído com sucesso", "Registro excluído com sucesso")

