import jwt
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from requests import Session 


# Define the JWT payload with specific claims
def create_token():
    payload = {
        'role': 'ADMIN',
        'exp': datetime.datetime.now() + datetime.timedelta(days=365),  
    }

    # Create the JWT using PyJWT
    encoded_jwt = jwt.encode(payload, 'secret123', algorithm='HS256')

    return encoded_jwt 


# Assigns a value to the token for use in requests.Session()
session = Session()  

# Assigns the token to session
session.headers.update({'Authorization': f'Bearer {create_token()}'})

# Automated request execution (use this carefully and only in controlled environments)
def perform_requests(endpoint, id):
    response = session.post(f"{endpoint}/{id}")  

    print(f"Response Status Code: {response.status_code}") 

    # Handle the response based on your specific needs


if __name__ == "__main__":
    perform_requests('/api/documents/1', 1) # Replace with actual endpoint and ID