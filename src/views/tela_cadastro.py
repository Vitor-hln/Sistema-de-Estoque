import tkinter as tk
from tkinter import ttk, messagebox
from database.database import conectar
from models.product import Produto
from repositories.product_repository import ProductRepository
from controllers.product_controller import ProductController

class TelaCadastro(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Título da tela
        tk.Label(self, text="Cadastro", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Criar formulário e lista de produtos
        self.criar_formulario()
        self.criar_lista_produtos()

        # Chamar atualização da lista ao abrir o app
        self.atualizar_lista_produtos()  # ✅ Agora a lista será carregada automaticamente

    def criar_formulario(self):
        """Cria o formulário de cadastro"""
        form_frame = tk.LabelFrame(self, text="Dados do Produto", padx=20, pady=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Campos do formulário
        tk.Label(form_frame, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=5)
        self.nome_entry = tk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(form_frame, text="Preço por Unidade (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.valor_entry = tk.Entry(form_frame, width=40)
        self.valor_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(form_frame, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=5)
        self.qtd_entry = tk.Entry(form_frame, width=40)
        self.qtd_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Lote:").grid(row=3, column=0, sticky="w", pady=5)
        self.lote_entry = tk.Entry(form_frame, width=40)
        self.lote_entry.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Descrição:").grid(row=4, column=0, sticky="w", pady=5)
        self.descricao_text = tk.Text(form_frame, width=40, height=3)
        self.descricao_text.grid(row=4, column=1, sticky="w", pady=5)
        
    
        # Botões
        # Criar o frame que conterá os botões dentro do form_frame
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=5, rowspan=1, sticky="ne", padx=80, pady=10)  # Alinhar à direita (nordeste - "ne")

        # Botão "Limpar" (Acima)
        btn_limpar = tk.Button(btn_frame, text="Limpar", command=self.limpar_campos, width=15, bg="gray", fg="white")
        btn_limpar.pack(side="top", fill="x", pady=5)  # "top" para ficar acima do botão Salvar

        # Botão "Salvar" (Abaixo)
        btn_salvar = tk.Button(btn_frame, text="Salvar", command=self.salvar, width=15, bg="#4a86e8", fg="white")
        btn_salvar.pack(side="top", fill="x")  # "top" mantém abaixo do Limpar


    
    def criar_lista_produtos(self):
        lista_frame = tk.LabelFrame(self, text="Produtos Cadastrados", padx=20, pady=10)
        lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview para listar os produtos
        colunas = ("Nome", "Descrição", "Preço", "QTD", "Lote")
        self.tabela = ttk.Treeview(lista_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos da tabela
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=100, anchor="center")
        
        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar tabela e scrollbar
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame dos botões
        btn_frame = tk.Frame(lista_frame)
        btn_frame.pack(fill="x", pady=5)

        # Botão Editar (Fica no topo)
        self.btn_editar = tk.Button(btn_frame, text="Editar", command=self.editar_produto, width=15)
        self.btn_editar.pack(pady=3, padx=10)  # Adiciona um espaço entre os botões

        # Botão Excluir (Fica abaixo)
        self.btn_excluir = tk.Button(btn_frame, text="Excluir", command=self.excluir_produto, 
                                     width=15, bg="#f44336", fg="white")
        self.btn_excluir.pack(pady=3, padx=10)

        self.tabela.column('Descrição', width=100)
        self.tabela.column('Preço', width=40)
        self.tabela.column('QTD', width=30)


        
    def carregar_produtos(self):
        self.tabela.delete(*self.tabela.get_children())  # Limpar lista antes de carregar novos dados
        produtos = self.produto_repository.listar_todos()  # Buscar produtos do banco
        for produto in produtos:
            self.tabela.insert("", "end", values=(produto["id"], produto["nome"], produto["valor"], produto["quantidade"], produto["lote"]))
    

    def salvar(self):
       # Obter os valores dos campos do formulário
       nome = self.nome_entry.get()
       descricao = self.descricao_text.get("1.0", "end-1c")
       lote = self.lote_entry.get()
       valor = self.valor_entry.get()
       quantidade = self.qtd_entry.get()

       # Conectar ao banco de dados
       conexao = conectar()
       cursor = conexao.cursor()
       
       try:
           if hasattr(self, 'id_produto') and self.id_produto is not None:
               # Modo edição: atualizar o registro existente
               query = """
                   UPDATE produtos 
                   SET nome = %s, quantidade = %s, valor = %s
                   WHERE id = %s
               """
               parametros = (nome, quantidade, valor, lote, self.id_produto)
               cursor.execute(query, parametros)
           else:
               # Modo cadastro: inserir um novo produto
               query = """
                   INSERT INTO produtos (nome, quantidade, valor, lote)
                   VALUES (%s, %s, %s, %s)
               """
               parametros = (nome, quantidade, valor, lote)
               cursor.execute(query, parametros)
               
           conexao.commit()
           messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
       except Exception as e:
           messagebox.showerror("Erro", f"Erro ao salvar o produto: {e}")
       finally:
           cursor.close()
           conexao.close()


    def limpar_campos(self):
        # Função para limpar os campos do formulário
        self.nome_entry.delete(0, "end")
        self.descricao_text.delete("1.0", "end")
        self.valor_entry.delete(0, "end")
        self.qtd_entry.delete(0, "end")
        self.lote_entry.delete(0, "end")
    

    def editar_produto(self):
        # Seleciona o item da tabela
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
            return
            
        # Obter valores do item selecionado
        valores = self.tabela.item(selecao[0], "values")
        
        # Preencher campos com os valores atuais
        self.nome_entry.delete(0, "end")
        self.nome_entry.insert(0, valores[1])
        
        self.valor_entry.delete(0, "end")
        self.valor_entry.insert(0, valores[2])
        
        self.qtd_entry.delete(0, "end")
        self.qtd_entry.insert(0, valores[3])

        self.lote_entry.delete(0, "end")
        self.lote_entry.insert(0, valores[4])
    

    def excluir_produto(self):
        """Excluir um produto do banco de dados e atualizar a interface"""
        selecao = self.tabela.selection()  # Obtém o item selecionado
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir!")
            return

        # Pega os valores da linha selecionada
        valores = self.tabela.item(selecao[0], "values")
        produto_id = valores[0]  # O ID do produto está na primeira coluna

        # Confirmação de exclusão
        if messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja excluir o produto {produto_id}?"):
            controller = ProductController()  # Criar uma instância do controlador
            sucesso = controller.remover_produto(produto_id)  # Chamar método de exclusão

            if sucesso:
                self.tabela.delete(selecao)  # Remove da interface
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                self.atualizar_lista_produtos()  # Atualizar a tabela após a exclusão
            else:
                messagebox.showerror("Erro", "Erro ao excluir o produto no banco de dados!")

    
    def atualizar_lista_produtos(self):
        """Atualiza a lista de produtos na interface"""
        self.tabela.delete(*self.tabela.get_children())  # Limpar tabela antes de carregar os novos dados

        controller = ProductController()  # Criando uma instância do controlador
        produtos = controller.listar_produtos()  # Chamando o método corretamente

        for produto in produtos:
             self.tabela.insert("", "end", values=(  
               produto.get("nome", "N/A"), 
               produto.get("descricao", "N/A"),  # Agora corretamente incluído
               produto.get("valor", "N/A"), 
               produto.get("quantidade", "N/A"),  
               produto.get("lote", "N/A")
        ))
