def gerar_urls(base_url, inicio_id, fim_id):
    """
    Gera uma lista de URLs combinando a string base com IDs sequenciais.

    Args:
        base_url (str): URL base.
        inicio_id (int): ID inicial.
        fim_id (int): ID final.

    Returns:
        list: Lista de URLs geradas.
    """
    return [f"{base_url}{id}" for id in range(inicio_id, fim_id + 1)]

# Exemplo de uso
base_url = 'http://localhost:8080/api/documents/'
inicio_id = 1
fim_id = 1000
urls = gerar_urls(base_url, inicio_id, fim_id)

import requests

def tamanho_resposta(url, token_jwt):
    """
    Realiza um GET na URL com o token JWT e retorna o tamanho da resposta.

    Args:
        url (str): URL para realizar o GET.
        token_jwt (str): Token JWT de baixo privilégio.

    Returns:
        tuple: Tamanho da resposta em bytes e status code.
    """
    headers = {'Authorization': f"Bearer {token_jwt}"}
    resposta = requests.get(url, headers=headers)
    return len(resposta.content), resposta.status_code

# Exemplo de uso
url = 'http://localhost:8080/api/documents/1'
token_jwt = 'f4557958a67b9bb9b762f1e0a7054c53dbe2af8c4cbafb730e8b60a3e4079192'
tamanho, status_code = tamanho_resposta(url, token_jwt)

import requests

def gerar_urls(base_url, inicio_id, fim_id):
    return [f"{base_url}{id}" for id in range(inicio_id, fim_id + 1)]

def tamanho_resposta(url, token_jwt):
    headers = {'Authorization': f"Bearer {token_jwt}"}
    resposta = requests.get(url, headers=headers)
    return len(resposta.content), resposta.status_code

def rotina_principal(base_url, inicio_id, fim_id, token_jwt):
    urls = gerar_urls(base_url, inicio_id, fim_id)
    for url in urls:
        tamanho, status_code = tamanho_resposta(url, token_jwt)
        if tamanho > 50 and status_code == 200:
            print(f"Falso positivo de permissão na URL: {url}")

# Exemplo de uso
base_url = 'http://localhost:8080/api/documents/'
inicio_id = 1
fim_id = 1000
rotina_principal(base_url, inicio_id, fim_id, token_jwt)