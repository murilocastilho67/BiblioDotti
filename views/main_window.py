import tkinter as tk
from views.livros_window import cadastro_livro_window
from views.cadastro_aluno import cadastro_aluno_window
from views.cadastro_emprestimo import cadastro_emprestimo_window
from views.devolucao import devolucao_window

def main_window(root):
    root.title("Sistema de Biblioteca")
    root.geometry("400x300")

    # Botão para cadastrar livro
    btn_cadastro_livro = tk.Button(root, text="Livros", command=cadastro_livro_window)
    btn_cadastro_livro.pack(pady=10)

    # Botão para cadastrar aluno
    btn_cadastro_aluno = tk.Button(root, text="Cadastrar Aluno", command=cadastro_aluno_window)
    btn_cadastro_aluno.pack(pady=10)

    # Botão para cadastrar empréstimo
    btn_cadastro_emprestimo = tk.Button(root, text="Cadastrar Empréstimo", command=cadastro_emprestimo_window)
    btn_cadastro_emprestimo.pack(pady=10)

    # Botão para devoluções pendentes
    btn_devolucao = tk.Button(root, text="Devoluções Pendentes", command=devolucao_window)
    btn_devolucao.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
