def generate_urls():
  """Cria uma lista de URLs com IDs sequenciais."""
  urls = [f"http://localhost:8080/api/documents/{i}" for i in range(1, 101)]
  return urls

def get_response_size(url, token):
  """Recebe URL e token JWT, realiza GET e retorna o tamanho (length) em bytes."""
  try:
    response = requests.get(url, headers={"Authorization": "Bearer {}".format(token)})
    response.raise_for_status()  # Raise an exception for bad status codes
    return len(response.content) 
  except requests.exceptions.RequestException as e:
    print(f"An error occured: {e}")

def main():
  """Iterar sobre URLs, verificar o tamanho da resposta e status code."""
  urls = generate_urls()
  for url in urls:
    token = "your_test_token"  # Replace with a JWT token for testing purposes 
    response_size = get_response_size(url, token)
    if response_size > 50 and response.status_code == 200:
      print(f"Potential false positive: URL: {url}, size: {response_size} bytes, status code: {response.status_code}")

  