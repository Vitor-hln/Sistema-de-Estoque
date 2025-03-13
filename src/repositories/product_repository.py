import mysql.connector
import sys
import os

# Adicionar o diretório raiz ao path para evitar problemas de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.database.database import conectar

class ProductRepository:
    def __init__(self):
        pass  # Não precisamos mais carregar configurações

    def _get_connection(self):
        """Estabelece a conexão com o banco de dados usando a função conectar()"""
        return conectar()

    def adicionar_produto(self, nome, descricao, valor, quantidade, lote=None):
        """Insere um novo produto no banco de dados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            if lote:  # Se 'lote' for fornecido
                cursor.execute("""
                INSERT INTO produtos (nome, descricao, valor, quantidade, lote)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, descricao, valor, quantidade, lote))
            else:  # Caso não haja lote
                cursor.execute("""
                INSERT INTO produtos (nome, descricao, valor, quantidade)
                VALUES (%s, %s, %s, %s)
            """, (nome, descricao, valor, quantidade))

            conn.commit()
            return True  # Retorna sucesso
        except mysql.connector.Error as err:
            print(f"Erro ao inserir produto: {err}")
            conn.rollback()
            return False  # Retorna falha
        finally:
            cursor.close()
            conn.close()

    def listar_todos(self):
        """Lista todos os produtos do banco de dados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = []
        for row in cursor.fetchall():
           produtos.append({
            'id': row[0],
            'nome': row[1],
            'descricao': row[2],  
            'valor': row[3],
            'quantidade': row[4],
            'lote': row[5] 
        })
        conn.close()
        return produtos  # Retorna a lista de produtos

    def obter_produto_por_id(self, id):
        """Obtém um produto pelo ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos p LEFT JOIN categorias c ON p.categoria_id = c.id WHERE id = %s", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'valor': row[3],
                'categoria_id': row[4],
                'quantidade': row[5]
            }
        return None  # Retorna None se o produto não for encontrado

    def obter_id_por_nome(self, nome):
        """Obtém o ID de um produto pelo nome"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM produtos WHERE nome = %s", (nome,))
        row = cursor.fetchone()  # Obtém a primeira linha do resultado da consulta   
        conn.close()
        return row[0] if row else None  # Retorna o ID se o produto for encontrado, caso contrário, retorna None

    def remover_produto(self, produto_id):
        """Remove um produto do banco de dados pelo ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            conn.commit()  # Confirmar a exclusão no banco de dados
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao excluir produto: {err}")
            conn.rollback()  # Reverter em caso de erro
            return False
        finally:
            cursor.close()
            conn.close()
