import tkinter as tk
from views.livros_window import cadastro_livro_window
from views.cadastro_aluno import cadastro_aluno_window
from views.cadastro_emprestimo import cadastro_emprestimo_window
from views.devolucao import devolucao_window


def main_window(root):
    # A janela principal já foi criada fora, só personalizamos aqui
    root.title("Sistema de Biblioteca")

    # Você pode até deixar o tamanho fixo se quiser, ou comentar essa linha
    # root.geometry("400x300")

    # Cria os botões
    tk.Button(root, text="Livros", command=cadastro_livro_window).pack(pady=10)
    tk.Button(root, text="Alunos", command=cadastro_aluno_window).pack(pady=10)
    tk.Button(root, text="Cadastrar Empréstimo", command=cadastro_emprestimo_window).pack(pady=10)
    tk.Button(root, text="Devoluções Pendentes", command=devolucao_window).pack(pady=10)

# Não precisa de if __name__ == "__main__" aqui
# Quem chama a main_window() é o iniciar_app()
