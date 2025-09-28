import os
import re
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

load_dotenv()

URL = os.getenv("URL")

def converter_nota_para_int(texto_nota_lista):
    """Converte a classe da nota (ex: ['star-rating', 'Five']) para um inteiro."""
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    # A nota em texto é o segundo item da lista de classes
    if len(texto_nota_lista) > 1:
        nota_texto = texto_nota_lista[1]
        return rating_map.get(nota_texto, 0)
    return 0

def scrape_books():
    """
    Função responsável por extrair dados do site 'books.toscrape.com'.
    """
    all_books_data = []
    print("Iniciando Processo de scraping...")

    # Começa na primeira página do catálogo
    url_atual = urljoin(URL, "catalogue/page-1.html")

    http_session = requests.Session()

    while url_atual:
        print(f"Raspando a página: {url_atual}")
        try:
            response = http_session.get(url_atual)
            # Lança uma exceção para status HTTP ruins (4xx ou 5xx). Mais robusto que checar o status code.
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_books = soup.find_all("article", class_="product_pod")

            if not page_books:
                print("Nenhum livro encontrado nesta página. Encerrando.")
                break

            # === PARTE COMPLETADA: EXTRAÇÃO DOS DADOS ===
            for book_pod in page_books:
                titulo = book_pod.h3.a["title"]
                
                preco_texto = book_pod.find("p", class_="price_color").text
                # Extrai apenas o valor numérico do preço
                preco = float(re.search(r"£([\d.]+)", preco_texto).group(1))
                
                nota_classes = book_pod.find("p", class_="star-rating")["class"]
                nota = converter_nota_para_int(nota_classes)

                # Adiciona os dados extraídos à lista principal
                all_books_data.append({
                    "Titulo": titulo,
                    "Preco (£)": preco,
                    "Nota (1-5)": nota
                })
            
            # === PARTE COMPLETADA: LÓGICA DE PAGINAÇÃO ===
            next_button = soup.find("li", class_="next")
            if next_button:
                # Constrói a URL completa da próxima página
                link_proxima_pagina = next_button.a["href"]
                url_atual = urljoin(URL + 'catalogue/', link_proxima_pagina)
            else:
                print("Fim da paginação. Nenhuma página 'next' encontrada.")
                url_atual = None # Encerra o loop while

            # Pausa respeitosa para não sobrecarregar o servidor
            time.sleep(0.5)

        # === PARTE REFINADA: TRATAMENTO DE ERROS ===
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de rede ao acessar {url_atual}: {e}")
            break # Interrompe o scraper em caso de falha de conexão

    print("-" * 30)
    if all_books_data:
        print(f"Scraping finalizado! {len(all_books_data)} livros foram encontrados.")
        # Exibe os dados do primeiro livro como exemplo
        print("Exemplo do primeiro livro encontrado:")
        print(all_books_data[0])
    else:
        print("Nenhum livro foi raspado.")
    
    return all_books_data

# --- Execução do Script ---
if __name__ == "__main__":
    livros = scrape_books()




    
    
            