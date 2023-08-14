import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urljoin



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


def download_image(url, filename, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()

    filename = filename.split('/')[-1]
    path_to_img = os.path.join(folder, filename)
    with open(f'{folder}{filename}', 'wb') as file:
        file.write(response.content)
    return path_to_img


    

if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)
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
            short_book_img = soup.find('div', class_='bookimage').find('img')['src']
            full_url_img = urljoin(url_for_title, short_book_img)
            book_name = title_text.split(':')[0].strip()
            comments = soup.find_all('div', class_='texts')
            print(book_name, end="\n\n")

            for comment in comments:
                comment = comment.find('span').text
                print(comment)

            print()
        
            # print(download_image(full_url_img, short_book_img))
            # print(download_txt(download_url, f'{book_id}.{book_name}'))
        except HTTPError as ex:
            print("На данной странице нет книги.", end="\n\n")

    