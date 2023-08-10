import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathlib import Path


# url = "https://www.franksonnenbergonline.com/blog/are-you-grateful/"

# response = requests.get(url)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, "lxml")
# title_text = soup.find('main').find('header').find('h1').text
# post_img = soup.find('img', class_='attachment-post-image')['src']
# post_text = soup.find('div', class_='entry-content').find('p').text

# print(title_text)
# print(post_img)
# print(post_text)


def save_books(num_book):
    url = "https://tululu.org/txt.php"
    for book_id in range(num_book):
        params = {
            "id": f'{book_id}'
        }

        response = requests.get(url ,params=params)
        response.raise_for_status() 

        try:
            check_for_redirect(response)
            filename = f'kniga_{book_id}.txt'
            with open(f'books/{filename}', 'wb') as file:
                file.write(response.content)
        except HTTPError as ex:
            print("На данной странице нет книги.")


def check_for_redirect(response):
    if len(response.history) > 0:
        raise HTTPError
    



if __name__ == '__main__':
    Path("books").mkdir(parents=True, exist_ok=True)
    num_book = 10

    save_books(num_book)
    