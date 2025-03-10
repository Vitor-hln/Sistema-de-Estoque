from repositories.movement_repository import MovementRepository

class MovimentacaoController:
    def __init__(self): 
        self.mv = MovementRepository()

    def registrar_inclusao(self, produto_id, quantidade, data, usuario):
        # Lógica para registrar a inclusão de um produto no estoque
        self.mv.registrar_movimentacao(produto_id, 'Inclusão', quantidade, data, usuario)

    def regitrar_retirada(self, produto_id, quantidade, data, usuario):
        # Lógica para registrar a retirada de um produto do estoque
        self.mv.registrar_movimentacao(produto_id, 'Retirada', -quantidade, data, usuario)

    def listar_mov(self):
        movimentacoes = self.mv.listar_movimentacoes()
        print(movimentacoes)
        return self.mv.listar_movimentacoes()