import tkinter as tk
from tkinter import messagebox
from models.emprestimo import Emprestimo
from models.aluno import Aluno
from models.livro import Livro

def cadastrar_emprestimo():
    aluno_id = entry_aluno_id.get()
    livro_id = entry_livro_id.get()

    aluno = Aluno.buscar_por_id(aluno_id)
    livro = Livro.buscar_por_id(livro_id)

    if not aluno or not livro:
        messagebox.showerror("Erro", "Aluno ou Livro não encontrado")
        return

    emprestimo = Emprestimo(aluno, livro)
    if emprestimo.salvar():
        messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Falha ao realizar empréstimo.")

def limpar_campos():
    entry_aluno_id.delete(0, tk.END)
    entry_livro_id.delete(0, tk.END)

def cadastro_emprestimo_window():
    global entry_aluno_id, entry_livro_id

    window = tk.Toplevel()
    window.title("Cadastro de Empréstimo")
    window.geometry("400x300")

    label_aluno_id = tk.Label(window, text="ID do Aluno:")
    label_aluno_id.pack()
    entry_aluno_id = tk.Entry(window)
    entry_aluno_id.pack(pady=5)

    label_livro_id = tk.Label(window, text="ID do Livro:")
    label_livro_id.pack()
    entry_livro_id = tk.Entry(window)
    entry_livro_id.pack(pady=5)

    btn_salvar = tk.Button(window, text="Salvar", command=cadastrar_emprestimo)
    btn_salvar.pack(pady=10)

    window.mainloop()
