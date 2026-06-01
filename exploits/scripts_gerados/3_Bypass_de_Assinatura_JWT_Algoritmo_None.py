import jwt
import requests

# Passo 1: Decodificar o token existente sem verificar a assinatura e alterar a claim 'sub'
token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJSYWZhZWxhIEJhcmF0YSIsInJvbGUiOiJVU0VSIiwidXNlcklkIjo4LCJpYXQiOjE3Nzk3ODkxMTUsImV4cCI6MTc3OTg3NTUxNX0.7SoIulyCpdxDpS4z6Ve0aVoqGlVxb-68q94vvLIbV7YTn0KVjWYwh8T--c7jQ3DuokOF2oQ8kfnt9BpepzAa5g"  # Substitua com o token que você deseja manipular
payload = jwt.decode(token, options={"verify_signature": False})
payload['sub'] = 'admin@corp.com'

# Passo 2: Recodificar o payload alterado utilizando o algoritmo 'none'
token_anomalo = jwt.encode(payload, None, algorithm=None)

# Passo 3: Construir uma requisição GET com o token anômalo no cabeçalho Authorization
headers = {"Authorization": f"Bearer {token_anomalo}"}
response = requests.get("http://localhost:8080/api/documents/1", headers=headers)

if response.status_code == 200:
    print("Atenção: O servidor retornou status 200. Isso pode indicar uma vulnerabilidade na validação de tokens.")
else:
    print(f"Servidor retornou status {response.status_code}. O token anômalo foi rejeitado como esperado.")

print(f"Token Anômalo: {token_anomalo}")