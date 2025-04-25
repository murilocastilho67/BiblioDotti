import tkinter as tk
from views.livros_window import cadastro_livro_window
from views.cadastro_aluno import cadastro_aluno_window
from views.cadastro_emprestimo import cadastro_emprestimo_window
from views.devolucao import devolucao_window

def main_window(root=None):
    if not root:
        root = tk.Tk()

    root.title("Sistema de Biblioteca")
    root.geometry("400x300")

    tk.Button(root, text="Livros", command=cadastro_livro_window).pack(pady=10)
    tk.Button(root, text="Cadastrar Aluno", command=cadastro_aluno_window).pack(pady=10)
    tk.Button(root, text="Cadastrar Empréstimo", command=cadastro_emprestimo_window).pack(pady=10)
    tk.Button(root, text="Devoluções Pendentes", command=devolucao_window).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
