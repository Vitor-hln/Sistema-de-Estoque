from repositories.product_repository import ProductRepository

class ProductController:
    def __init__(self):
        self.pr = ProductRepository()
    @staticmethod
    def adicionar_produto(nome, descricao, valor, quantidade, lote=None):
        """Adiciona um produto no banco de dados através do repositório"""
        if not nome or not descricao or valor <= 0 or quantidade < 0:
            return "❌ Erro: Dados inválidos para adicionar produto."

        produto_repository = ProductRepository()
        sucesso = produto_repository.adicionar_produto(nome, descricao, valor, quantidade, lote)

        if sucesso:
            return "✅ Produto adicionado com sucesso!"
        else:
            return "❌ Erro ao cadastrar produto no banco de dados!"


    def atualizar_produto(self, produto_id, nome, descricao, valor, quantidade, lote):
        if quantidade < 0 or valor < 0:
            raise ValueError("Preço e quantidade devem ser valores não negativos.")
        self.pr.atualizar_produto(produto_id, nome, descricao, valor, quantidade, lote)

    def remover_produto(self, produto_id):
        """Remove um produto do banco de dados e retorna True se bem-sucedido"""
        try:
            return self.pr.remover_produto(produto_id)
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            return False

    def listar_produtos(self):
        return self.pr.listar_todos()

    def buscar_produto(self, produto_id):
        return self.pr.buscar_produto(produto_id)
