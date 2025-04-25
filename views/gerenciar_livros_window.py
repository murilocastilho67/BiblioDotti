import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.conexao import conectar


def gerenciar_livros_window():
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Livros")

    # Frame de filtros
    filtros_frame = ttk.LabelFrame(janela, text="Filtros")
    filtros_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    campos = ['Título', 'Autor', 'Categoria', 'Editora', 'Tipo', 'Cor']
    entradas_filtros = {}

    for i, campo in enumerate(campos):
        ttk.Label(filtros_frame, text=campo + ":").grid(row=0, column=i * 2, padx=2, pady=2, sticky="w")
        entrada = ttk.Entry(filtros_frame, width=15)
        entrada.grid(row=0, column=i * 2 + 1, padx=2, pady=2)
        entradas_filtros[campo.lower()] = entrada

    # Frame da tabela
    frame_tabela = ttk.Frame(janela)
    frame_tabela.grid(row=1, column=0, padx=10, pady=5)

    columns = ('ID', 'Título', 'Autor', 'Categoria', 'Editora', 'Tipo', 'Cor', 'Quantidade')
    tree = ttk.Treeview(frame_tabela, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)

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

    # Botões principais
    botoes_frame = ttk.Frame(janela)
    botoes_frame.grid(row=2, column=0, pady=10)

    ttk.Button(botoes_frame, text="Editar Título", command=lambda: editar_titulo(tree, atualizar_lista)).grid(row=0, column=0, padx=5)
    ttk.Button(botoes_frame, text="Atualizar Quantidade", command=lambda: atualizar_quantidade(tree, atualizar_lista)).grid(row=0, column=1, padx=5)
    ttk.Button(botoes_frame, text="Aplicar Filtros", command=atualizar_lista).grid(row=0, column=2, padx=5)

    atualizar_lista()


# Funções auxiliares
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

    if nova_qtd is not None and nova_qtd >= 0:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_exemplar WHERE id_livro = %s", (livro_id,))
        for i in range(nova_qtd):
            codigo_exemplar = f"{livro_id:05d}-{i + 1:03d}"
            cursor.execute("INSERT INTO tb_exemplar (id_livro, codigo_exemplar) VALUES (%s, %s)",
                           (livro_id, codigo_exemplar))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Quantidade de exemplares atualizada com sucesso!")
        atualizar_callback()
    else:
        messagebox.showerror("Erro", "Quantidade inválida!")
