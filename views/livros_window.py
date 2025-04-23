import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models.livro import Livro
from database.conexao import conectar


class AutoCompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._completion_list = []
        self._hits = []
        self._position = 0
        self._hits_index = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def handle_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Shift_L", "Shift_R", "Control_L", "Control_R"):
            return

        value = self.get().lower()
        self._hits = [item for item in self._completion_list if item.lower().startswith(value)]

        if self._hits:
            self['values'] = self._hits
        else:
            self['values'] = self._completion_list

        self.event_generate('<Down>')


def carregar_opcoes(campo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT nome FROM tb_{campo}")
    opcoes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return opcoes


def adicionar_opcao(campo, combobox):
    nova_opcao = simpledialog.askstring("Novo Cadastro", f"Digite o novo {campo}:")
    if nova_opcao:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO tb_{campo} (nome) VALUES (%s)", (nova_opcao,))
        conn.commit()
        conn.close()
        combobox.set_completion_list(carregar_opcoes(campo))
        combobox.set(nova_opcao)


def verificar_registro(campo, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM tb_{campo} WHERE nome = %s", (valor,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def cadastro_livro_window():
    janela = tk.Toplevel()
    janela.title("Cadastro de Livro")

    # Título
    tk.Label(janela, text="Título:").grid(row=0, column=0)
    entry_titulo = tk.Entry(janela)
    entry_titulo.grid(row=0, column=1)

    def criar_campo(label, campo, row):
        tk.Label(janela, text=f"{label}:").grid(row=row, column=0)
        combo = AutoCompleteCombobox(janela)
        combo.set_completion_list(carregar_opcoes(campo))
        combo.grid(row=row, column=1)
        btn = tk.Button(janela, text="(+)", command=lambda: adicionar_opcao(campo, combo))
        btn.grid(row=row, column=2)
        return combo

    combobox_autor = criar_campo("Autor", "autor", 1)
    combobox_categoria = criar_campo("Categoria", "categoria", 2)
    combobox_editora = criar_campo("Editora", "editora", 3)
    combobox_tipo = criar_campo("Tipo", "tipo", 4)
    combobox_cor = criar_campo("Cor", "cor", 5)

    error_label = tk.Label(janela, text="", fg="red")
    error_label.grid(row=6, column=0, columnspan=3)

    def cadastrar_livro():
        titulo = entry_titulo.get()
        autor = combobox_autor.get()
        categoria = combobox_categoria.get()
        editora = combobox_editora.get()
        tipo = combobox_tipo.get()
        cor = combobox_cor.get()

        if not titulo or not autor or not categoria or not editora or not tipo or not cor:
            error_label.config(text="Por favor, preencha todos os campos!")
            return

        for campo, valor in [("autor", autor), ("categoria", categoria), ("editora", editora), ("tipo", tipo), ("cor", cor)]:
            if not verificar_registro(campo, valor):
                error_label.config(text=f"O {campo} '{valor}' não está cadastrado. Cadastre-o primeiro.")
                return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM tb_autor WHERE nome = %s", (autor,))
        id_autor = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM tb_categoria WHERE nome = %s", (categoria,))
        id_categoria = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM tb_editora WHERE nome = %s", (editora,))
        id_editora = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM tb_tipo WHERE nome = %s", (tipo,))
        id_tipo = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM tb_cor WHERE nome = %s", (cor,))
        id_cor = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO tb_livro (titulo, id_autor, id_categoria, id_editora, id_tipo, id_cor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (titulo, id_autor, id_categoria, id_editora, id_tipo, id_cor))

        conn.commit()
        conn.close()

        error_label.config(text="")
        entry_titulo.delete(0, tk.END)
        for cb in [combobox_autor, combobox_categoria, combobox_editora, combobox_tipo, combobox_cor]:
            cb.set("")

        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")

    tk.Button(janela, text="Cadastrar Livro", command=cadastrar_livro).grid(row=7, column=0, columnspan=3)
