import tkinter as tk
from tkinter import messagebox
from models.aluno import Aluno

def editar_aluno_window(aluno, callback):
    janela = tk.Toplevel()
    janela.title("Editar Aluno")

    campos = {}

    labels = [
        ("ID Matriz", aluno.id_matriz),
        ("Turno", aluno.turno),
        ("Série", aluno.serie),
        ("Turma", aluno.turma),
        ("Matrícula", aluno.matricula),
        ("Estudante", aluno.estudante),
        ("Sexo", aluno.sexo),
        ("Data Nascimento", aluno.data_nascimento.strftime("%Y-%m-%d")),
        ("Bloqueado", aluno.bloqueado),
        ("Data Bloqueio", aluno.data_bloqueio.strftime("%Y-%m-%d") if aluno.data_bloqueio else "")
    ]

    for i, (label_text, valor) in enumerate(labels):
        tk.Label(janela, text=label_text).grid(row=i, column=0)
        entry = tk.Entry(janela)
        entry.insert(0, str(valor))
        entry.grid(row=i, column=1)
        campos[label_text] = entry

    def salvar_edicao():
        try:
            aluno.id_matriz = int(campos["ID Matriz"].get())
            aluno.turno = campos["Turno"].get()
            aluno.serie = campos["Série"].get()
            aluno.turma = campos["Turma"].get()
            aluno.matricula = campos["Matrícula"].get()
            aluno.estudante = campos["Estudante"].get()
            aluno.sexo = campos["Sexo"].get()
            aluno.data_nascimento = campos["Data Nascimento"].get()
            aluno.bloqueado = campos["Bloqueado"].get()
            aluno.data_bloqueio = campos["Data Bloqueio"].get()

            if aluno.editar():
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                callback()  # Atualiza a lista
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o aluno.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    tk.Button(janela, text="Salvar", command=salvar_edicao).grid(row=len(labels), column=0, columnspan=2)
