import os
import sqlalchemy
from dotenv import load_dotenv

@staticmethod
def connection_database():
    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
        engine = sqlalchemy.create_engine(database_url, echo=False)

        with engine.connect() as connection:
            print("Conexão com o PostgreSQL realizada com sucesso!")

        result = connection.execute(sqlalchemy.text("SELECT version()"))
        for row in result:
            print(f"Versão do PostgreSQL: {row[0]}")

    except ValueError as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        print("Por favor, verifique se:")
        print("- O servidor PostgreSQL está rodando.")
        print("- As credenciais (usuário, senha, host, porta, nome do banco) estão corretas.")
