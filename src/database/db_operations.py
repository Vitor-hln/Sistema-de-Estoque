from database import conectar

class DBoperations:
    """ Classe responsável por operações no banco de dados """

    @staticmethod
    def adicionar_produto(nome, descricao, valor, quantidade, lote):
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            sql = "INSERT INTO produtos (nome, descricao, valor, quantidade, lote) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, descricao, valor, quantidade, lote))
            conexao.commit()
            cursor.close()
            conexao.close()
            return "✅ Produto adicionado com sucesso!"

    @staticmethod
    def listar_produtos():
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor(dictionary=True)  # Retorna os dados como dicionário
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            cursor.close()
            conexao.close()
            return produtos  # Retorna a lista de produtos

    @staticmethod
    def atualizar_produto(produto_id, nome, descricao, valor, quantidade, lote):
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            sql = "UPDATE produtos SET nome=%s, descricao=%s, valor=%s, quantidade=%s, lote=%s WHERE id=%s"
            cursor.execute(sql, (nome, descricao, valor, quantidade, lote, produto_id))
            conexao.commit()
            cursor.close()
            conexao.close()
            return "✅ Produto atualizado com sucesso!"

    @staticmethod
    def remover_produto(produto_id):
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            sql = "DELETE FROM produtos WHERE id=%s"
            cursor.execute(sql, (produto_id,))
            conexao.commit()
            cursor.close()
            conexao.close()
            return "✅ Produto removido com sucesso!"
