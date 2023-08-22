import requests
import json
from requests.exceptions import HTTPError, ConnectionError
from bs4 import BeautifulSoup
from save_book import check_for_redirect, download_image, download_txt, parse_book_page
from urllib.parse import urljoin



if __name__ == "__main__":
    main_url = "https://tululu.org/"
    download_url = "https://tululu.org/txt.php"
    page_num = 1
    count = 1
    for page in range(1, page_num + 1):
        fantasy_block_url = f"https://tululu.org/l55/{page}/"
        response = requests.get(fantasy_block_url)
        response.raise_for_status()
        check_for_redirect(response)

        soup = BeautifulSoup(response.text, "lxml")
        book_cards = soup.select(".d_book")
        for book_url in book_cards:
            book_id = book_url.select_one("a")["href"][2:-1]
            book_url = urljoin(main_url, book_url.select_one("a")["href"])
            print(book_url)
            params = {
                "id": book_id
            }
            try:
                response = requests.get(book_url)
                response.raise_for_status()
                check_for_redirect(response)

                reference_book = parse_book_page(response.text, book_url)
                book_path = download_txt(download_url, params, f'{book_id}.{reference_book["book_name"]}')
                img_path = download_image(reference_book['full_img_url'], reference_book['short_img_url'])
                reference_book["book_path"] = book_path
                reference_book["img_path"] = img_path
                
                with open("capitals.json", "a", encoding="utf-8") as file:
                    json.dump(reference_book, file, ensure_ascii=False, indent=2)
                    file.write("\n\n")
            except HTTPError as ex:
                print("На данной странице нет книги.", end="\n\n")
            except ConnectionError as ex:
                print(ex)

            print(book_id)
            count += 1


    

