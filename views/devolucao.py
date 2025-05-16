import tkinter as tk
from tkinter import messagebox, ttk
from models.devolucao import Devolucao
from database.conexao import conectar
from datetime import datetime, timedelta


def registrar_devolucao():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Erro", "Selecione um empréstimo.")
        return

    emprestimo_id = tree.item(selected)["values"][0]
    devolucao = Devolucao(emprestimo_id=int(emprestimo_id))
    sucesso, mensagem = devolucao.salvar()
    if sucesso:
        messagebox.showinfo("Sucesso", mensagem)
        atualizar_lista()
    else:
        messagebox.showerror("Erro", mensagem)


def atualizar_lista(*args):
    for row in tree.get_children():
        tree.delete(row)
    busca = entry_busca.get().lower()
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT e.id, a.estudante, l.titulo, e.data_emprestimo, e.data_prevista_devolucao,
           CASE 
               WHEN e.data_prevista_devolucao < %s THEN 
                   (DATEDIFF(%s, e.data_prevista_devolucao) * 2.00)
               ELSE 0.00 
           END AS multa
    FROM tb_emprestimo e
    JOIN tb_aluno a ON e.id_aluno = a.id
    JOIN tb_exemplar ex ON e.id_exemplar = ex.id
    JOIN tb_livro l ON ex.id_livro = l.id
    LEFT JOIN tb_devolucao d ON e.id = d.id_emprestimo
    WHERE d.id IS NULL
    AND (a.estudante LIKE %s OR a.matricula LIKE %s)
    """
    today = datetime.now().date()
    limite_proximo = today + timedelta(days=2)
    cursor.execute(query, (today, today, f"%{busca}%", f"%{busca}%"))
    for row in cursor.fetchall():
        data_prevista = row[4]
        tag = ""
        if data_prevista < today:
            tag = "vencido"
        elif data_prevista <= limite_proximo:
            tag = "proximo"
        tree.insert("", "end", values=row, tags=(tag,))
    cursor.close()
    conn.close()


def devolucao_window():
    window = tk.Toplevel()
    window.title("Registrar Devolução")

    # Tamanho inicial da janela
    largura = 900
    altura = 500
    # Centralizar a janela
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Configurar a janela para ser responsiva
    window.minsize(800, 400)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Frame principal
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Busca de aluno
    label_busca = tk.Label(frame, text="Buscar Aluno (Nome ou Matrícula):")
    label_busca.pack(anchor="w", pady=5)
    global entry_busca
    entry_busca = tk.Entry(frame, width=50)
    entry_busca.pack(fill="x", pady=5)
    entry_busca.bind("<KeyRelease>", atualizar_lista)

    # Tabela
    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Aluno", "Livro", "Data Empréstimo", "Data Prevista", "Multa"),
                        show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Aluno", text="Aluno")
    tree.heading("Livro", text="Livro")
    tree.heading("Data Empréstimo", text="Data Empréstimo")
    tree.heading("Data Prevista", text="Data Prevista")
    tree.heading("Multa", text="Multa (R$)")
    tree.column("ID", width=50)
    tree.column("Aluno", width=150)
    tree.column("Livro", width=200)
    tree.column("Data Empréstimo", width=100)
    tree.column("Data Prevista", width=100)
    tree.column("Multa", width=100)
    tree.pack(fill="both", expand=True, pady=10)

    # Configurar cores para vencidos e próximos
    tree.tag_configure("vencido", background="salmon")
    tree.tag_configure("proximo", background="lightyellow")

    # Botão
    btn_registrar = tk.Button(frame, text="Registrar Devolução", command=registrar_devolucao)
    btn_registrar.pack(pady=10)

    # Carrega a lista inicial
    atualizar_lista()

    window.mainloop()