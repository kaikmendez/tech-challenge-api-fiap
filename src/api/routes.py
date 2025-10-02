from fastapi import APIRouter, HTTPException, Depends
from src.utils.db import SetupDatabase
import sqlite3

router = APIRouter(prefix="/api/v1")

@router.get("/")
def index():
    return {"message": "Hello, World"}

@router.get("/books")
def get_all_books(conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
    # Agora, a variável 'conexao' é nova e segura para ser usada aqui
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM book_api_fiap")
        rows = cursor.fetchall()
        books = [dict(row) for row in rows]
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {e}")

@router.get("/books/{id}")
def get_book_by_id(id: int, conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        query = "SELECT * FROM book_api_fiap WHERE id = ?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao buscar livro: {e}')