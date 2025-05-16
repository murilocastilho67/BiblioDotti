import tkinter as tk
from views.livros_window import cadastro_livro_window
from views.cadastro_aluno import cadastro_aluno_window
from views.cadastro_emprestimo import cadastro_emprestimo_window
from views.devolucao import devolucao_window

def main_window(root):
    # Configura o título da janela
    root.title("Sistema de Biblioteca")

    # Frame principal para centralizar e organizar os botões
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Função para criar botões estilizados
    def criar_botao(texto, comando, cor):
        return tk.Button(
            frame,
            text=texto,
            command=comando,
            bg=cor,
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        )

    # Cria e posiciona os botões
    criar_botao("Livros", cadastro_livro_window, "#4CAF50").pack(pady=10)
    criar_botao("Alunos", cadastro_aluno_window, "#2196F3").pack(pady=10)
    criar_botao("Empréstimos", cadastro_emprestimo_window, "#FFC107").pack(pady=10)
    criar_botao("Devoluções", devolucao_window, "#F44336").pack(pady=10)