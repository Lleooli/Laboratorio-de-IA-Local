import requests

# Define base URL and endpoint for retrieving documents
base_url = 'http://localhost:8080/api/documents/'
endpoint_pattern = '{id}'

# Initializing headers for the request 
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' ,
    'Accept': 'application/json' ,
    'Content-Type': 'application/json' 
}

# Looping through the list of document IDs
for document_id in range(1, 10):  
   # Construct the full URL with ID 
   # Adaptado, estava com erro de formatação, agora está correto
   url = base_url + str(document_id)

   # Initiate a GET request to retrieve the document
   response = requests.get(url, headers=headers)

   # Check for successful response (HTTP 200 status code)
   if response.status_code == 200:
     print(f'Document {document_id} retrieved successfully.') 
   else: 
       print(f'Error retrieving document {document_id}: {response.status_code}')

# For the deletion, we use a different endpoint
delete_url = base_url + 'users/{id}'

headers_delete = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' , 
    'Accept': 'application/json' ,
    'Content-Type': 'application/json'  
}

for id in range(1, 10): 
   # Construct the full URL with ID
   url = delete_url.format(id=id)  
   
   # Initiate a DELETE request to remove user from the system 
   response = requests.delete(url, headers=headers_delete)

   # Check for successful response (HTTP 204 status code)
   if response.status_code == 204: 
       print(f'User {id} deleted successfully.')  
   else: 
       # Resultado: Erro 404, não conseguiu deletar
       print(f'Error deleting user {id}: {response.status_code}')