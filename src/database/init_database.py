import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def init_database():
    try:
        #Conectar ao MySQL (sem especificar banco de dados ainda)
        conexao = mysql.connector.connect(
          host='localhost',
          user='root',
          password=os.getenv("DB_password", "")
        )

        cursor = conexao.cursor()

        #Criar o banco de dados se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS controle_estoque;")
        print("Banco de dados 'controle_estoque' criado ou já exitente")

        #Conectar ao banco de dados recém-criado
        conexao.database = "controle_estoque"

        #Criar a tabela 'produtos'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            valor DECIMAL(10,2) NOT NULL,
            quantidade INT NOT NULL,
            lote VARCHAR(50) NOT NULL
            );
        """)  # Fixed the syntax error (colon changed to semicolon) and added categoria_id column
        print("Tabela 'produtos' criada ou já existente")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_hora DATETIME NOT NULL,
                produto_id INT NOT NULL,
                tipo VARCHAR(10) NOT NULL,
                quantidade INT NOT NULL,
                usuario VARCHAR(50) NOT NULL,
                observacoes TEXT,
                solicitante VARCHAR(50) NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
        ''')
        print("Tabela 'movimentacoes' criada ou já existente.")
        
        # Commit the changes
        conexao.commit()
        
        print("Configuração do banco de dados concluída!")

    except mysql.connector.Error as erro:
        print(f"Erro ao criar banco de dados ou tabela: {erro}")
    finally:
        #Fechar conexão
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()
