import tkinter as tk
from tkinter import messagebox
from models.livro import Livro

def cadastrar_livro():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    categoria = entry_categoria.get()
    editora = entry_editora.get()
    tipo = entry_tipo.get()
    cor = entry_cor.get()

    # Validar se todos os campos foram preenchidos
    if not titulo or not autor or not categoria or not editora or not tipo or not cor:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios")
        return

    # Criar objeto livro
    livro = Livro(titulo, autor, categoria, editora, tipo, cor)

    # Salvar no banco de dados
    if livro.salvar():
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar livro.")

def limpar_campos():
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_editora.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_cor.delete(0, tk.END)

def cadastro_livro_window():
    global entry_titulo, entry_autor, entry_categoria, entry_editora, entry_tipo, entry_cor

    window = tk.Toplevel()
    window.title("Cadastro de Livro")
    window.geometry("400x400")

    label_titulo = tk.Label(window, text="Título:")
    label_titulo.pack()
    entry_titulo = tk.Entry(window)
    entry_titulo.pack(pady=5)

    label_autor = tk.Label(window, text="Autor:")
    label_autor.pack()
    entry_autor = tk.Entry(window)
    entry_autor.pack(pady=5)

    label_categoria = tk.Label(window, text="Categoria:")
    label_categoria.pack()
    entry_categoria = tk.Entry(window)
    entry_categoria.pack(pady=5)

    label_editora = tk.Label(window, text="Editora:")
    label_editora.pack()
    entry_editora = tk.Entry(window)
    entry_editora.pack(pady=5)

    label_tipo = tk.Label(window, text="Tipo:")
    label_tipo.pack()
    entry_tipo = tk.Entry(window)
    entry_tipo.pack(pady=5)

    label_cor = tk.Label(window, text="Cor:")
    label_cor.pack()
    entry_cor = tk.Entry(window)
    entry_cor.pack(pady=5)

    btn_salvar = tk.Button(window, text="Salvar", command=cadastrar_livro)
    btn_salvar.pack(pady=10)

    btn_limpar = tk.Button(window, text="Limpar", command=limpar_campos)
    btn_limpar.pack(pady=5)

    window.mainloop()
