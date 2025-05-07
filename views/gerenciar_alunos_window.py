import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models.aluno import Aluno  # Certifique-se que o model aceite todos os campos
from editar_aluno_window import editar_aluno_window

def gerenciar_alunos_window():
    janela = tk.Toplevel()
    janela.title("Gerenciar Alunos")
    janela.geometry("900x400")

    colunas = ("ID", "ID Matriz", "Turno", "Série", "Turma", "Matrícula", "Estudante", "Sexo", "Data Nascimento", "Bloqueado", "Data Bloqueio")
    tree = ttk.Treeview(janela, columns=colunas, show='headings')
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    def atualizar_lista():
        tree.delete(*tree.get_children())
        alunos = Aluno.listar()
        for aluno in alunos:
            tree.insert("", tk.END, values=(
                aluno.id, aluno.id_matriz, aluno.turno, aluno.serie, aluno.turma,
                aluno.matricula, aluno.estudante, aluno.sexo, aluno.data_nascimento.strftime("%d/%m/%Y"),
                aluno.bloqueado, aluno.data_bloqueio.strftime("%d/%m/%Y") if aluno.data_bloqueio else ""
            ))

    def editar_aluno():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Por favor, selecione um aluno para editar.")
            return
        valores = tree.item(selected_item)['values']
        aluno = Aluno(*valores[1:], id=valores[0])  # Certifique-se que a ordem bate com o model
        editar_aluno_window(aluno, atualizar_lista)

    def excluir_aluno():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Por favor, selecione um aluno para excluir.")
            return
        valores = tree.item(selected_item)['values']
        aluno = Aluno(*valores[1:], id=valores[0])
        if aluno.excluir():
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Falha ao excluir aluno.")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)
    tk.Button(frame_botoes, text="Editar", command=editar_aluno).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Excluir", command=excluir_aluno).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_lista).pack(side=tk.LEFT, padx=5)

    atualizar_lista()
