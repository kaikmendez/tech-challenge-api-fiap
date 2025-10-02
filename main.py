# Mantenha os mesmos imports
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.scripts.scraper import ScraperBook
from src.api.routes import router
from src.utils.db import SetupDatabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executa tarefas na inicialização. Agora, de forma síncrona e bloqueante.
    """
    print("INFO:     Rotina de startup iniciada.")

    setup_database = SetupDatabase()
    setup_database.setup_initial_database()

    scraper = ScraperBook()

    print("INFO:     Iniciando processo de scraping (aguarde, isso pode levar um minuto)...")
    
    # Executa as funções diretamente, sem thread separada.
    # O programa vai esperar aqui até que tudo termine.
    books = scraper.scrape_books()
    
    if books:
        print(f"INFO:     Scraping concluído. {len(books)} livros encontrados. Salvando dados...")
        
        scraper.save_to_csv(books)
        scraper.save_on_db(books) # Esta função agora também será aguardada
        
        print("INFO:     Salvamento de dados concluído.")
    else:
        print("WARNING:  Nenhum livro foi encontrado durante o scraping.")
    
    # Somente DEPOIS de tudo acima terminar, a API ficará online.
    yield
    
    print("INFO:     API desligada.")

app = FastAPI(
    title="Book API - Tech Challenge FIAP",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)