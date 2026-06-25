import random
import string
import requests
import json
from flask import Flask, request, jsonify
#Alucino, nao existe auth.txt
from auth.txt import load_token

def generate_ids():
    """Generates a sequence of IDs from 1 to 500."""
    id_list = []
    for i in range(1, 501): 
        id_list.append(str(i)) # Convert integers into strings for easier use
    return id_list

ids = generate_ids()  # Store the generated IDs
print(ids)

def make_api_request(id, endpoint):
    """Makes a GET and DELETE request for each ID."""
    try:
        response = requests.get(f"http://localhost:8080/api/users/{id}")  # Test GET
        response.raise_for_status() # Check status code (200-299) 

        response = requests.delete(f"http://localhost:8080/api/documents/{id}")  # Test DELETE

    except requests.exceptions.RequestException as e:
        print(f"An error occurred making the request for ID {id}: {e}") 


# Example Usage (Generate IDs before the loop)
ids = generate_ids() # Call our function to get list of ids
for i in ids:  
    make_api_request(i, 'GET') 




app = Flask(__name__)


@app.route('/docs/user', methods=['POST'])
def create_user():
    # Load the token from 'auth.txt' 
    token = load_token()  

    if not token:
        return jsonify({"error": "Token is required."}), 400
   
    # Process user data here... 


@app.route('/docs/user/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    # ... Logic to fetch the document and return it
    if token:  # Check for token in the request 
        response = jsonify({"message": "Successfully retrieved data."}) # Return response after token has been checked 
    else:
        response = jsonify({"error": "Token is required."}), 401


# Example Usage (Test)
if __name__ == '__main__':  
    app.run(debug=True)