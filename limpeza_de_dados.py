import requests
import concurrent.futures

# Componente X: Função de worker
def delete_user(id, token):
    try:
        response = requests.delete(f'http://localhost:8080/api/users/{id}', headers={'Authorization': f'Bearer {token}'}, timeout=1)
        response.raise_for_status()
        print(f'Utilizador {id} eliminado com sucesso')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao eliminar utilizador {id}: {e}')

# Componente Y: Leitura de IDs de utilizadores a partir de ficheiro
def load_ids(filename):
    try:
        with open(filename, 'r') as file:
            ids = [int(line.strip()) for line in file]
        return ids
    except FileNotFoundError:
        print(f'Ficheiro {filename} não encontrado')
        return []

# Componente Z: Implementação do ThreadPoolExecutor
def main():
    token = 'seu_token_estático_aqui'
    ids = load_ids('alvos_a_purgar.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda id: delete_user(id, token), ids)

if __name__ == '__main__':
    main()
