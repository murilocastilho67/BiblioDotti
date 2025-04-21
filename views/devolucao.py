import tkinter as tk
from tkinter import messagebox
from models.devolucao import Devolucao
from models.emprestimo import Emprestimo

def registrar_devolucao():
    emprestimo_id = entry_emprestimo_id.get()

    emprestimo = Emprestimo.buscar_por_id(emprestimo_id)
    if not emprestimo:
        messagebox.showerror("Erro", "Empréstimo não encontrado")
        return

    devolucao = Devolucao(emprestimo)
    if devolucao.registrar():
        messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Falha ao registrar devolução.")

def limpar_campos():
    entry_emprestimo_id.delete(0, tk.END)

def devolucao_window():
    global entry_emprestimo_id

    window = tk.Toplevel()
    window.title("Registrar Devolução")
    window.geometry("400x200")

    label_emprestimo_id = tk.Label(window, text="ID do Empréstimo:")
    label_emprestimo_id.pack()
    entry_emprestimo_id = tk.Entry(window)
    entry_emprestimo_id.pack(pady=5)

    btn_registrar = tk.Button(window, text="Registrar Devolução", command=registrar_devolucao)
    btn_registrar.pack(pady=10)

    window.mainloop()
