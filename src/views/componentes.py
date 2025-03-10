from tkinter import Frame, Label, Entry, Button, StringVar, messagebox

class Componentes:
    def __init__(self, master):
        self.master = master

    def criar_label(self, texto, linha, coluna):
        label = Label(self.master, text=texto)
        label.grid(row=linha, column=coluna, padx=10, pady=10)

    def criar_entry(self, linha, coluna, variavel):
        entry = Entry(self.master, textvariable=variavel)
        entry.grid(row=linha, column=coluna, padx=10, pady=10)

    def criar_botao(self, texto, comando, linha, coluna):
        botao = Button(self.master, text=texto, command=comando)
        botao.grid(row=linha, column=coluna, padx=10, pady=10)

    def mostrar_mensagem(self, mensagem):
        messagebox.showinfo("Informação", mensagem)