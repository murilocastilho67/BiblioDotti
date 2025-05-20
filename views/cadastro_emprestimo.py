import tkinter as tk
from tkinter import messagebox, ttk
from models.emprestimo import Emprestimo
from models.exemplar import Exemplar
from database.conexao import conectar


def cadastrar_emprestimo():
    aluno_id = combo_aluno.get().split(" - ")[0] if combo_aluno.get() else None
    exemplar_id = combo_exemplar.get().split(" - ")[0] if combo_exemplar.get() else None

    if not aluno_id or not exemplar_id:
        messagebox.showerror("Erro", "Selecione um aluno e um exemplar.")
        return

    emprestimo = Emprestimo(id_aluno=int(aluno_id), id_exemplar=int(exemplar_id))
    sucesso, mensagem = emprestimo.salvar()
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        limpar_campos()
        atualizar_exemplares()
    else:
        messagebox.showerror("Erro", mensagem)


def limpar_campos():
    entry_busca_aluno.delete(0, tk.END)
    entry_busca_livro.delete(0, tk.END)
    combo_aluno.set("")
    combo_livro.set("")
    combo_exemplar.set("")
    combo_exemplar["values"] = []


def atualizar_exemplares(*args):
    livro_id = combo_livro.get().split(" - ")[0] if combo_livro.get() else None
    combo_exemplar["values"] = []
    if livro_id:
        exemplares = Exemplar.buscar_disponiveis_por_livro(int(livro_id))
        combo_exemplar["values"] = [f"{e.id} - {e.codigo_exemplar}" for e in exemplares]


def filtrar_alunos(*args):
    busca = entry_busca_aluno.get().lower()
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT id, estudante, matricula
    FROM tb_aluno
    WHERE estudante LIKE %s OR matricula LIKE %s
    """
    cursor.execute(query, (f"%{busca}%", f"%{busca}%"))
    alunos = cursor.fetchall()
    cursor.close()
    conn.close()
    combo_aluno["values"] = [f"{a[0]} - {a[1]} (Matrícula: {a[2]})" for a in alunos]


def filtrar_livros(*args):
    busca = entry_busca_livro.get().lower()
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT tb_livro.id, tb_livro.titulo
    FROM tb_livro
    LEFT JOIN tb_autor ON tb_livro.id_autor = tb_autor.id
    WHERE tb_livro.titulo LIKE %s OR tb_autor.nome LIKE %s
    """
    cursor.execute(query, (f"%{busca}%", f"%{busca}%"))
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    combo_livro["values"] = [f"{l[0]} - {l[1]}" for l in livros]


def cadastro_emprestimo_window():
    window = tk.Toplevel()
    window.title("Cadastro de Empréstimo")

    # Tamanho inicial da janela
    largura = 600
    altura = 450
    # Centralizar a janela
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Configurar a janela para ser responsiva
    window.minsize(500, 400)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Frame principal
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Busca de aluno
    label_busca_aluno = tk.Label(frame, text="Buscar Aluno (Nome ou Matrícula):")
    label_busca_aluno.pack(anchor="w", pady=5)
    global entry_busca_aluno
    entry_busca_aluno = tk.Entry(frame, width=50)
    entry_busca_aluno.pack(fill="x", pady=5)
    entry_busca_aluno.bind("<KeyRelease>", filtrar_alunos)

    # Aluno
    label_aluno = tk.Label(frame, text="Aluno:")
    label_aluno.pack(anchor="w", pady=5)
    global combo_aluno
    combo_aluno = ttk.Combobox(frame, width=50)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, estudante, matricula FROM tb_aluno")
    alunos = cursor.fetchall()
    combo_aluno["values"] = [f"{a[0]} - {a[1]} (Matrícula: {a[2]})" for a in alunos]
    cursor.close()
    conn.close()
    combo_aluno.pack(fill="x", pady=5)

    # Busca de livro
    label_busca_livro = tk.Label(frame, text="Buscar Livro (Título ou Autor):")
    label_busca_livro.pack(anchor="w", pady=5)
    global entry_busca_livro
    entry_busca_livro = tk.Entry(frame, width=50)
    entry_busca_livro.pack(fill="x", pady=5)
    entry_busca_livro.bind("<KeyRelease>", filtrar_livros)

    # Livro
    label_livro = tk.Label(frame, text="Livro:")
    label_livro.pack(anchor="w", pady=5)
    global combo_livro
    combo_livro = ttk.Combobox(frame, width=50)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM tb_livro")
    livros = cursor.fetchall()
    combo_livro["values"] = [f"{l[0]} - {l[1]}" for l in livros]
    cursor.close()
    conn.close()
    combo_livro.pack(fill="x", pady=5)
    combo_livro.bind("<<ComboboxSelected>>", atualizar_exemplares)

    # Exemplar
    label_exemplar = tk.Label(frame, text="Exemplar:")
    label_exemplar.pack(anchor="w", pady=5)
    global combo_exemplar
    combo_exemplar = ttk.Combobox(frame, width=50)
    combo_exemplar.pack(fill="x", pady=5)

    # Botões
    btn_salvar = tk.Button(frame, text="Cadastrar Empréstimo", command=cadastrar_emprestimo)
    btn_salvar.pack(pady=20)

    window.mainloop()