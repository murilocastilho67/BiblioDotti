import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.livro import Livro
from database.conexao import conectar
from app.utils import carregar_opcoes_combobox
from views.gerenciar_livros_window import gerenciar_livros_window  # Correto, apenas a função

def cadastro_livro_window():
    janela = tk.Toplevel()
    janela.title("Cadastro de Livro")

    manter_dados_var = tk.BooleanVar(value=False)

    tk.Label(janela, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    titulo_entry = ttk.Entry(janela, width=50)
    titulo_entry.grid(row=0, column=1, padx=5, pady=5)

    # Função para criar um Combobox com autocomplete
    def criar_combobox_autocomplete(janela, row, label_text, table_name):
        tk.Label(janela, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        combobox = ttk.Combobox(janela, width=47)
        combobox.grid(row=row, column=1, padx=5, pady=5)
        carregar_opcoes_combobox(combobox, table_name)
        combobox['state'] = 'normal'

        # Filtragem ao digitar
        def on_keyrelease(event):
            texto = combobox.get().lower()
            valores = combobox['values']
            filtrado = [item for item in valores if texto in item.lower()]
            combobox['values'] = filtrado
            combobox.event_generate('<Down>')  # mostra a lista filtrada

        combobox.bind('<KeyRelease>', on_keyrelease)
        return combobox

    autor_combobox = criar_combobox_autocomplete(janela, 1, "Autor:", "tb_autor")
    categoria_combobox = criar_combobox_autocomplete(janela, 2, "Categoria:", "tb_categoria")
    editora_combobox = criar_combobox_autocomplete(janela, 3, "Editora:", "tb_editora")
    tipo_combobox = criar_combobox_autocomplete(janela, 4, "Tipo:", "tb_tipo")
    cor_combobox = criar_combobox_autocomplete(janela, 5, "Cor:", "tb_cor")

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
        confirmacao = messagebox.askyesno("Confirmar exclusão", f"Tem certeza de que deseja excluir {titulo.lower()} '{valor}'?")
        if confirmacao:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE nome = %s", (valor,))
            conn.commit()
            cursor.close()
            conn.close()
            carregar_opcoes_combobox(combobox, tabela)
            messagebox.showinfo("Sucesso", f"{titulo} excluída com sucesso!")

    ttk.Button(janela, text="Criar", command=lambda: adicionar_valor(autor_combobox, "tb_autor", "Autor")).grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(janela, text="Editar", command=lambda: editar_valor(autor_combobox, "tb_autor", "Autor")).grid(row=1, column=3, padx=5, pady=5)
    ttk.Button(janela, text="Excluir", command=lambda: excluir_valor(autor_combobox, "tb_autor", "Autor")).grid(row=1, column=4, padx=5, pady=5)

    ttk.Button(janela, text="Criar", command=lambda: adicionar_valor(categoria_combobox, "tb_categoria", "Categoria")).grid(row=2, column=2, padx=5, pady=5)
    ttk.Button(janela, text="Editar", command=lambda: editar_valor(categoria_combobox, "tb_categoria", "Categoria")).grid(row=2, column=3, padx=5, pady=5)
    ttk.Button(janela, text="Excluir", command=lambda: excluir_valor(categoria_combobox, "tb_categoria", "Categoria")).grid(row=2, column=4, padx=5, pady=5)

    ttk.Button(janela, text="Criar", command=lambda: adicionar_valor(editora_combobox, "tb_editora", "Editora")).grid(row=3, column=2, padx=5, pady=5)
    ttk.Button(janela, text="Editar", command=lambda: editar_valor(editora_combobox, "tb_editora", "Editora")).grid(row=3, column=3, padx=5, pady=5)
    ttk.Button(janela, text="Excluir", command=lambda: excluir_valor(editora_combobox, "tb_editora", "Editora")).grid(row=3, column=4, padx=5, pady=5)

    ttk.Button(janela, text="Criar", command=lambda: adicionar_valor(tipo_combobox, "tb_tipo", "Tipo")).grid(row=4, column=2, padx=5, pady=5)
    ttk.Button(janela, text="Editar", command=lambda: editar_valor(tipo_combobox, "tb_tipo", "Tipo")).grid(row=4, column=3, padx=5, pady=5)
    ttk.Button(janela, text="Excluir", command=lambda: excluir_valor(tipo_combobox, "tb_tipo", "Tipo")).grid(row=4, column=4, padx=5, pady=5)

    ttk.Button(janela, text="Criar", command=lambda: adicionar_valor(cor_combobox, "tb_cor", "Cor")).grid(row=5, column=2, padx=5, pady=5)
    ttk.Button(janela, text="Editar", command=lambda: editar_valor(cor_combobox, "tb_cor", "Cor")).grid(row=5, column=3, padx=5, pady=5)
    ttk.Button(janela, text="Excluir", command=lambda: excluir_valor(cor_combobox, "tb_cor", "Cor")).grid(row=5, column=4, padx=5, pady=5)

    tk.Label(janela, text="Qtd. Exemplares:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
    qtd_entry = ttk.Entry(janela, width=10)
    qtd_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    manter_dados_checkbox = ttk.Checkbutton(janela, text="Manter dados após cadastro", variable=manter_dados_var)
    manter_dados_checkbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    # Botão para Gerenciar Livros (fora da função cadastrar_livro)
    def abrir_gerenciamento():
        gerenciar_livros_window()  # Certifique-se de que essa função está corretamente definida em views.py

    gerenciar_btn = ttk.Button(janela, text="Gerenciar Livros", command=abrir_gerenciamento)
    gerenciar_btn.grid(row=9, column=0, columnspan=2, pady=10)

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
            codigo_exemplar = f"{livro_id:05d}-{i+1:03d}"
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

    cadastrar_btn = ttk.Button(janela, text="Cadastrar", command=cadastrar_livro)
    cadastrar_btn.grid(row=8, column=0, columnspan=2, pady=10)
