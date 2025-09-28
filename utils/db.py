import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

class SetupDatabase():

    @staticmethod
    def connection_database():
        load_dotenv()

        DB_USER  = os.getenv("DB_USER")
        DB_PASSWORD  = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        try:
            engine = create_engine(DATABASE_URL, echo=False)

            with engine.connect() as connection:
                print("Conexão com o PostgreSQL realizada com sucesso!")

                result = connection.execute(text("SELECT version()"))
                for row in result:
                    print(f"Versão do PostgreSQL: {row[0]}")

        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
            print("Por favor, verifique se:")
            print("- O servidor PostgreSQL está rodando.")
            print("- As credenciais (usuário, senha, host, porta, nome do banco) estão corretas.")


if __name__ == "__main__":
    SetupDatabase.connection_database()
