import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.conexao import conectar


def gerenciar_livros_window():
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Livros")

    # Tamanho inicial maior e centralização
    largura = 800
    altura = 600
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    janela.minsize(700, 500)
    janela.configure(bg="#f0f0f0")
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # Frame principal
    frame = tk.Frame(janela, bg="#f0f0f0")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame.grid_rowconfigure(1, weight=1)  # Tabela expande verticalmente
    frame.grid_columnconfigure(0, weight=1)  # Tabela expande horizontalmente

    # Frame de filtros
    filtros_frame = ttk.LabelFrame(frame, text="Filtros", padding=5)
    filtros_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    filtros_frame.grid_columnconfigure(0, weight=1)

    campos = ['Título', 'Autor', 'Categoria', 'Editora', 'Tipo', 'Cor']
    entradas_filtros = {}

    # Subframe para filtros
    filtros_subframe = tk.Frame(filtros_frame, bg="#f0f0f0")
    filtros_subframe.grid(row=0, column=0, sticky="ew")
    for i, campo in enumerate(campos):
        tk.Label(filtros_subframe, text=campo + ":", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=i * 2, padx=3,
                                                                                            pady=2, sticky="w")
        entrada = ttk.Entry(filtros_subframe, width=15)
        entrada.grid(row=0, column=i * 2 + 1, padx=3, pady=2, sticky="ew")
        entradas_filtros[campo.lower()] = entrada
        filtros_subframe.grid_columnconfigure(i * 2 + 1, weight=1)  # Filtros expansíveis

    # Frame da tabela
    frame_tabela = ttk.Frame(frame)
    frame_tabela.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    columns = ('ID', 'Título', 'Autor', 'Categoria', 'Editora', 'Tipo', 'Cor', 'Quantidade')
    tree = ttk.Treeview(frame_tabela, columns=columns, show='headings', height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", stretch=True)
    # Larguras iniciais ajustadas
    tree.column('ID', width=50)
    tree.column('Título', width=150)
    tree.column('Autor', width=120)
    tree.column('Categoria', width=100)
    tree.column('Editora', width=100)
    tree.column('Tipo', width=80)
    tree.column('Cor', width=80)
    tree.column('Quantidade', width=80)
    tree.grid(row=0, column=0, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Função para buscar e preencher a tabela
    def atualizar_lista():
        for item in tree.get_children():
            tree.delete(item)

        filtros = {campo: entradas_filtros[campo].get().strip() for campo in entradas_filtros}
        query = """
        SELECT l.id, l.titulo, a.nome, c.nome, e.nome, t.nome, co.nome, COUNT(ex.id)
        FROM tb_livro l
        JOIN tb_autor a ON l.id_autor = a.id
        JOIN tb_categoria c ON l.id_categoria = c.id
        JOIN tb_editora e ON l.id_editora = e.id
        JOIN tb_tipo t ON l.id_tipo = t.id
        JOIN tb_cor co ON l.id_cor = co.id
        LEFT JOIN tb_exemplar ex ON ex.id_livro = l.id
        WHERE (%s = '' OR LOWER(l.titulo) LIKE LOWER(%s))
        AND (%s = '' OR LOWER(a.nome) LIKE LOWER(%s))
        AND (%s = '' OR LOWER(c.nome) LIKE LOWER(%s))
        AND (%s = '' OR LOWER(e.nome) LIKE LOWER(%s))
        AND (%s = '' OR LOWER(t.nome) LIKE LOWER(%s))
        AND (%s = '' OR LOWER(co.nome) LIKE LOWER(%s))
        GROUP BY l.id, a.nome, c.nome, e.nome, t.nome, co.nome
        """

        params = []
        for valor in filtros.values():
            params.append(valor)
        for valor in filtros.values():
            params.append(f'%{valor}%')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, params)
        livros = cursor.fetchall()
        cursor.close()
        conn.close()

        for livro in livros:
            tree.insert('', 'end', values=livro)

        # Ajustar largura das colunas dinamicamente
        for col in columns:
            max_width = tk.font.Font().measure(col)  # Tamanho do cabeçalho
            for item in tree.get_children():
                valor = str(tree.item(item)['values'][columns.index(col)])
                max_width = max(max_width, tk.font.Font().measure(valor) + 10)
            tree.column(col, width=min(max_width, 300))  # Limite máximo de 300px

    # Botões principais
    botoes_frame = tk.Frame(frame, bg="#f0f0f0")
    botoes_frame.grid(row=2, column=0, pady=10, sticky="ew")

    tk.Button(botoes_frame, text="Editar Título", command=lambda: editar_titulo(tree, atualizar_lista),
              bg="#2196F3", fg="white", font=("Arial", 10), width=12).grid(row=0, column=0, padx=5)
    tk.Button(botoes_frame, text="Atualizar Qtd.", command=lambda: atualizar_quantidade(tree, atualizar_lista),
              bg="#4CAF50", fg="white", font=("Arial", 10), width=12).grid(row=0, column=1, padx=5)
    tk.Button(botoes_frame, text="Aplicar Filtros", command=atualizar_lista,
              bg="#FFC107", fg="white", font=("Arial", 10), width=12).grid(row=0, column=2, padx=5)

    atualizar_lista()


def editar_titulo(tree, atualizar_callback):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Por favor, selecione um livro para editar.")
        return

    livro_id = tree.item(selected_item[0])['values'][0]
    novo_titulo = simpledialog.askstring("Editar Título", "Digite o novo título:")
    if novo_titulo:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE tb_livro SET titulo = %s WHERE id = %s", (novo_titulo, livro_id))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Título atualizado com sucesso!")
        atualizar_callback()


def atualizar_quantidade(tree, atualizar_callback):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Seleção", "Por favor, selecione um livro para atualizar a quantidade.")
        return

    livro_id = tree.item(selected_item[0])['values'][0]
    nova_qtd = simpledialog.askinteger("Atualizar Quantidade", "Informe a nova quantidade de exemplares:")
    if nova_qtd is None or nova_qtd < 0:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    # Verificar se há empréstimos ativos (sem registro em tb_devolucao)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM tb_emprestimo e
        JOIN tb_exemplar ex ON e.id_exemplar = ex.id
        LEFT JOIN tb_devolucao d ON e.id = d.id_emprestimo
        WHERE ex.id_livro = %s AND d.id IS NULL
    """, (livro_id,))
    emprestimos_ativos = cursor.fetchone()[0]

    if emprestimos_ativos > 0:
        cursor.close()
        conn.close()
        messagebox.showerror("Erro",
                             "Não é possível atualizar a quantidade porque há empréstimos ativos para este livro.")
        return

    # Se não houver empréstimos ativos, prosseguir com a atualização
    cursor.execute("DELETE FROM tb_exemplar WHERE id_livro = %s", (livro_id,))
    for i in range(nova_qtd):
        codigo_exemplar = f"{livro_id:05d}-{i + 1:03d}"
        cursor.execute(
            "INSERT INTO tb_exemplar (id_livro, codigo_exemplar, disponivel) VALUES (%s, %s, %s)",
            (livro_id, codigo_exemplar, True)
        )
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Quantidade de exemplares atualizada com sucesso!")
    atualizar_callback()