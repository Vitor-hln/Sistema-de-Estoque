class Movimentacao:
    def __init__(self, id, data, tipo, quantidade, produto_id):
        self.id = id
        self.data = data
        self.tipo = tipo # 'entrada' ou 'saida'
        self.quantidade = quantidade
        self.produto_id = produto_id

    def __str__(self):
        # Retorna uma representação de string do objeto Movimentacao
        return f"Movimentacao(id={self.id}, data={self.data}, tipo={self.tipo}, quantidade={self.quantidade}, produto_id={self.produto_id})"
