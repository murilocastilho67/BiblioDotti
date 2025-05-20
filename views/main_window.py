import tkinter as tk
from PIL import Image, ImageTk
from views.livros_window import cadastro_livro_window
from views.cadastro_aluno import cadastro_aluno_window
from views.cadastro_emprestimo import cadastro_emprestimo_window
from views.devolucao import devolucao_window
from database.conexao import conectar

def obter_contagens():
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Contagem de livros
        cursor.execute("SELECT COUNT(*) FROM tb_livro")
        total_livros = cursor.fetchone()[0]

        # Contagem de pessoas (alunos)
        cursor.execute("SELECT COUNT(*) FROM tb_aluno")
        total_pessoas = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return total_livros, total_pessoas
    except Exception as e:
        print(f"Erro ao obter contagens: {e}")
        return 0, 0

def main_window(root):
    # Configura o título da janela
    root.title("Gerenciador de Biblioteca DOTTI")

    # Define o tamanho da janela
    largura = 800
    altura = 600
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    root.configure(bg="#ffffff")

    # Frame para o cabeçalho com fundo listrado
    header_frame = tk.Frame(root, bg="#d4e4d1", height=100)
    header_frame.pack(fill="x")

    # Título no cabeçalho
    title_label = tk.Label(
        header_frame,
        text="Gerenciador de Biblioteca DOTTI",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#d4e4d1",
        padx=20,
        pady=20
    )
    title_label.pack(side="left")

    # Frame principal para os botões
    button_frame = tk.Frame(root, bg="#ffffff")
    button_frame.pack(expand=False, pady=20)

    # Função para criar botões estilizados
    def criar_botao(texto, comando):
        return tk.Button(
            button_frame,
            text=texto,
            command=comando,
            bg="#e0e0e0",
            fg="black",
            font=("Arial", 12),
            width=15,
            height=2,
            relief="flat"
        )

    # Cria e posiciona os botões horizontalmente
    botao_livros = criar_botao("Livros", cadastro_livro_window)
    botao_livros.pack(side="left", padx=10)

    botao_alunos = criar_botao("Alunos", cadastro_aluno_window)
    botao_alunos.pack(side="left", padx=10)

    botao_emprestimos = criar_botao("Empréstimos", cadastro_emprestimo_window)
    botao_emprestimos.pack(side="left", padx=10)

    botao_devolucoes = criar_botao("Devoluções", devolucao_window)
    botao_devolucoes.pack(side="left", padx=10)

    # Frame para o card de contagem
    card_frame = tk.Frame(root, bg="#f5f5f5", bd=2, relief="solid")
    card_frame.pack(expand=True, fill="x", padx=50, pady=20)

    # Obter contagens do banco
    total_livros, total_pessoas = obter_contagens()

    # Frame interno para organizar as contagens (horizontal)
    inner_card_frame = tk.Frame(card_frame, bg="#f5f5f5")
    inner_card_frame.pack(pady=20)

    # Contagem de Livros
    livros_frame = tk.Frame(inner_card_frame, bg="#f5f5f5")
    livros_frame.pack(side="left", padx=50)

    tk.Label(
        livros_frame,
        text="Livros",
        font=("Arial", 14, "bold"),
        bg="#f5f5f5",
        fg="#333333"
    ).pack()
    tk.Label(
        livros_frame,
        text=str(total_livros),
        font=("Arial", 24, "bold"),
        bg="#f5f5f5",
        fg="#4CAF50"
    ).pack()

    # Contagem de Pessoas
    pessoas_frame = tk.Frame(inner_card_frame, bg="#f5f5f5")
    pessoas_frame.pack(side="left", padx=50)

    tk.Label(
        pessoas_frame,
        text="Pessoas",
        font=("Arial", 14, "bold"),
        bg="#f5f5f5",
        fg="#333333"
    ).pack()
    tk.Label(
        pessoas_frame,
        text=str(total_pessoas),
        font=("Arial", 24, "bold"),
        bg="#f5f5f5",
        fg="#2196F3"
    ).pack()

    # Frame para o logotipo (centralizado)
    logo_frame = tk.Frame(root, bg="#ffffff")
    logo_frame.pack(expand=True, fill="x", pady=20)

    # Carregar e exibir a logo centralizada
    try:
        logo_image = Image.open("dotti_logo.png")
        logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  # Ajustar tamanho
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(logo_frame, image=logo_photo, bg="#ffffff")
        logo_label.image = logo_photo  # Para evitar garbage collection
        logo_label.pack(anchor="center")
    except Exception as e:
        print(f"Erro ao carregar a logo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    main_window(root)
    root.mainloop()