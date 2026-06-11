import requests
from concurrent.futures import ThreadPoolExecutor
import time

def worker(user_id, token):
    """Worker function to delete user data."""
    try:
        url = f"http://localhost:8080/api/users/{user_id}"
        response = requests.delete(url, timeout=1)  # Timeout of 1 second
        if response.status_code == 204:
            print(f"User {user_id} deleted successfully.")
        else:
            print(f"Error deleting user {user_id}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting user {user_id}: {e}")

def load_users_from_file(filename):
    """Loads user IDs from the given file."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f]

# ThreadPoolExecutor settings
num_threads = 50  

# Main execution loop 
def main():
    user_ids = load_users_from_file('alvos_a_purgar.txt')  # Load user IDs from 'alvos_a_purgar.txt'
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker, id, token) for id in user_ids]
        for future in futures:
            future.result()  # Wait for tasks to complete


if __name__ == "__main__":
    main() 
