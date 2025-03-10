import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta

class TelaRelatorios(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Título da tela
        tk.Label(self, text="Relatórios", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Frame para filtros
        filtros_frame = tk.LabelFrame(self, text="Filtros", padx=20, pady=10)
        filtros_frame.pack(fill="x", padx=20, pady=10)
        
        # Tipo de relatório
        tk.Label(filtros_frame, text="Tipo de Relatório:").grid(row=0, column=0, sticky="w", pady=5)
        self.tipo_relatorio = ttk.Combobox(filtros_frame, width=30)
        self.tipo_relatorio['values'] = ["Movimentações de Estoque", "Produtos com Estoque Baixo", 
                                       "Produtos Mais Movimentados", "Valor Total em Estoque"]
        self.tipo_relatorio.current(0)
        self.tipo_relatorio.grid(row=0, column=1, sticky="w", pady=5)
        
        # Período
        tk.Label(filtros_frame, text="Período:").grid(row=1, column=0, sticky="w", pady=5)
        
        periodo_frame = tk.Frame(filtros_frame)
        periodo_frame.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(periodo_frame, text="De:").pack(side="left", padx=(0, 5))
        self.data_inicio = tk.Entry(periodo_frame, width=12)
        self.data_inicio.pack(side="left", padx=(0, 10))
        
        tk.Label(periodo_frame, text="Até:").pack(side="left", padx=(0, 5))
        self.data_fim = tk.Entry(periodo_frame, width=12)
        self.data_fim.pack(side="left")
        
        # Botões de atalho para período
        btn_frame = tk.Frame(filtros_frame)
        btn_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        self.btn_hoje = tk.Button(btn_frame, text="Hoje", command=lambda: self.definir_periodo(0))
        self.btn_hoje.pack(side="left", padx=5)
        
        self.btn_7dias = tk.Button(btn_frame, text="Últimos 7 dias", command=lambda: self.definir_periodo(7))
        self.btn_7dias.pack(side="left", padx=5)
        
        self.btn_30dias = tk.Button(btn_frame, text="Últimos 30 dias", command=lambda: self.definir_periodo(30))
        self.btn_30dias.pack(side="left", padx=5)
        
        # Botão para gerar relatório
        self.btn_gerar = tk.Button(filtros_frame, text="Gerar Relatório", command=self.gerar_relatorio,bg="#4a86e8", fg="white", width=15)
        self.btn_exportar = tk.Button(filtros_frame, text="Exportar Relatório", command=self.exportar_para_csv, bg="#4a86e8", fg="white", width=15)
        
        
        self.btn_gerar.grid(row=3, column=0, sticky="e", pady=10)
        self.btn_exportar.grid(row=3, column=1, sticky="e", pady=10)
        
        # Inicializar com o período de hoje
        self.definir_periodo(0)
        
        # Container para o relatório
        self.relatorio_frame = tk.LabelFrame(self, text="Resultado", padx=20, pady=10)
        self.relatorio_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Mostrar um relatório padrão
        self.gerar_relatorio()
    
    def definir_periodo(self, dias):
        # Define o período baseado no número de dias atrás
        hoje = datetime.now()
        data_fim = hoje.strftime("%d/%m/%Y")
        
        if dias == 0:
            data_inicio = data_fim
        else:
            data_inicio = (hoje - timedelta(days=dias)).strftime("%d/%m/%Y")
        
        self.data_inicio.delete(0, "end")
        self.data_inicio.insert(0, data_inicio)
        
        self.data_fim.delete(0, "end")
        self.data_fim.insert(0, data_fim)
    
    def gerar_relatorio(self):
        # Limpar frame de relatório
        for widget in self.relatorio_frame.winfo_children():
            widget.destroy()
            
        tipo = self.tipo_relatorio.get()
        
        # Criar tabela para relatório
        if tipo == "Movimentações de Estoque":
            self.relatorio_movimentacoes()
        elif tipo == "Produtos com Estoque Baixo":
            self.relatorio_estoque_baixo()
        elif tipo == "Produtos Mais Movimentados":
            self.relatorio_mais_movimentados()
        elif tipo == "Valor Total em Estoque":
            self.relatorio_valor_estoque()
        else:
            tk.Label(self.relatorio_frame, text="Selecione um tipo de relatório").pack()

    def relatorio_movimentacoes(self):
        # Criar treeview para movimento de estoque
        colunas = ("ID", "Data/Hora", "Produto", "Tipo", "Quantidade", "Usuário")
        tabela = ttk.Treeview(self.relatorio_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=100, anchor="center")
        
        # Ajustar larguras específicas
        tabela.column("Data/Hora", width=150)
        tabela.column("Produto", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar na tela
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adicionar dados de exemplo
        for i in range(20):
            data = datetime.now() - timedelta(hours=i*3)
            tipo = "Entrada" if i % 2 == 0 else "Saída"
            quantidade = i + 5
            tabela.insert("", "end", values=(f"{i+1}", data.strftime("%d/%m/%Y %H:%M:%S"), 
                                          f"Produto {i%5 + 1}", tipo, quantidade, "Administrador"))

    def relatorio_estoque_baixo(self):
        # Criar treeview para produtos com estoque baixo
        colunas = ("ID", "Produto", "Estoque Atual", "Estoque Mínimo", "Status")
        tabela = ttk.Treeview(self.relatorio_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=100, anchor="center")
        
        # Ajustar larguras específicas
        tabela.column("Produto", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar na tela
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adicionar dados de exemplo
        for i in range(10):
            estoque_atual = i
            estoque_minimo = 10
            status = "CRÍTICO" if estoque_atual < 5 else "BAIXO"
            
            tabela.insert("", "end", values=(f"{i+1}", f"Produto {i+1}", estoque_atual, 
                                          estoque_minimo, status))
            
            # Aplicar cor de fundo com base no status
            item = tabela.get_children()[-1]
            if status == "CRÍTICO":
                tabela.item(item, tags=("critico",))
            else:
                tabela.item(item, tags=("baixo",))
        
        # Definir cores para as tags
        tabela.tag_configure("critico", background="#ffcccc")
        tabela.tag_configure("baixo", background="#ffffcc")
    
    def relatorio_mais_movimentados(self):
        # Criar treeview para produtos mais movimentados
        colunas = ("Ranking", "Produto", "Total Movimentações", "Entradas", "Saídas")
        tabela = ttk.Treeview(self.relatorio_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=100, anchor="center")
        
        # Ajustar larguras específicas
        tabela.column("Produto", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar na tela
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adicionar dados de exemplo
        for i in range(10):
            entradas = i * 10
            saidas = i * 5
            total = entradas + saidas
            
            tabela.insert("", "end", values=(f"{i+1}", f"Produto {i+1}", total, entradas, saidas))
    
    def relatorio_valor_estoque(self):
        # Criar treeview para valor total em estoque
        colunas = ("ID", "Produto", "Quantidade", "Valor Unitário", "Valor Total")
        tabela = ttk.Treeview(self.relatorio_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=100, anchor="center")
        
        # Ajustar larguras específicas
        tabela.column("Produto", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar na tela
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adicionar dados de exemplo
        for i in range(10):
            quantidade = i * 10
            valor_unitario = 5.0
            valor_total = quantidade * valor_unitario
            
            tabela.insert("", "end", values=(f"{i+1}", f"Produto {i+1}", quantidade, 
                                          f"R$ {valor_unitario:.2f}", f"R$ {valor_total:.2f}"))
            
            
    def exportar_para_csv(self):
           if not hasattr(self, "tabela"):
               messagebox.showwarning("Aviso", "Nenhum relatório foi gerado ainda!")
               return
           
           arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
           
           if not arquivo:
               return
           
           colunas = [self.tabela.heading(col)["text"] for col in self.tabela["columns"]]
           dados = [self.tabela.item(item, "values") for item in self.tabela.get_children()]
           
           with open(arquivo, mode="w", newline="", encoding="utf-8") as f:
               escritor = csv.writer(f)
               escritor.writerow(colunas)
               escritor.writerows(dados)
           
           messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
           
           
           