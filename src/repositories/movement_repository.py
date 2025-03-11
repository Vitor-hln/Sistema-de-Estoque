import datetime
import mysql.connector
import configparser

class MovementRepository:
    def __init__(self):
        self.config = self._load_config()     # Carrega as configurações do banco de dados   


    def _load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')# Certifique-se de que o arquivo config.ini está no mesmo diretório ou ajuste o caminho conforme necessário
        return config
    

    def _get_connection(self):      # Estabelece a conexão com o banco de dados
        return mysql.connector.connect(
            host=self.config['database']['host'],
            user=self.config['database']['user'],
            password=self.config['database']['password'],
            database=self.config['database']['database']
        )
    
    def _init_db(self):
        # Cria a tabela de produtos se ela não existir
        query = '''
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
           data_hora DATETIME NOT NULL,
           produto_id INT NOT NULL,
           tipo VARCHAR(10) NOT NULL,
           quantidade INT NOT NULL,
           usuario_id INT NOT NULL,
           observacoes TEXT,
           FOREIGN KEY (produto_id) REFERENCES produtos(id),
           FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        '''
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def registrar_movimentacao(self, data_hora, produto_id, tipo, quantidade, usuario, observacoes, solicitante):   # Registra uma movimentação de estoque

        if data_hora is None:
          from datetime import datetime
          data_hora = datetime.now()
        
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            # Insere a movimentação no banco de dados
            cursor.execute('''
                INSERT INTO movimentacoes (data_hora, produto_id, tipo, quantidade, usuario, observacoes, solicitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (data_hora, produto_id, tipo, quantidade, usuario, observacoes, solicitante))
            
            # Atulaliza o estoque do produto
            if tipo == 'Entrada':
                cursor.execute('''
                UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s''', (quantidade, produto_id))
            else: # tipo == 'saida'
                # Verifica se há estoque suficiente para a saída
                cursor.execute('SELECT quantidade FROM produtos WHERE id = %s', (produto_id,))
                estoque_atual = cursor.fetchone()[0]
                if estoque_atual >= quantidade:
                    cursor.execute('''UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s''', (quantidade, produto_id))
                else:
                    raise ValueError('Estoque insuficiente para a saída')     # Lança uma exceção se o estoque for insuficiente
                
            connection.commit()
            return True, "Movimentação registrada com sucesso"
        except Exception as e:
            connection.rollback()
            return False, f"Erro ao registrar movimentação: {str(e)}"
        finally:
            cursor.close()

    def listar_movimentacoes(self, limit=100):
        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("""
            SELECT 
            m.tipo, 
            m.quantidade, 
            m.solicitante,
            m.usuario, 
            p.nome AS produto, 
            m.data_hora,
            (
                SELECT COALESCE(SUM(
                    CASE 
                        WHEN m2.tipo = 'Entrada' THEN m2.quantidade  -- Somar nas Entradas
                        WHEN m2.tipo = 'Saída' THEN -m2.quantidade   -- Subtrair nas Saídas
                        ELSE 0 
                    END
                ), 0)
                FROM movimentacoes m2
                WHERE m2.produto_id = m.produto_id 
                AND m2.data_hora <= m.data_hora
            ) AS qtd_atualizada
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        ORDER BY m.data_hora ASC;
        """)

            movimentacoes = cursor.fetchall()

            return movimentacoes
        except Exception as e:
            print(f"Erro ao buscar movimentações: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()