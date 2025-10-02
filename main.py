import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.scripts.scraper import ScraperBook
from src.api.routes import router
from src.utils.db import SetupDatabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Esta função executa tarefas quando a API inicia e antes de desligar.
    """
    print("INFO:     Rotina de startup iniciada.")

    setup_database = SetupDatabase()
    setup_database.setup_initial_database()

    scraper = ScraperBook()

    print("INFO:     Iniciando processo de scraping em background...")
    
    # Executa a função síncrona e demorada em uma thread externa
    books = await asyncio.to_thread(scraper.scrape_books)
    
    if books:
        print(f"INFO:     Scraping concluído. {len(books)} livros encontrados. Salvando dados...")
        
        await asyncio.to_thread(scraper.save_to_csv, books)
        await asyncio.to_thread(scraper.save_on_db, books)
        
        print("INFO:     Salvamento de dados concluído.")
    else:
        print("WARNING:  Nenhum livro foi encontrado durante o scraping.")
    
    yield # A API fica online e aceitando requisições a partir deste ponto
    
    print("INFO:     API desligada.")

app = FastAPI(
    title="Book API - Tech Challenge FIAP",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)