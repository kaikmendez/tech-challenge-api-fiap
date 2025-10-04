import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from src.utils.db import SetupDatabase
from typing import Optional
from src.api.models import HealthStatus

router = APIRouter(prefix="/api/v1")

@router.get("/")
def index():
    return {"message": "Bem-vindo à API de Livros! Acesse /docs para ver a documentação."}

@router.get("/books")
def get_all_books(conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
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
            raise HTTPException(status_code=400, detail="Livro não encontrado.")
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao buscar livro: {e}')

@router.get("/books/search")
def search_books(title: Optional[str] = None, category: Optional[str] = None, conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
    """
    Busca livros por título e/ou categoria.
    A busca por título é parcial e case-insensitive.
    """
    if not title and not category:
        raise HTTPException(
            status_code=400, 
            detail="Forneça um 'title' ou 'category' para a busca."
        )
    
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        query = ("SELECT * FROM book_api_fiap WHERE ")
        conditions = []
        params = []

        if title:
            conditions.append("lower(title) like ?")
            params.append(f"%{title.lower}%")

        if category:
            conditions.append("lower(category) like ?")
            params.append(f"%{category.lower}%")

        query = query + " AND ".join(conditions)
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        books = [dict(row) for row in rows]

        return books
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livro: {e}")
    
@router.get("/categories")
def categories(conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        query = "SELECT DISTINCT category FROM book_api_fiap ORDER BY category"
        cursor.execute(query)
        rows = cursor.fetchall()
        categories = [row['category'] for row in rows]
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {e}")
    
@router.get("/health", response_model=HealthStatus, tags=["Status"])
def health_check():
    """
    Verifica o status da API e a conectividade com o banco de dados.
    """
    api_status = "ok"
    db_status = "disconnected"

    try:
        # Tenta criar uma conexão rápida com o banco para verificar a conectividade
        # Usamos uma conexão separada aqui para não depender da injeção de dependência,
        # pois queremos controlar a resposta mesmo em caso de falha.
        conexao = sqlite3.connect("book_api.db", timeout=1)
        
        # Se a conexão foi bem-sucedida, tentamos executar uma consulta simples.
        cursor = conexao.cursor()
        cursor.execute("SELECT 1") # Query simples que não faz nada, só valida a conexão
        
        # Se tudo correu bem até aqui, a conexão está ok
        db_status = "ok"
        
        conexao.close()

    except Exception as e:
        print(f"Health check falhou ao conectar ao DB: {e}")
        db_status = "error"

    return {"api_status": api_status, "db_status": db_status}