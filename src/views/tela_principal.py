"""import tkinter as tk
from tkinter import ttk, messagebox
from .tela_cadastro import TelaCadastro
from .tela_movimentacao import TelaMovimentacao
from .tela_relatorios import TelaRelatorios

class TelaPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Definindo estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usando um tema mais moderno
        
        # Criando o container principal
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Criando o menu de navegação
        self.criar_menu()
        
        # Frame para conteúdo
        self.frame_conteudo = tk.Frame(self.container)
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar tela inicial
        self.mostrar_tela_inicial()
    
    def criar_menu(self):
        # Frame para o menu
        menu_frame = tk.Frame(self.container, bg="#333333")
        menu_frame.pack(side="top", fill="x")
        
        # Botões do menu
        estilo_botao = {"bg": "#333333", "fg": "white", "padx": 15, "pady": 8, 
                       "font": ("Helvetica", 10, "bold"), "bd": 0}
        
        btn_inicio = tk.Button(menu_frame, text="Início", command=self.mostrar_tela_inicial, **estilo_botao)
        btn_inicio.pack(side="left")
        
        btn_produtos = tk.Button(menu_frame, text="Cadastro de Produtos", 
                               command=self.abrir_cadastro_produtos, **estilo_botao)
        btn_produtos.pack(side="left")
        
        btn_movimentacao = tk.Button(menu_frame, text="Movimentação de Estoque", 
                                  command=self.abrir_movimentacao, **estilo_botao)
        btn_movimentacao.pack(side="left")
        
        btn_relatorios = tk.Button(menu_frame, text="Relatórios", 
                                command=self.abrir_relatorios, **estilo_botao)
        btn_relatorios.pack(side="left")
        
    def mostrar_tela_inicial(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        
        # Criar conteúdo da tela inicial
        tk.Label(self.frame_conteudo, text="Sistema de Gerenciamento de Estoque", 
                font=("Helvetica", 20, "bold")).pack(pady=20)
        
        tk.Label(self.frame_conteudo, text="Bem-vindo ao sistema de controle de estoque.", 
                font=("Helvetica", 12)).pack(pady=10)
        
        # Frame para os atalhos
        frame_atalhos = tk.Frame(self.frame_conteudo)
        frame_atalhos.pack(pady=40, fill="x")
        
        # Estilo para botões de atalho
        estilo_atalho = {"width": 25, "height": 4, "font": ("Helvetica", 10, "bold"),
                        "bg": "#4a86e8", "fg": "white", "bd": 0}
        
        # Botões de atalho
        btn_cadastrar = tk.Button(frame_atalhos, text="Cadastrar Produto", 
                                command=self.abrir_cadastro_produtos, **estilo_atalho)
        btn_cadastrar.grid(row=0, column=0, padx=10, pady=10)
        
        btn_movimentar = tk.Button(frame_atalhos, text="Movimentar Estoque", 
                                 command=self.abrir_movimentacao, **estilo_atalho)
        btn_movimentar.grid(row=0, column=1, padx=10, pady=10)
        
        btn_relatorio = tk.Button(frame_atalhos, text="Ver Relatórios", 
                               command=self.abrir_relatorios, **estilo_atalho)
        btn_relatorio.grid(row=0, column=2, padx=10, pady=10)
    
    def abrir_cadastro_produtos(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        
        # Criar tela de cadastro
        tela_cadastro = TelaCadastro(self.frame_conteudo)
        tela_cadastro.pack(fill="both", expand=True)
    
    def abrir_movimentacao(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        
        # Criar tela de movimentação
        tela_movimentacao = TelaMovimentacao(self.frame_conteudo)
        tela_movimentacao.pack(fill="both", expand=True)
    
    def abrir_relatorios(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        
        # Criar tela de relatórios
        tela_relatorios = TelaRelatorios(self.frame_conteudo)
        tela_relatorios.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaPrincipal(root)
    app.pack(fill="both", expand=True)
    root.mainloop()"""
