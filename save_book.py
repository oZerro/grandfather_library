import requests
import os
import argparse
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
    try:
        filename = filename.split('/')[-1]
        path_to_img = os.path.join(folder, filename)
        with open(f'{folder}{filename}', 'wb') as file:
            file.write(response.content)
        return path_to_img
    except HTTPError as ex:
        print("Тут нет картинок")


def parse_book_page(page_html):
    soup = BeautifulSoup(page_html, "lxml")
    title_text = soup.find('div', {'id': 'content'}).find('h1').text
    short_img_url = soup.find('div', class_='bookimage').find('img')['src']

    reference_book = {
        'short_img_url': short_img_url,
        'full_img_url': urljoin(url_for_title, short_img_url),
        'book_name': title_text.split(':')[0].strip(),
        'book_author': title_text.split(':')[-1].strip(),
        'comments': [comment.find('span').text for comment in soup.find_all('div', class_='texts')],
        'book_genres': [genre.text for genre in soup.find('span', class_='d_book').find_all('a')],
    }

    return reference_book
    
    

if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description='Помогает скачивать книги')
    parser.add_argument('--start_id', help="Id начальной книги для скачивания", default=1)
    parser.add_argument('--end_id', help='Id финальной книги для скачивания', default=10)
    args = parser.parse_args()

    start_id = int(args.start_id)
    end_id = int(args.end_id)
    book_id = start_id

    while book_id <= end_id:
        url_for_title = f"https://tululu.org/b{book_id}/"
        download_url = f"https://tululu.org/txt.php?id={book_id}"

        response = requests.get(url_for_title)
        response.raise_for_status()

        try:
            check_for_redirect(response)
            reference_book = parse_book_page(response.text)
            download_txt(download_url, f'{book_id}.{reference_book["book_name"]}')
            download_image(reference_book['full_img_url'], reference_book['short_img_url'])
        except HTTPError as ex:
            print("На данной странице нет книги.", end="\n\n")
        book_id += 1

    