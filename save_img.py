import requests
from pathlib import Path


def save_book(num_book):
    url = "https://tululu.org/txt.php"
    for book_id in range(num_book):
        params = {
            "id": f'{book_id}'
        }

        response = requests.get(url ,params=params)
        response.raise_for_status() 

        filename = f'kniga_{book_id}.txt'
        with open(f'books/{filename}', 'wb') as file:
            file.write(response.content)



if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)
    