import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Componente X: Função de worker independente
def worker(id_utilizador, token_estatico):
    """
    Envia um pedido HTTP DELETE para eliminar um utilizador.
    
    Args:
        id_utilizador (int): ID do utilizador a eliminar.
        token_estatico (str): Token estático para autenticação.
    """
    url = f'http://localhost:8080/api/users/{id_utilizador}'
    headers = {'Authorization': f'Bearer {token_estatico}'}
    try:
        resposta = requests.delete(url, headers=headers, timeout=1)
        resposta.raise_for_status()  # Lança uma exceção para códigos de status de erro
        print(f'Utilizador {id_utilizador} eliminado com sucesso.')
    except requests.exceptions.HTTPError as errh:
        print(f'Erro HTTP: {errh}')
    except requests.exceptions.ConnectionError as errc:
        print(f'Erro de conexão: {errc}')
    except requests.exceptions.Timeout as errt:
        print(f'Timeout: {errt}')
    except requests.exceptions.RequestException as err:
        print(f'Erro geral: {err}')

# Componente Y: Função para ler IDs de utilizadores de um ficheiro
def ler_ids_ficheiro(nome_ficheiro):
    """
    Lê IDs de utilizadores a partir de um ficheiro de texto.
    
    Args:
        nome_ficheiro (str): Nome do ficheiro de texto.
    
    Returns:
        list: Lista de IDs de utilizadores.
    """
    try:
        with open(nome_ficheiro, 'r') as ficheiro:
            ids = [int(linha.strip()) for linha in ficheiro.readlines()]
        return ids
    except FileNotFoundError:
        print(f'Ficheiro {nome_ficheiro} não encontrado.')
        return []

# Componente Z: Utilização do ThreadPoolExecutor
def main():
    token_estatico = 'SEU_TOKEN_ESTATICO_AQUI'  # Substitua com o seu token estático
    nome_ficheiro = 'alvos_a_purgar.txt'
    ids_utilizadores = ler_ids_ficheiro(nome_ficheiro)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda id_utilizador: worker(id_utilizador, token_estatico), ids_utilizadores)

if __name__ == '__main__':
    inicio = time.time()
    main()
    fim = time.time()
    print(f'Tempo total de execução: {fim - inicio} segundos')