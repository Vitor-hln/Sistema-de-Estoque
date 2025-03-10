class Produto:
    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    def adicionar_estoque(self, quantidade):
        self.quantidade += quantidade

    def remover_estoque(self, quantidade):
        if quantidade <= self.quantidade:   
            self.quantidade -= quantidade
        else:
            raise ValueError("Quantidade insuficiente em estoque")
        
    def __str__(self):
        return f"Produto: {self.nome}, Descrição: {self.descricao}, Preço: R${self.preco:.2f}, Quantidade: {self.quantidade}"