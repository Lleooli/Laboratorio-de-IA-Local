import requests
from jose import jwt
#nao importou datetime
from datetime import datetime
from datetime import timedelta as dt
# Definir URL de endpoint de API para apagar usuários
url = 'http://localhost:8080/api/users/' 

# Função para gerar um JWT válido
def generate_jwt(user_id):
  payload, secret_key = {"sub": user_id, "exp": datetime.datetime.utcnow() + dt.timedelta(days=1)} # exemplo de payload
  #alucinou
  token = jwt.encode(payload, secret_key) 
  return token

# Definir um dicionário com IDs de usuários para apagar
user_ids = [1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

# Loop para enviar solicitações DELETE
for i in user_ids:
  token = generate_jwt(i) # Gera um JWT para cada usuário
  headers = {"Authorization": f"Bearer {token}"} # Adiciona o token JWT na requisição
  response = requests.delete(url + str(i)) # Realiza a requisição DELETE

  # Verifica se o servidor respondeu com sucesso 
  if response.status_code == 204: 
    print(f"Usuário {user_id} foi excluído com sucesso.") 
  else: 
    print(f"Erro ao excluir usuário {i}: {response.text}") # Imprime o erro caso ocorra