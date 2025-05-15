import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import re
from models.aluno import Aluno

def editar_aluno_window(aluno, callback):
    janela = tk.Toplevel()
    janela.title("Editar Aluno")
    janela.geometry("400x350")  # Ajustado para layout mais compacto
    janela.resizable(False, False)

    campos = {}

    # Mapear valores iniciais
    turno_display = {'M': 'Matutino', 'V': 'Vespertino', 'N': 'Noturno'}.get(aluno.turno, aluno.turno)
    sexo_display = aluno.sexo

    # Campos de texto
    labels = [
        ("ID Matriz (4 dígitos)", str(aluno.id_matriz), tk.Entry),
        ("Turno (M/V/N)", aluno.turno, tk.Entry),
        ("Série (1 dígito)", str(aluno.serie), tk.Entry),
        ("Turma (3 dígitos)", str(aluno.turma), tk.Entry),
        ("Matrícula (10 dígitos)", str(aluno.matricula), tk.Entry),
        ("Estudante", aluno.estudante, tk.Entry),
        ("Sexo (Mas/Fem)", sexo_display, tk.Entry)
    ]

    for i, (label_text, valor, widget_type) in enumerate(labels):
        tk.Label(janela, text=label_text).grid(row=i, column=0, padx=5, pady=2, sticky="w")
        entry = widget_type(janela)
        entry.insert(0, valor)
        entry.grid(row=i, column=1, padx=5, pady=2)
        campos[label_text] = entry

    # Campo de data_nascimento com DateEntry
    tk.Label(janela, text="Data Nascimento (DD/MM/YYYY)").grid(row=len(labels), column=0, padx=5, pady=2, sticky="w")
    entry_data_nascimento = DateEntry(janela, date_pattern='dd/mm/yyyy', locale='pt_BR')
    if aluno.data_nascimento and isinstance(aluno.data_nascimento, date):
        entry_data_nascimento.set_date(aluno.data_nascimento)
    else:
        entry_data_nascimento.set_date(date.today())  # Valor padrão
    entry_data_nascimento.grid(row=len(labels), column=1, padx=5, pady=2)
    campos["Data Nascimento"] = entry_data_nascimento

    # Campo Bloqueado com Checkbutton e exibição da data de bloqueio
    bloqueado_var = tk.BooleanVar(value=aluno.bloqueado == 'Sim')
    frame_bloqueado = tk.Frame(janela)
    frame_bloqueado.grid(row=len(labels)+1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    tk.Checkbutton(frame_bloqueado, text="Bloqueado?", variable=bloqueado_var).pack(side=tk.LEFT)

    # Label para exibir a data de bloqueio (atualizado dinamicamente)
    label_data_bloqueio = tk.Label(frame_bloqueado, text="")
    label_data_bloqueio.pack(side=tk.LEFT, padx=5)

    def atualizar_data_bloqueio():
        if bloqueado_var.get():
            # Se bloqueado, exibir a data de bloqueio existente ou a data atual
            if aluno.data_bloqueio and isinstance(aluno.data_bloqueio, date):
                data_texto = aluno.data_bloqueio.strftime("%d/%m/%Y")
            else:
                data_texto = date.today().strftime("%d/%m/%Y")
            label_data_bloqueio.config(text=f"({data_texto})")
        else:
            # Se não bloqueado, limpar a data
            label_data_bloqueio.config(text="")

    # Atualizar a data inicialmente
    atualizar_data_bloqueio()

    # Vincular mudança no Checkbutton para atualizar a exibição
    bloqueado_var.trace("w", lambda *args: atualizar_data_bloqueio())

    def salvar_edicao():
        try:
            # Validações
            id_matriz = campos["ID Matriz (4 dígitos)"].get()
            if not re.fullmatch(r'\d{4}', id_matriz):
                raise ValueError("ID Matriz deve conter exatamente 4 números.")

            turno = campos["Turno (M/V/N)"].get()
            if turno not in ['M', 'V', 'N']:
                raise ValueError("Turno deve ser M, V ou N.")

            serie = campos["Série (1 dígito)"].get()
            if not re.fullmatch(r'\d{1}', serie):
                raise ValueError("Série deve conter 1 número.")

            turma = campos["Turma (3 dígitos)"].get()
            if not re.fullmatch(r'\d{3}', turma):
                raise ValueError("Turma deve conter 3 números.")

            matricula = campos["Matrícula (10 dígitos)"].get()
            if not re.fullmatch(r'\d{10}', matricula):
                raise ValueError("Matrícula deve conter 10 números.")

            estudante = campos["Estudante"].get()
            if re.search(r'\d', estudante) or not estudante.strip():
                raise ValueError("Nome do estudante não deve conter números ou estar em branco.")

            sexo = campos["Sexo (Mas/Fem)"].get()
            if sexo not in ['Mas', 'Fem']:
                raise ValueError("Sexo deve ser 'Mas' ou 'Fem'.")

            # Tratar data_nascimento
            data_nascimento = campos["Data Nascimento"].get_date()

            # Tratar bloqueado e data_bloqueio
            if bloqueado_var.get():
                aluno.bloqueado = 'Sim'
                # Manter data_bloqueio existente ou usar a data atual
                if not aluno.data_bloqueio or not isinstance(aluno.data_bloqueio, date):
                    aluno.data_bloqueio = date.today()
            else:
                aluno.bloqueado = 'Não'
                aluno.data_bloqueio = None

            # Atribuir valores ao objeto aluno
            aluno.id_matriz = int(id_matriz)
            aluno.turno = turno
            aluno.serie = int(serie)
            aluno.turma = int(turma)
            aluno.matricula = int(matricula)
            aluno.estudante = estudante.strip().title()
            aluno.sexo = sexo
            aluno.data_nascimento = data_nascimento

            print(f"Data de nascimento salva: {aluno.data_nascimento}")  # Log para depuração
            print(f"Bloqueado salvo: {aluno.bloqueado}")  # Log para depuração
            print(f"Data de bloqueio salva: {aluno.data_bloqueio}")  # Log para depuração

            if aluno.editar():
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
                callback()  # Atualiza a lista
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar o aluno.")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    tk.Button(janela, text="Salvar", command=salvar_edicao).grid(row=len(labels)+2, column=0, columnspan=2, pady=10)
    tk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=len(labels)+3, column=0, columnspan=2, pady=5)