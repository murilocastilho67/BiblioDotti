import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.livro import Livro
from database.conexao import conectar
from app.utils import carregar_opcoes_combobox
from views.gerenciar_livros_window import gerenciar_livros_window


def cadastro_livro_window():
    janela = tk.Toplevel()
    janela.title("Cadastro de Livro")

    # Tamanho inicial e centralização
    largura = 600
    altura = 400
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    janela.minsize(550, 350)
    janela.configure(bg="#f0f0f0")

    # Frame principal para conter todos os widgets
    frame = tk.Frame(janela, bg="#f0f0f0")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    manter_dados_var = tk.BooleanVar(value=False)

    # Título
    tk.Label(frame, text="Título:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    titulo_entry = ttk.Entry(frame, width=40)
    titulo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Função para criar um Combobox com autocomplete
    def criar_combobox_autocomplete(frame, row, label_text, table_name):
        tk.Label(frame, text=label_text, bg="#f0f0f0", font=("Arial", 10)).grid(row=row, column=0, padx=5, pady=5,
                                                                                sticky="w")
        combobox = ttk.Combobox(frame, width=37)
        combobox.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        carregar_opcoes_combobox(combobox, table_name)
        combobox['state'] = 'normal'

        def on_keyrelease(event):
            texto = combobox.get().lower()
            valores = combobox['values']
            filtrado = [item for item in valores if texto in item.lower()]
            combobox['values'] = filtrado
            combobox.event_generate('<Down>')

        combobox.bind('<KeyRelease>', on_keyrelease)
        return combobox

    # Comboboxes
    autor_combobox = criar_combobox_autocomplete(frame, 1, "Autor:", "tb_autor")
    categoria_combobox = criar_combobox_autocomplete(frame, 2, "Categoria:", "tb_categoria")
    editora_combobox = criar_combobox_autocomplete(frame, 3, "Editora:", "tb_editora")
    tipo_combobox = criar_combobox_autocomplete(frame, 4, "Tipo:", "tb_tipo")
    cor_combobox = criar_combobox_autocomplete(frame, 5, "Cor:", "tb_cor")

    # Funções para gerenciar valores dos comboboxes
    def adicionar_valor(combobox, tabela, titulo):
        novo_valor = simpledialog.askstring(f"Nova(o) {titulo}", f"Digite o nome da(o) {titulo.lower()}:")
        if novo_valor:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {tabela} (nome) VALUES (%s)", (novo_valor,))
            conn.commit()
            cursor.close()
            conn.close()
            carregar_opcoes_combobox(combobox, tabela)
            messagebox.showinfo("Sucesso", f"{titulo} cadastrada com sucesso!")

    def editar_valor(combobox, tabela, titulo):
        valor_atual = combobox.get()
        if not valor_atual:
            messagebox.showerror("Erro", f"Selecione um(a) {titulo} para editar.")
            return
        novo_valor = simpledialog.askstring(f"Editar {titulo}", f"Digite o novo nome para {titulo.lower()}:")
        if novo_valor:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {tabela} SET nome = %s WHERE nome = %s", (novo_valor, valor_atual))
            conn.commit()
            cursor.close()
            conn.close()
            carregar_opcoes_combobox(combobox, tabela)
            messagebox.showinfo("Sucesso", f"{titulo} editada com sucesso!")

    def excluir_valor(combobox, tabela, titulo):
        valor = combobox.get()
        if not valor:
            messagebox.showerror("Erro", f"Selecione um(a) {titulo} para excluir.")
            return
        confirmacao = messagebox.askyesno("Confirmar exclusão",
                                          f"Tem certeza de que deseja excluir {titulo.lower()} '{valor}'?")
        if confirmacao:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE nome = %s", (valor,))
            conn.commit()
            cursor.close()
            conn.close()
            carregar_opcoes_combobox(combobox, tabela)
            messagebox.showinfo("Sucesso", f"{titulo} excluída com sucesso!")

    # Botões para cada combobox (Criar, Editar, Excluir)
    for row, combobox, tabela, titulo in [
        (1, autor_combobox, "tb_autor", "Autor"),
        (2, categoria_combobox, "tb_categoria", "Categoria"),
        (3, editora_combobox, "tb_editora", "Editora"),
        (4, tipo_combobox, "tb_tipo", "Tipo"),
        (5, cor_combobox, "tb_cor", "Cor")
    ]:
        tk.Button(frame, text="Criar", command=lambda c=combobox, t=tabela, ti=titulo: adicionar_valor(c, t, ti),
                  bg="#4CAF50", fg="white", font=("Arial", 8), width=8).grid(row=row, column=2, padx=2, pady=5)
        tk.Button(frame, text="Editar", command=lambda c=combobox, t=tabela, ti=titulo: editar_valor(c, t, ti),
                  bg="#2196F3", fg="white", font=("Arial", 8), width=8).grid(row=row, column=3, padx=2, pady=5)
        tk.Button(frame, text="Excluir", command=lambda c=combobox, t=tabela, ti=titulo: excluir_valor(c, t, ti),
                  bg="#F44336", fg="white", font=("Arial", 8), width=8).grid(row=row, column=4, padx=2, pady=5)

    # Quantidade de exemplares
    tk.Label(frame, text="Qtd. Exemplares:", bg="#f0f0f0", font=("Arial", 10)).grid(row=6, column=0, padx=5, pady=5,
                                                                                    sticky="w")
    qtd_entry = ttk.Entry(frame, width=10)
    qtd_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    # Checkbox
    manter_dados_checkbox = ttk.Checkbutton(frame, text="Manter dados após cadastro", variable=manter_dados_var)
    manter_dados_checkbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    # Função de cadastro de livro
    def cadastrar_livro():
        titulo = titulo_entry.get()
        autor = autor_combobox.get()
        categoria = categoria_combobox.get()
        editora = editora_combobox.get()
        tipo = tipo_combobox.get()
        cor = cor_combobox.get()
        qtd_exemplares = qtd_entry.get()

        if not titulo or not autor or not categoria or not editora or not tipo or not cor or not qtd_exemplares:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not qtd_exemplares.isdigit() or int(qtd_exemplares) <= 0:
            messagebox.showerror("Erro", "Informe uma quantidade válida de exemplares.")
            return

        qtd_exemplares = int(qtd_exemplares)

        def get_id(tabela, nome):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT id FROM {tabela} WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado[0] if resultado else None

        autor_id = get_id("tb_autor", autor)
        categoria_id = get_id("tb_categoria", categoria)
        editora_id = get_id("tb_editora", editora)
        tipo_id = get_id("tb_tipo", tipo)
        cor_id = get_id("tb_cor", cor)

        if None in [autor_id, categoria_id, editora_id, tipo_id, cor_id]:
            messagebox.showerror("Erro", "Todos os itens devem estar previamente cadastrados.")
            return

        livro = Livro(titulo, autor_id, categoria_id, editora_id, tipo_id, cor_id)
        livro_id = livro.salvar()

        conn = conectar()
        cursor = conn.cursor()
        for i in range(qtd_exemplares):
            codigo_exemplar = f"{livro_id:05d}-{i + 1:03d}"
            cursor.execute(
                "INSERT INTO tb_exemplar (id_livro, codigo_exemplar) VALUES (%s, %s)",
                (livro_id, codigo_exemplar)
            )
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Livro e exemplares cadastrados com sucesso!")

        if not manter_dados_var.get():
            titulo_entry.delete(0, tk.END)
            qtd_entry.delete(0, tk.END)
            autor_combobox.set('')
            categoria_combobox.set('')
            editora_combobox.set('')
            tipo_combobox.set('')
            cor_combobox.set('')

    # Botões principais
    tk.Button(frame, text="Cadastrar", command=cadastrar_livro,
              bg="#4CAF50", fg="white", font=("Arial", 10), width=12).grid(row=8, column=0, columnspan=2, pady=10)
    tk.Button(frame, text="Gerenciar Livros", command=gerenciar_livros_window,
              bg="#2196F3", fg="white", font=("Arial", 10), width=15).grid(row=9, column=0, columnspan=2, pady=10)

    # Configurar peso das colunas para responsividade
    frame.grid_columnconfigure(1, weight=1)

    janela.mainloop()