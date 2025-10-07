import sqlite3
from fastapi import APIRouter, HTTPException, Depends, status
from src.utils.db import SetupDatabase
from typing import Optional
from src.api.models import HealthStatus
from fastapi.security import OAuth2PasswordRequestForm
from src.scripts.scraper import ScraperBook
from datetime import timedelta
from .auth import (
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/v1")

@router.get("/")
def index():
    return {"message": "Bem-vindo à API de Livros! Acesse /docs para ver a documentação."}

@router.get("/books/search")
def search_books(
    title: Optional[str] = None, 
    category: Optional[str] = None,
    conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)
):
    """
    Busca livros por título e/ou categoria.
    """
    if not title and not category:
        raise HTTPException(
            status_code=400, 
            detail="Forneça um 'title' ou 'category' para a busca."
        )
    
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()

        query_base = "SELECT * FROM book_api_fiap WHERE "
        conditions = []
        params = []

        if title:
            # Usamos LIKE para busca parcial e case-insensitive
            conditions.append("lower(title) LIKE ?")
            params.append(f"%{title.lower()}%")
        
        if category:
            # Usamos = para busca exata e case-insensitive na categoria
            conditions.append("lower(category) = ?")
            params.append(category.lower())

        # AQUI ESTÁ A MUDANÇA: Usamos 'OR' para uma busca "E/OU"
        # Isso retornará livros que correspondam ao título OU à categoria.
        query_final = query_base + " OR ".join(conditions)
        
        cursor.execute(query_final, tuple(params))
        rows = cursor.fetchall()
        
        books = [dict(row) for row in rows]
        return books
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livro: {e}")

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
    
@router.get("/categories")
def categories(conexao: sqlite3.Connection = Depends(SetupDatabase.get_db_connection)):
    try:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        query = "SELECT DISTINCT category FROM book_api_fiap WHERE lower(availability) LIKE '%in stock%' ORDER BY category"
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

# --- BANCO DE DADOS DE USUÁRIOS SIMULADO ---
# Em um projeto real, isso viria de um banco de dados.
# A senha 'testpassword' foi "hasheada" e o resultado está abaixo.
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$dQ4BQOidk/Leey+lFMJ4rw$JKenTSQe+mr7WkhHsIMEQ5qurAe11rJj3lJoEUKQM0E",
        "role": "admin"
    }
}

@router.post("/auth/login", tags=["Autenticação"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica um usuário e retorna um token de acesso JWT.
    """
    user = fake_users_db.get(form_data.username)

    # Usa a senha truncada na verificação para garantir consistência.
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/scraping/trigger", tags=["Admin"])
def trigger_scraping(current_user: dict = Depends(get_current_user)):
    """
    Um endpoint protegido que só pode ser acessado com um token JWT válido.
    Inicia o processo de scraping.
    """
    # O código aqui só será executado se o token for válido.
    # A variável 'current_user' contém o payload do token (ex: {"username": "admin"}).
    
    print(f"Scraping iniciado pelo usuário: {current_user['username']}")
    
    scraper = ScraperBook()
    books = scraper.scrape_books()
    if books:
        scraper.save_on_db(books)
        print("INFO:     Scraping e salvamento de dados concluídos.")
    else:
        print("WARNING:  Nenhum livro foi encontrado durante o scraping.")