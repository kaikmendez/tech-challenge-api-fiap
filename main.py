from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from src.api.routes import router
from src.utils.db import SetupDatabase
from src.scripts.scraper import ScraperBook

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Função que executa código na inicialização e no desligamento da API.
    """
    print("INFO:     Aplicação iniciando...")
    SetupDatabase.setup_initial_database()
    
    # (Opcional) Executa o scraping na inicialização
    # print("INFO:     Iniciando processo de scraping no startup...")
    # scraper = ScraperBook()
    # books = scraper.scrape_books()
    # if books:
    #     scraper.save_on_db(books)
    #     print("INFO:     Scraping e salvamento de dados concluídos.")
    # else:
    #     print("WARNING:  Nenhum livro foi encontrado durante o scraping.")
    
    yield
    print("INFO:     API sendo desligada.")


app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_welcome_page():
    """
    Serve a página HTML de boas-vindas a partir do arquivo index.html.
    """
    try:
        with open("src/api/template/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Erro: Arquivo index.html não encontrado.</h1>", status_code=500)

app.include_router(router)