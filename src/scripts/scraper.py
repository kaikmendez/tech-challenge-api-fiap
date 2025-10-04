import os
import requests
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.utils.db import SetupDatabase

load_dotenv()

URL = os.getenv("URL")

class ScraperBook():
    def __init__(self):
        pass

    def scrape_books(self):
        """
        Função responsável por extrair dados do site 'books.toscrape.com'.
        """
        all_books_data = []
        print("Starting the Web Scraping...")

        url_join = urljoin(URL, "page-1.html")

        http_session = requests.Session()

        while url_join:
            print(f"Raspando a página: {url_join}")

            data_pag = http_session.get(url_join)
            data_pag.encoding='utf-8'
            soup = BeautifulSoup(data_pag.text, 'html.parser')

            books_on_page = soup.find_all('article', class_='product_pod')

            for book in books_on_page:
                specific_url = book.find('h3').find('a')['href']
                full_url = urljoin(url_join, specific_url)
                specific_book = http_session.get(full_url)
                specific_book.encoding='utf-8'

                soup_book = BeautifulSoup(specific_book.text, 'html.parser')
                
                category_name = soup_book.find('ul', class_='breadcrumb').find_all('li')[2].find('a').text
                book_title = soup_book.find('div', class_='col-sm-6 product_main').find('h1').text
                desc_div = soup_book.find('div',id='product_description')
                if desc_div:
                    product_description = desc_div.find_next_sibling('p').text
                else:
                    product_description = ''
                price = soup_book.find('table', class_='table table-striped').find_all('tr')[3].find('td').text
                tax = soup_book.find('table', class_='table table-striped').find_all('tr')[5].find('td').text
                availability = soup_book.find('table', class_='table table-striped').find_all('tr')[6].find('td').text

                dict_book = {
                    "category": category_name,
                    "title": book_title,
                    "description": product_description,
                    "price": price,
                    "tax": tax,
                    "availability": availability
                }

                all_books_data.append(dict_book)

            next_button = soup.find('li', class_='next')
            if next_button:
                next_url = next_button.find('a')['href']
                url_join = urljoin(URL, next_url)
            else:
                url_join = None
            
        print(f"\tTotal books scraped: {len(all_books_data)}")
        print("Ending the Web Scraping...")
        print("*************************************************************************************************")

        return all_books_data

    def save_to_csv(self,scraper_books):
        if scraper_books:
            try:
                df = pd.DataFrame(scraper_books)
                df.to_csv('livros.csv', index=False, encoding='utf-8')
            except Exception as e:
                print(f'Erro ao salvar em csv: {e}')

    def save_on_db(self, scraper_books):
        if not scraper_books:
            return

        conn = None
        try:
            conn = SetupDatabase.create_script_connection()
            df = pd.DataFrame(scraper_books)
            df.index = df.index + 1
            
            df.to_sql(
                'book_api_fiap',
                con=conn,
                if_exists='replace',
                index=True,
                index_label='id'
            )
            print(f"{len(df)} registros salvos no banco de dados com sucesso!")

        except Exception as e:
            print(f'Erro ao salvar no banco de dados: {e}')
        
        finally:
            if conn:
                conn.close()
