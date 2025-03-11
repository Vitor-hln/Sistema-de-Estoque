import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers import movement_controller
from models.stock_movement import Movimentacao
from repositories.product_repository import ProductRepository
from repositories.movement_repository import MovementRepository
from controllers.movement_controller import MovimentacaoController


class TelaMovimentacao(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Repositórios
        self.produto_repository = ProductRepository()
        self.movement_repository = MovementRepository()
        
        # Título da tela
        tk.Label(self, text="Movimentação de Estoque", font=("Helvetica", 16, "bold")).pack(pady=5)
        
        # Frame para operações
        op_frame = tk.LabelFrame(self, text="Operação", padx=20, pady=1)
        op_frame.pack(fill="both", padx=20, pady=10)
        
        # Selecionar tipo de operação
        tk.Label(op_frame, text="Tipo de Operação:  ").grid(row=0, column=0, sticky="w", pady=5)
        
        self.tipo_operacao = tk.StringVar(value="entrada")
        rb_entrada = tk.Radiobutton(op_frame, text="Entrada", variable=self.tipo_operacao, value="entrada")
        rb_entrada.grid(row=0, column=1, sticky="w", pady=5)
        
        rb_saida = tk.Radiobutton(op_frame, text="Saída", variable=self.tipo_operacao, value="saida")
        rb_saida.grid(row=0, column=2, sticky="w", pady=5)
        
        # Selecionar produto
        tk.Label(op_frame, text="Produto:").grid(row=1, column=0, sticky="w", pady=5)
        self.produto_cb = ttk.Combobox(op_frame, width=40)
        self.produto_cb.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)
        
        # Carregar produtos do banco de dados
        self.carregar_produtos()
        
        # Funcionario Responsável (está como usuario no banco de dados)
        tk.Label(op_frame, text="Responsável:").grid(row=2, column=0, sticky="w", pady=5)
        self.funcionario_entry = tk.Entry(op_frame, width=20)
        self.funcionario_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Solicitante
        tk.Label(op_frame, text="Solicitante:").grid(row=3, column=0, sticky="w", pady=5)
        self.solicitante_entry = tk.Entry(op_frame, width=20)
        self.solicitante_entry.grid(row=3, column=1, sticky="w", pady=5)

        # Quantidade
        tk.Label(op_frame, text="Quantidade:").grid(row=4, column=0, sticky="w", pady=5)
        self.quantidade_entry = tk.Entry(op_frame, width=10)
        self.quantidade_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        # Observações
        tk.Label(op_frame, text="Observações:").grid(row=5, column=0, sticky="w", pady=5)
        self.obs_text = tk.Text(op_frame, width=35, height=2)
        self.obs_text.grid(row=5, column=1, columnspan=2, sticky="w", pady=5)
        
        # Botão para registrar movimentação
        # Criar um espaço abaixo antes do botão
        op_frame.rowconfigure(5, minsize=20)  # Garante espaço extra

        # Botão para registrar movimentação em uma linha abaixo
        self.btn_movimentar = tk.Button(op_frame, text="Registrar Movimentação", 
                                        command=self.adicionar_movimentacao, width=20,
                                        bg="#4a86e8", fg="white")
        self.btn_movimentar.grid(row=5, column=15, columnspan=2, sticky="e", pady=10, padx=(120,0))  # Usando grid em vez de pack
        
        # Frame para histórico de movimentações
        self.criar_historico()
        # Carregar movimentações existentes
        self.carregar_movimentacoes()
    
    def carregar_produtos(self):
        """Carrega produtos do banco de dados para o combobox"""
        produtos = self.produto_repository.listar_todos()
        self.produto_cb['values'] = [produto['nome'] for produto in produtos]
    
    def criar_historico(self):
        historico_frame = tk.LabelFrame(self, text="Histórico de Movimentações", padx=20, pady=10)
        historico_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview para listar as movimentações
        colunas = ("Tipo", "QTD", "Peças", "QTD Atual", "Responsável", "Solicitante", "Data/Hora")
        self.tabela = ttk.Treeview(historico_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos da tabela
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=120, anchor="center")
        
        # Ajustar tamanhos específicos
        self.tabela.column("Tipo",width=50)
        self.tabela.column("Data/Hora", width=110)
        self.tabela.column("Peças", width=100)
        self.tabela.column("QTD", width=40)
        self.tabela.column("QTD Atual", width=50)
        self.tabela.column("Responsável", width=50)
        self.tabela.column("Solicitante", width=50)
        

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(historico_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar tabela e scrollbar
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def carregar_movimentacoes(self):
        """Carrega movimentações do banco de dados para a tabela"""

        self.tabela.delete(*self.tabela.get_children()) # Limpar tabela antes de carregar os novos dados
    
    
        controller = MovimentacaoController() # Criando uma instância do controlador
        movimentacoes = controller.listar_mov()
        for mov in movimentacoes:
            data_formatada = mov['data_hora'].strftime("%d/%m/%Y %H:%M:%S")
            self.tabela.insert(
                "", 0, values=(
                mov.get('tipo', 'N/A'),  
                mov.get('quantidade', 0),
                mov.get('produto', 'Desconhecido'),
                mov.get('qtd_atualizada', 0),
                mov.get('usuario', 'Desconhecido'),
                mov.get('solicitante', 'Desconhecido'),
                data_formatada
            ))

    
    def adicionar_movimentacao(self):
        # Função para registrar movimentação
        produto = self.produto_cb.get()
        
        # Validando campos
        if not produto:
            messagebox.showerror("Erro", "Selecione um produto!")
            return
        
        usuario = self.funcionario_entry.get()
        
        try:
            quantidade = int(self.quantidade_entry.get())
            if quantidade <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            return
        
        tipo = "Entrada" if self.tipo_operacao.get() == "entrada" else "Saída"
        observacoes = self.obs_text.get("1.0", "end-1c")

       
        
        # Obter ID do produto
        produto_id = self.produto_repository.obter_id_por_nome(produto)
        if not produto_id:
            messagebox.showerror("Erro", "Produto não encontrado no banco de dados!")
            return
        
        # Registrar movimentação no banco de dados
        sucesso, mensagem = self.movement_repository.registrar_movimentacao(
            produto_id=produto_id,
            tipo=tipo,
            quantidade=quantidade,
            usuario=usuario,
            observacoes=observacoes,
            data_hora=datetime.now(),
            solicitante=self.solicitante_entry.get()
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", f"Movimentação de {tipo} registrada com sucesso!")
            
            # Limpar campos
            self.quantidade_entry.delete(0, "end")
            self.obs_text.delete("1.0", "end")
            
            # Atualizar a tabela de histórico
            self.carregar_movimentacoes()
        else:
            messagebox.showerror("Erro", mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaMovimentacao(root)
    app.pack(fill="both", expand=True)
    root.mainloop()