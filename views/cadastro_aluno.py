import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date
import re
from models.aluno import Aluno
from views.gerenciar_alunos_window import gerenciar_alunos_window
from database.conexao import conectar


def carregar_turmas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM tb_turma ORDER BY nome")
    turmas = [(row[0], row[1]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return turmas


def cadastrar_aluno():
    try:
        id_matriz = entry_id_matriz.get()
        turno = turno_var.get()
        serie = entry_serie.get()
        turma = turma_combobox.get()
        matricula = entry_matricula.get()
        estudante = entry_nome.get()
        sexo = sexo_var.get()
        data_nascimento = entry_data_nascimento.get_date()

        # Validações
        if not re.fullmatch(r'\d{4}', id_matriz):
            raise ValueError("ID Matriz deve conter exatamente 4 números.")
        if turno not in ['M', 'V', 'N']:
            raise ValueError("Selecione um turno válido (Matutino, Vespertino ou Noturno).")
        if not re.fullmatch(r'\d{1}', serie):
            raise ValueError("Série deve conter 1 número.")
        if not turma:
            raise ValueError("Selecione uma turma válida.")
        if not re.fullmatch(r'\d{10}', matricula):
            raise ValueError("Matrícula deve conter 10 números.")
        if re.search(r'\d', estudante) or not estudante.strip():
            raise ValueError("Nome do estudante não deve conter números ou estar em branco.")
        if sexo not in ['M', 'F']:
            raise ValueError("Selecione o sexo do aluno (Masculino ou Feminino).")

        # Obter o ID da turma selecionada
        turma_id = next(id for id, nome in turmas if nome == turma)

        aluno = Aluno(
            id_matriz=int(id_matriz),
            turno=turno,
            serie=int(serie),
            turma=turma_id,
            matricula=int(matricula),
            estudante=estudante.strip().title(),
            sexo='Mas' if sexo == 'M' else 'Fem',
            data_nascimento=data_nascimento,
            bloqueado='Não',
            data_bloqueio=None
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
    turma_combobox.set("")
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    sexo_var.set("")
    entry_data_nascimento.set_date(date.today())


def cadastro_aluno_window():
    global entry_id_matriz, turno_var, entry_serie, turma_combobox
    global entry_matricula, entry_nome, sexo_var, entry_data_nascimento
    global turmas

    window = tk.Toplevel()
    window.title("Cadastro de Aluno")

    # Centralizar janela
    largura = 600
    altura = 400
    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    window.minsize(550, 350)
    window.configure(bg="#f0f0f0")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Frame principal
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    # Linha 1: ID Matriz e Matrícula
    tk.Label(frame, text="ID Matriz (4 dígitos):", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="w",
                                                                                          padx=5, pady=5)
    entry_id_matriz = ttk.Entry(frame, width=15)
    entry_id_matriz.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Matrícula (10 dígitos):", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=2, sticky="w",
                                                                                           padx=5, pady=5)
    entry_matricula = ttk.Entry(frame, width=20)
    entry_matricula.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # Linha 2: Série e Turma
    tk.Label(frame, text="Série (1 dígito):", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w",
                                                                                     padx=5, pady=5)
    entry_serie = ttk.Entry(frame, width=10)
    entry_serie.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Turma:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    turmas = carregar_turmas()
    turma_combobox = ttk.Combobox(frame, values=[nome for _, nome in turmas], width=20, state="readonly")
    turma_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # Linha 3: Nome do Estudante
    tk.Label(frame, text="Nome do Estudante:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky="w",
                                                                                      padx=5, pady=5)
    entry_nome = ttk.Entry(frame, width=50)
    entry_nome.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

    # Linha 4: Turno
    tk.Label(frame, text="Turno:", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    turno_var = tk.StringVar()
    frame_turno = tk.Frame(frame, bg="#f0f0f0")
    frame_turno.grid(row=3, column=1, columnspan=3, sticky="w", padx=5, pady=5)
    for valor, texto in [('M', 'Matutino'), ('V', 'Vespertino'), ('N', 'Noturno')]:
        tk.Radiobutton(frame_turno, text=texto, variable=turno_var, value=valor, font=("Arial", 10), bg="#f0f0f0").pack(
            side="left", padx=5)

    # Linha 5: Sexo
    tk.Label(frame, text="Sexo:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    sexo_var = tk.StringVar()
    frame_sexo = tk.Frame(frame, bg="#f0f0f0")
    frame_sexo.grid(row=4, column=1, columnspan=3, sticky="w", padx=5, pady=5)
    tk.Radiobutton(frame_sexo, text="Masculino", variable=sexo_var, value='M', font=("Arial", 10), bg="#f0f0f0").pack(
        side="left", padx=5)
    tk.Radiobutton(frame_sexo, text="Feminino", variable=sexo_var, value='F', font=("Arial", 10), bg="#f0f0f0").pack(
        side="left", padx=5)

    # Linha 6: Data de Nascimento
    tk.Label(frame, text="Data de Nascimento:", font=("Arial", 10), bg="#f0f0f0").grid(row=5, column=0, sticky="w",
                                                                                       padx=5, pady=5)
    entry_data_nascimento = DateEntry(frame, date_pattern='dd/mm/yyyy', locale='pt_BR', width=15)
    entry_data_nascimento.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Linha 7: Botões
    frame_botoes = tk.Frame(frame, bg="#f0f0f0")
    frame_botoes.grid(row=6, column=0, columnspan=4, pady=10)
    tk.Button(frame_botoes, text="Salvar", command=cadastrar_aluno, font=("Arial", 10), bg="#4CAF50", fg="white",
              width=12).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Limpar", command=limpar_campos, font=("Arial", 10), bg="#FFC107", fg="black",
              width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Gerenciar Alunos", command=gerenciar_alunos_window, font=("Arial", 10), bg="#2196F3",
              fg="white", width=15).grid(row=0, column=2, padx=5)

    window.mainloop()