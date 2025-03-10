import csv
from sqlite3 import Cursor
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from database import conectar
import openpyxl
from openpyxl.styles import Font
from tkinter import filedialog, messagebox

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
        self.btn_exportar = tk.Button(filtros_frame, text="Exportar Relatório", command=self.exportar_para_excel, bg="#4a86e8", fg="white", width=15)
        
        
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
        self.tabela = ttk.Treeview(self.relatorio_frame, columns=colunas, show="headings")
        
        # Definir cabeçalhos
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=100, anchor="center")
        
        # Ajustar larguras específicas
        self.tabela.column("Data/Hora", width=150)
        self.tabela.column("Produto", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.relatorio_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar na tela
        self.tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    m.id, 
                    m.data_hora, 
                    p.nome AS produto, 
                    m.tipo, 
                    m.quantidade, 
                    m.usuario 
                FROM movimentacoes m
                JOIN produtos p ON m.produto_id = p.id
                ORDER BY m.data_hora DESC
            """)

            movimentacoes = cursor.fetchall()

            for mov in movimentacoes:
                data_formatada = mov['data_hora'].strftime("%d/%m/%Y %H:%M:%S")
                self.tabela.insert(
                    "", "end",
                    values=(
                    mov['id'], data_formatada, mov['produto'], mov['tipo'], mov['quantidade'], mov['usuario']
                ))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar movimentações: {e}")
    
        finally:
            cursor.close()
            conexao.close()

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
            
    def exportar_para_excel(self):
        if not self.tabela.get_children():
            messagebox.showwarning("Aviso", "Nenhum relatório foi gerado ainda!")
            return

        # Abrir a caixa de diálogo para salvar o arquivo
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivo Excel", "*.   xlsx")])

        if not arquivo:
            return

        # Garantir que o nome do arquivo termina em .xlsx
        if not arquivo.endswith(".xlsx"):
            arquivo += ".xlsx"

        colunas = [self.tabela.heading(col)["text"] for col in self.tabela["columns"]]
        dados = [self.tabela.item(item, "values") for item in self.tabela.get_children()]

        try:
            # Criar um novo arquivo Excel
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Relatório"

            # Adicionar cabeçalhos
            for col_index, col_name in enumerate(colunas, start=1):
                cell = sheet.cell(row=1, column=col_index, value=col_name)
                cell.font = Font(bold=True)  # Negrito para os cabeçalhos

            # Adicionar dados na planilha
            for row_index, row_data in enumerate(dados, start=2):
                for col_index, cell_value in enumerate(row_data, start=1):
                    sheet.cell(row=row_index, column=col_index, value=cell_value)

            # Salvar o arquivo Excel corretamente
            workbook.save(arquivo)
            workbook.close()  # 🔹 Fechar corretamente para evitar corrupção do arquivo

            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\nSalvo em: {arquivo}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar para Excel: {e}")


    """   def exportar_para_csv(self):
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
           
           messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")"""