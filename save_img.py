import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename



def check_for_redirect(response):
    if len(response.history) > 0:
        raise HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
        filename = sanitize_filename(filename)
        path_to_file = os.path.join(folder, f'{filename}.txt')
        with open(f'{folder}{filename}', 'wb') as file:
            file.write(response.content)
        return path_to_file
    except HTTPError as ex:
        print("На данной странице нет книги.")

    


# for i in range(1, 50):
#     url = f"https://tululu.org/b{i}/"

#     response = requests.get(url)
#     response.raise_for_status()

#     try:
#         check_for_redirect(response)
#         soup = BeautifulSoup(response.text, "lxml")
#         title_text = soup.find('div', {'id': 'content'}).find('h1').text

#         book_name = title_text.split(':')[0].strip()
#         author_name = title_text.split(':')[-1].strip()

#         print('Заголовок:', book_name)
#         print('Автор:', author_name)
#         print()
#     except HTTPError as ex:
#         print("На данной странице нет книги.")
#         print()

    

if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)
    num_book = 10


    for book_id in range(1, num_book+1):
        url_for_title = f"https://tululu.org/b{book_id}/"
        download_url = f"https://tululu.org/txt.php?id={book_id}"

        response = requests.get(url_for_title)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, "lxml")
            title_text = soup.find('div', {'id': 'content'}).find('h1').text
            book_name = title_text.split(':')[0].strip()
            print(download_txt(download_url, f'{book_id}.{book_name}'))
        except HTTPError as ex:
            print("На данной странице нет книги.")

    