from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from src.utils.db import SetupDatabase

router = APIRouter(prefix="/api/v1")
engine = SetupDatabase.connection_database()

@router.get("/")
def index():
    return {"message": "Hello, World"}

@router.get("/books")
def get_all_books():
    """
    Retorna todos os livros disponíveis na base de dados.
    """
    with engine.connect() as coon:
        result = coon.execute(text("SELECT title FROM scraper.book_api_fiap"))
        books = [row[0] for row in result]
        return books
    
@router.get("/books/{id}")
def get_book_by_id(id: int):
    """
    Busca os detalhes de um livro específico pelo seu ID.
    """
    with engine.connect() as coon:
        query = text("SELECT title FROM scraper.book_api_fiap where id = :book_id")
        result = coon.execute(query, {"book_id": id})
        book = {"book": result.fetchone()}
        if book is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return book



    

    