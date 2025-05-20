import tkinter as tk
from tkinter import messagebox, ttk
from models.devolucao import Devolucao
from database.conexao import conectar
from datetime import datetime, timedelta

# Variáveis globais para rastrear ordenação
sort_column = None
sort_reverse = False


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


def atualizar_lista(*args, sort_col=None, reverse=None):
    global sort_column, sort_reverse
    if sort_col is not None:
        sort_column = sort_col
        sort_reverse = reverse if reverse is not None else not sort_reverse

    # Atualizar indicadores visuais nos cabeçalhos
    for col in ("ID", "Aluno", "Livro", "Data Empréstimo", "Data Prevista", "Multa"):
        tree.heading(col, text=col)
    if sort_column:
        col_map = {
            "e.id": "ID",
            "a.estudante": "Aluno",
            "l.titulo": "Livro",
            "e.data_emprestimo": "Data Empréstimo",
            "e.data_prevista_devolucao": "Data Prevista",
            "multa": "Multa"
        }
        for db_col, display_col in col_map.items():
            if sort_column == db_col:
                arrow = " ↓" if sort_reverse else " ↑"
                tree.heading(display_col, text=display_col + arrow)

    for row in tree.get_children():
        tree.delete(row)
    busca = entry_busca.get().lower()
    status = combo_status.get()
    today = datetime.now().date()
    limite_proximo = today + timedelta(days=2)
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
    params = [today, today, f"%{busca}%", f"%{busca}%"]
    if status == "Vencidos":
        query += " AND e.data_prevista_devolucao < %s"
        params.append(today)
    elif status == "Próximos do Vencimento":
        query += " AND e.data_prevista_devolucao <= %s AND e.data_prevista_devolucao >= %s"
        params.extend([limite_proximo, today])

    if sort_column:
        query += f" ORDER BY {sort_column} {'DESC' if sort_reverse else 'ASC'}"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    for row in rows:
        data_prevista = row[4]
        tag = ""
        if data_prevista < today:
            tag = "vencido"
        elif data_prevista <= limite_proximo:
            tag = "proximo"
        tree.insert("", "end", values=row, tags=(tag,))
    cursor.close()
    conn.close()


def sort_treeview(col):
    # Mapear colunas do Treeview para colunas do banco
    col_map = {
        "ID": "e.id",
        "Aluno": "a.estudante",
        "Livro": "l.titulo",
        "Data Empréstimo": "e.data_emprestimo",
        "Data Prevista": "e.data_prevista_devolucao",
        "Multa": "multa"
    }
    if col in col_map:
        atualizar_lista(sort_col=col_map[col])


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
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Busca de aluno
    label_busca = tk.Label(frame, text="Buscar Aluno (Nome ou Matrícula):")
    label_busca.pack(anchor="w", pady=5)
    global entry_busca
    entry_busca = tk.Entry(frame, width=50)
    entry_busca.pack(fill="x", pady=5)
    entry_busca.bind("<KeyRelease>", atualizar_lista)

    # Filtro por status
    label_status = tk.Label(frame, text="Filtrar por Status:")
    label_status.pack(anchor="w", pady=5)
    global combo_status
    combo_status = ttk.Combobox(frame, values=["Todos", "Vencidos", "Próximos do Vencimento"], state="readonly")
    combo_status.set("Todos")
    combo_status.pack(fill="x", pady=5)
    combo_status.bind("<<ComboboxSelected>>", atualizar_lista)

    # Tabela
    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Aluno", "Livro", "Data Empréstimo", "Data Prevista", "Multa"),
                        show="headings")
    tree.heading("ID", text="ID", command=lambda: sort_treeview("ID"))
    tree.heading("Aluno", text="Aluno", command=lambda: sort_treeview("Aluno"))
    tree.heading("Livro", text="Livro", command=lambda: sort_treeview("Livro"))
    tree.heading("Data Empréstimo", text="Data Empréstimo", command=lambda: sort_treeview("Data Empréstimo"))
    tree.heading("Data Prevista", text="Data Prevista", command=lambda: sort_treeview("Data Prevista"))
    tree.heading("Multa", text="Multa (R$)", command=lambda: sort_treeview("Multa"))
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