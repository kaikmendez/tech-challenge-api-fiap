import sqlite3

class SetupDatabase():

    @staticmethod
    def setup_initial_database():
        """
        Cria a conexão e a tabela, depois fecha.
        Deve ser chamada apenas uma vez.
        """
        conexao = None
        try:
            conexao = sqlite3.connect("book_api.db", check_same_thread=False)
            cursor = conexao.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS book_api_fiap (
                id INTEGER PRIMARY KEY,
                category TEXT,
                title TEXT,
                description TEXT,
                price TEXT,
                tax TEXT,
                availability TEXT
            )
            ''')
            
            conexao.commit()
            print("Banco de dados e tabela verificados/criados com sucesso.")
        
        except sqlite3.Error as e:
            print(f"Erro ao configurar o banco de dados: {e}")
        
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def get_db_connection():
        """
        Esta função cria uma nova conexão com o banco para cada requisição,
        entrega para a rota e a fecha no final.
        """
        conexao = sqlite3.connect("book_api.db", check_same_thread=False)
        try:
            yield conexao
        finally:
            conexao.close()