import requests
from concurrent.futures import ThreadPoolExecutor

# Importar biblioteca para leitura de ficheiros de texto
import json 


def worker(user_id, token):
    """Executa a ação de limpeza de dados de teste."""  
    url = f'http://localhost:8080/api/users/{user_id}'
    try:
        response = requests.delete(url, timeout=1) 
        if response.status_code == 204: # Verificar se a ação foi bem-sucedida
            print(f"Registro de ID {user_id} removido com sucesso!")
        else:
            print(f"Falha na remoção do registro de ID {user_id}: Status Code: {response.status_code}") 
    except requests.exceptions.RequestException as error: 
        print(f"Erro ao remover o registro de ID {user_id}: {error}")

def load_users(filename):
    """Lê a lista de IDs de usuários de um ficheiro de texto."""  
    with open(filename, 'r') as file:  # Abrir o ficheiro para leitura
        data = json.load(file) 
    return data


def main():  
    """Função principal que organiza e executa os demais componentes."""   
    user_ids = load_users('alvos_a_purgar.txt') # Carregar IDs de usuários do ficheiro

    with ThreadPoolExecutor(max_workers=50) as executor: 
        # Mapea a função `worker` a cada ID de usuário e executa em paralelo  
        for user_id in user_ids: 
            executor.submit(worker, user_id, 'token_de_autenticação') # Executar a função worker com o ID do usuário

    print("Limpeza de dados concluída!")


if __name__ == "__main__":
    main()   