# Tech Challenge - Fase 1: API de Livros

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

## 📖 Descrição do Projeto

Este projeto consiste na criação de uma API pública para consulta de livros, desenvolvida como parte do Tech Challenge da Fase 1 de Machine Learning Engineering. O objetivo principal é construir um pipeline completo, desde a extração de dados via web scraping, passando pelo armazenamento e transformação, até a disponibilização desses dados através de uma API RESTful robusta e documentada.

A arquitetura foi pensada para ser modular e escalável, servindo como a base para futuros sistemas de recomendação e modelos de Machine Learning.

## 🏛️ Arquitetura

O projeto segue uma arquitetura simples e desacoplada:

1.  **Web Scraper (`src/scripts`):** Um script Python responsável por extrair os dados do site [books.toscrape.com](https://books.toscrape.com/) e salvá-los em um banco de dados.
2.  **Banco de Dados (`src/Utils`):** Um banco de dados SQLite (`book_api.db`) é utilizado para armazenar os dados dos livros de forma estruturada. Ele é criado e populado na inicialização da aplicação.
3.  **API RESTful (`src/api`):** Construída com FastAPI, a API expõe os dados do banco através de diversos endpoints, com lógica de negócios, validação e autenticação.
4.  **Cliente:** Qualquer aplicação que consuma os dados da API (navegador, outra aplicação, etc.).

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI:** Framework web para a construção da API.
* **Uvicorn:** Servidor ASGI para executar a aplicação FastAPI.
* **SQLite:** Banco de dados relacional para armazenamento dos dados.
* **Pandas:** Utilizado no script de scraping para manipulação e inserção dos dados em massa.
* **BeautifulSoup4 & Requests:** Bibliotecas para extração de dados (Web Scraping).
* **Passlib & Python-JOSE:** Bibliotecas para implementação da autenticação com JWT (Hashing de senhas e geração/validação de tokens).

## ⚙️ Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**1. Clone o Repositório**
```bash
git clone <url-do-seu-repositorio>
cd <nome-do-seu-repositorio>
```

**2. Crie e Ative um Ambiente Virtual**
É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.
```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar no Linux/macOS
source venv/bin/activate

# Ativar no Windows
.\venv\Scripts\activate
```

**3. Instale as Dependências**
Todas as bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

## ▶️ Instruções para Execução

Com o ambiente configurado, inicie a aplicação com o servidor Uvicorn.

```bash
uvicorn src.main:app --reload
```
* `--reload`: Ativa o modo de desenvolvimento, que reinicia o servidor automaticamente após alterações no código.

Ao iniciar, a aplicação irá:
1.  Criar o banco de dados `book_api.db` (se não existir).
2.  Executar o script de web scraping para popular o banco com os dados dos livros.
3.  Iniciar o servidor da API.

A aplicação estará disponível em `http://127.0.0.1:8000`.

## 📚 Documentação da API

A API possui uma documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI. Para acessá-la, visite:

**`http://127.0.0.1:8000/docs`**

Abaixo estão listados os principais endpoints disponíveis.

---
### Endpoints Públicos

#### Health Check
Verifica o status da API e a conectividade com o banco de dados.

* **Endpoint:** `GET /api/v1/health`
* **Exemplo de Resposta (Sucesso):**
    ```json
    {
      "api_status": "ok",
      "db_status": "ok"
    }
    ```

#### Listar Todos os Livros
Retorna uma lista de todos os livros disponíveis na base de dados.

* **Endpoint:** `GET /api/v1/books`
* **Exemplo de Resposta:**
    ```json
    [
      {
        "id": 1,
        "title": "A Light in the Attic",
        "category": "Poetry",
        "price": "51.77",
        ...
      },
      ...
    ]
    ```

#### Buscar Livro por ID
Retorna os detalhes de um livro específico pelo seu ID.

* **Endpoint:** `GET /api/v1/books/{id}`
* **Exemplo de Resposta (id=1):**
    ```json
    {
      "id": 1,
      "category": "Poetry",
      "title": "A Light in the Attic",
      "description": "It's hard to imagine a world without A Light in the Attic...",
      "price": "51.77",
      "tax": "0.00",
      "availability": "In stock (22 available)"
    }
    ```

#### Listar Categorias
Retorna uma lista com todas as categorias de livros únicas.

* **Endpoint:** `GET /api/v1/categories`
* **Exemplo de Resposta:**
    ```json
    [
      "Add a comment",
      "Art",
      "Autobiography",
      ...
    ]
    ```
    
#### Buscar Livros (Filtro)
Busca livros por título e/ou categoria. A busca é opcional e combinada com `OR`.

* **Endpoint:** `GET /api/v1/books/search`
* **Parâmetros de Consulta:**
    * `title` (opcional): Parte do título do livro.
    * `category` (opcional): Nome da categoria.
* **Exemplo de Chamada:**
    ```bash
    curl -X GET "[http://127.0.0.1:8000/api/v1/books/search?category=Music](http://127.0.0.1:8000/api/v1/books/search?category=Music)"
    ```
* **Exemplo de Resposta:**
    ```json
    [
      {
        "id": 3,
        "category": "Music",
        "title": "Rip it Up and Start Again",
        ...
      }
    ]
    ```

---
### Endpoints de Autenticação

#### Obter Token de Acesso
Autentica um usuário com `username` e `password` e retorna um token de acesso JWT.

* **Endpoint:** `POST /api/v1/auth/login`
* **Corpo da Requisição:** `application/x-www-form-urlencoded`
    * `username`: "admin"
    * `password`: "testpassword"
* **Exemplo de Resposta:**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

---
### Endpoints Protegidos

#### Disparar Web Scraping
Endpoint de exemplo protegido por autenticação JWT. Somente usuários autenticados podem acioná-lo.

* **Endpoint:** `POST /api/v1/scraping/trigger`
* **Autenticação:** Requer um token JWT no cabeçalho `Authorization`.
    * `Authorization: Bearer <seu_token_jwt>`
* **Exemplo de Chamada:**
    ```bash
    curl -X POST "[http://127.0.0.1:8000/api/v1/scraping/trigger](http://127.0.0.1:8000/api/v1/scraping/trigger)" -H "Authorization: Bearer eyJhbGciOiJI..."
    ```
* **Exemplo de Resposta:**
    ```json
    {
      "message": "Scraping iniciado com sucesso pelo usuário admin!"
    }
    ```

## 🗂️ Estrutura do Projeto

O código do projeto está organizado em módulos para facilitar a manutenção e escalabilidade.

```
.
├── .venv/                  # Ambiente virtual
├── src/                    # Código fonte da aplicação
|   ├── template/           # Arquivos estáticos (ex: index.html) 
|   |   └── index.html                      
│   ├── api/                # Módulos da API (rotas, modelos, autenticação)
│   ├── scripts/            # Scripts independentes (ex: scraper)
│   └── utils/              # Funções utilitárias (ex: conexão com DB)
├── book_api.db             # Arquivo do banco de dados SQLite
├── main.py                 # Arquivo principal da aplicação FastAPI                            
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```