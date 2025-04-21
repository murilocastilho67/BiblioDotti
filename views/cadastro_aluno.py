import tkinter as tk
from tkinter import messagebox
from models.aluno import Aluno

def cadastrar_aluno():
    nome = entry_nome.get()
    matricula = entry_matricula.get()

    if not nome or not matricula:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")
        return

    aluno = Aluno(nome, matricula)
    if aluno.salvar():
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar aluno.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)

def cadastro_aluno_window():
    global entry_nome, entry_matricula

    window = tk.Toplevel()
    window.title("Cadastro de Aluno")
    window.geometry("400x300")

    label_nome = tk.Label(window, text="Nome do Aluno:")
    label_nome.pack()
    entry_nome = tk.Entry(window)
    entry_nome.pack(pady=5)

    label_matricula = tk.Label(window, text="Matrícula:")
    label_matricula.pack()
    entry_matricula = tk.Entry(window)
    entry_matricula.pack(pady=5)

    btn_salvar = tk.Button(window, text="Salvar", command=cadastrar_aluno)
    btn_salvar.pack(pady=10)

    btn_limpar = tk.Button(window, text="Limpar", command=limpar_campos)
    btn_limpar.pack(pady=5)

    window.mainloop()
