import mysql.connector
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

def conectar():
    try:
        # Criando a conexão com o MySQL
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("DB_PASSWORD", ""),  # Pega a senha do .env
            database="controle_estoque"  
        )
        return conexao
    except mysql.connector.Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None