import tkinter as tk
from tkinter import ttk, messagebox
from .tela_cadastro import TelaCadastro
from .tela_movimentacao import TelaMovimentacao
from .tela_relatorios import TelaRelatorios

class TelaPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Definindo estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usando um tema mais moderno

        # Criando o container principal
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Criando o menu de navegação
        self.criar_menu()

        # Frame para conteúdo
        self.frame_conteudo = tk.Frame(self.container)
        self.frame_conteudo.pack(fill="both", expand=True, padx=20, pady=20)

        # Mostrar tela inicial
        self.mostrar_tela_inicial()

    def criar_menu(self):
        # Frame para o menu
        menu_frame = tk.Frame(self.container, bg="#333333")
        menu_frame.pack(side="top", fill="x")

        # Botões do menu
        estilo_botao = {"bg": "#333333", "fg": "white", "padx": 15, "pady": 8,
                        "font": ("Helvetica", 10, "bold"), "bd": 0}


        btn_produtos = tk.Button(menu_frame, text="Cadastro",
                                 command=self.abrir_cadastro_produtos, **estilo_botao)
        btn_produtos.pack(side="left")

        btn_movimentacao = tk.Button(menu_frame, text="Movimentação de Estoque",
                                     command=self.abrir_movimentacao, **estilo_botao)
        btn_movimentacao.pack(side="left")

        btn_relatorios = tk.Button(menu_frame, text="Relatórios",
                                   command=self.abrir_relatorios, **estilo_botao)
        btn_relatorios.pack(side="left")

    def mostrar_tela_inicial(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Criar conteúdo da tela inicial
        tk.Label(self.frame_conteudo, text="Sistema de Gerenciamento de Estoque",
                 font=("Helvetica", 20, "bold")).pack(pady=20)

        tk.Label(self.frame_conteudo, text="Bem-vindo ao sistema de controle de estoque.",
                 font=("Helvetica", 12)).pack(pady=10)

        # Frame para os atalhos (Melhorado para centralizar dinamicamente)
        frame_atalhos = tk.Frame(self.frame_conteudo)
        frame_atalhos.pack(pady=40, fill="both", expand=True)

        # Configurar grid responsivo
        frame_atalhos.grid_columnconfigure(0, weight=1)  # Primeira coluna
        frame_atalhos.grid_columnconfigure(1, weight=1)  # Segunda coluna
        frame_atalhos.grid_columnconfigure(2, weight=1)  # Terceira coluna

        # Estilo para botões de atalho
        estilo_atalho = {"width": 20, "height": 3, "font": ("Helvetica", 10, "bold"),
                         "bg": "#4a86e8", "fg": "white", "bd": 0}

        # Botões de atalho (Usando grid e sticky="ew" para centralizar)
        btn_cadastrar = tk.Button(frame_atalhos, text="Cadastrar Produto",
                                  command=self.abrir_cadastro_produtos, **estilo_atalho)
        btn_cadastrar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_movimentar = tk.Button(frame_atalhos, text="Movimentar Estoque",
                                   command=self.abrir_movimentacao, **estilo_atalho)
        btn_movimentar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_relatorio = tk.Button(frame_atalhos, text="Ver Relatórios",
                                  command=self.abrir_relatorios, **estilo_atalho)
        btn_relatorio.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def abrir_cadastro_produtos(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Criar tela de cadastro
        tela_cadastro = TelaCadastro(self.frame_conteudo)
        tela_cadastro.pack(fill="both", expand=True)

    def abrir_movimentacao(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Criar tela de movimentação
        tela_movimentacao = TelaMovimentacao(self.frame_conteudo)
        tela_movimentacao.pack(fill="both", expand=True)

    def abrir_relatorios(self):
        # Limpar frame de conteúdo
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        # Criar tela de relatórios
        tela_relatorios = TelaRelatorios(self.frame_conteudo)
        tela_relatorios.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Define um tamanho inicial adequado
    app = TelaPrincipal(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
