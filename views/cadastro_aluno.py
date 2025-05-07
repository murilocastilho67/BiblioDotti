import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
import re
from models.aluno import Aluno  # Certifique-se que o model aceite todos os campos
from gerenciar_alunos_window import gerenciar_alunos_window

def cadastrar_aluno():
    try:
        id_matriz = entry_id_matriz.get()
        turno = turno_var.get()
        serie = entry_serie.get()
        turma = entry_turma.get()
        matricula = entry_matricula.get()
        estudante = entry_nome.get()
        sexo = sexo_var.get()
        data_nascimento = entry_data_nascimento.get_date()
        bloqueado = 'Sim' if bloqueado_var.get() else 'Não'
        data_bloqueio = date.today() if bloqueado == 'Sim' else None

        # Validações
        if not re.fullmatch(r'\d{4}', id_matriz):
            raise ValueError("ID Matriz deve conter exatamente 4 números.")
        if turno not in ['M', 'V', 'N']:
            raise ValueError("Selecione um turno válido (M, V ou N).")
        if not re.fullmatch(r'\d{1}', serie):
            raise ValueError("Série deve conter 1 número.")
        if not re.fullmatch(r'\d{3}', turma):
            raise ValueError("Turma deve conter 3 números.")
        if not re.fullmatch(r'\d{10}', matricula):
            raise ValueError("Matrícula deve conter 10 números.")
        if re.search(r'\d', estudante) or not estudante.strip():
            raise ValueError("Nome do estudante não deve conter números ou estar em branco.")
        if sexo not in ['M', 'F']:
            raise ValueError("Selecione o sexo do aluno (Masculino ou Feminino).")

        aluno = Aluno(
            id_matriz=int(id_matriz),
            turno=turno,
            serie=int(serie),
            turma=int(turma),
            matricula=int(matricula),
            estudante=estudante.strip().title(),
            sexo='Mas' if sexo == 'M' else 'Fem',
            data_nascimento=data_nascimento,
            bloqueado=bloqueado,
            data_bloqueio=data_bloqueio
        )

        if aluno.salvar():
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar aluno.")

    except ValueError as e:
        messagebox.showerror("Erro de Validação", str(e))
    except Exception as e:
        messagebox.showerror("Erro inesperado", str(e))

def limpar_campos():
    entry_id_matriz.delete(0, tk.END)
    turno_var.set("")
    entry_serie.delete(0, tk.END)
    entry_turma.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    sexo_var.set("")
    entry_data_nascimento.set_date(date.today())
    bloqueado_var.set(False)

def cadastro_aluno_window():
    global entry_id_matriz, turno_var, entry_serie, entry_turma
    global entry_matricula, entry_nome, sexo_var, entry_data_nascimento, bloqueado_var

    window = tk.Toplevel()
    window.title("Cadastro de Aluno")
    window.geometry("400x600")
    window.resizable(False, False)

    def criar_label(texto):
        return tk.Label(window, text=texto, anchor="w")

    criar_label("ID Matriz (4 dígitos):").pack()
    entry_id_matriz = tk.Entry(window)
    entry_id_matriz.pack(pady=2)

    criar_label("Turno:").pack()
    turno_var = tk.StringVar()
    frame_turno = tk.Frame(window)
    for valor, texto in [('M', 'Matutino'), ('V', 'Vespertino'), ('N', 'Noturno')]:
        tk.Radiobutton(frame_turno, text=texto, variable=turno_var, value=valor).pack(side="left")
    frame_turno.pack(pady=2)

    criar_label("Série (1 dígito):").pack()
    entry_serie = tk.Entry(window)
    entry_serie.pack(pady=2)

    criar_label("Turma (3 dígitos):").pack()
    entry_turma = tk.Entry(window)
    entry_turma.pack(pady=2)

    criar_label("Matrícula (10 dígitos):").pack()
    entry_matricula = tk.Entry(window)
    entry_matricula.pack(pady=2)

    criar_label("Nome do Estudante:").pack()
    entry_nome = tk.Entry(window)
    entry_nome.pack(pady=2)

    criar_label("Sexo:").pack()
    sexo_var = tk.StringVar()
    frame_sexo = tk.Frame(window)
    tk.Radiobutton(frame_sexo, text="Masculino", variable=sexo_var, value='M').pack(side="left")
    tk.Radiobutton(frame_sexo, text="Feminino", variable=sexo_var, value='F').pack(side="left")
    frame_sexo.pack(pady=2)

    criar_label("Data de Nascimento:").pack()
    entry_data_nascimento = DateEntry(window, date_pattern='dd/mm/yyyy', locale='pt_BR')
    entry_data_nascimento.pack(pady=2)

    bloqueado_var = tk.BooleanVar()
    tk.Checkbutton(window, text="Bloquear aluno para empréstimos", variable=bloqueado_var).pack(pady=5)

    tk.Button(window, text="Salvar", command=cadastrar_aluno).pack(pady=10)
    tk.Button(window, text="Limpar", command=limpar_campos).pack(pady=2)
    tk.Button(window, text="Gerenciar Alunos", command=gerenciar_alunos_window).pack(pady=5)

    window.mainloop()
