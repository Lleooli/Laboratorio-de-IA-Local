def generate_urls(base="http://localhost:8080/api/documents/"):
  urls = []
  for i in range(1, 101):
    urls.append(f"{base}{i}")
  return urls

def get_response_size(url, token="Bearer exampleToken"):
  try:
    import requests
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    # Verificar se o request foi bem sucedido 
    if response.status_code == 200:
      return len(response.content) # tamanho em bytes da resposta
    else:
      print(f"Request to URL {url} failed with status code: {response.status_code}")
  except Exception as e:
    print(f"Error during request: {e}")


def main():
  urls = generate_urls()
  for url in urls:
    size = get_response_size(url)
    if size > 50 and response.status_code == 200:
      print(f"Potencial falso positivo: {url} - Tamanho: {size} bytes, Status Code: {response.status_code}")

  
main()