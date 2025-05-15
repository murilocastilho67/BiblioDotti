import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from models.aluno import Aluno
from views.editar_aluno_window import editar_aluno_window


def gerenciar_alunos_window():
    janela = tk.Toplevel()
    janela.title("Gerenciar Alunos")
    janela.geometry("1100x600")  # Tamanho inicial maior para acomodar colunas
    janela.minsize(800, 400)  # Tamanho mínimo para evitar colapso
    janela.resizable(True, True)  # Permitir redimensionamento

    # Frame de filtros
    frame_filtros = tk.LabelFrame(janela, text="Filtros", padx=10, pady=5)
    frame_filtros.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(frame_filtros, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(frame_filtros)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame_filtros, text="Matrícula:").grid(row=0, column=2, padx=5)
    entry_matricula = tk.Entry(frame_filtros)
    entry_matricula.grid(row=0, column=3)

    tk.Label(frame_filtros, text="Turno:").grid(row=0, column=4, padx=5)
    combo_turno = ttk.Combobox(frame_filtros, values=["", "Matutino", "Vespertino", "Noturno"], state="readonly")
    combo_turno.grid(row=0, column=5)

    tk.Label(frame_filtros, text="Série:").grid(row=1, column=0, padx=5)
    entry_serie = tk.Entry(frame_filtros)
    entry_serie.grid(row=1, column=1)

    tk.Label(frame_filtros, text="Turma:").grid(row=1, column=2, padx=5)
    entry_turma = tk.Entry(frame_filtros)
    entry_turma.grid(row=1, column=3)

    # Função para converter os valores de turno para o banco de dados
    def converter_turno(turno):
        if turno == "Matutino":
            return "M"
        elif turno == "Vespertino":
            return "V"
        elif turno == "Noturno":
            return "N"
        return ""

    # Função de atualização da lista com os filtros aplicados
    def atualizar_lista():
        tree.delete(*tree.get_children())

        turno_selecionado = combo_turno.get()
        turno_banco = converter_turno(turno_selecionado)

        alunos = Aluno.listar(
            turno=turno_banco or None,
            serie=entry_serie.get() or None,
            turma=entry_turma.get() or None,
            matricula=entry_matricula.get() or None,
            estudante=entry_nome.get() or None
        )
        for aluno in alunos:
            # Formatar datas
            try:
                data_nascimento = aluno.data_nascimento.strftime("%d/%m/%Y")
            except AttributeError:
                data_nascimento = aluno.data_nascimento

            if aluno.data_bloqueio:
                try:
                    data_bloqueio = aluno.data_bloqueio.strftime("%d/%m/%Y")
                except AttributeError:
                    data_bloqueio = aluno.data_bloqueio
            else:
                data_bloqueio = ""

            tree.insert("", tk.END, values=(
                aluno.id, aluno.id_matriz, aluno.turno, aluno.serie, aluno.turma,
                aluno.matricula, aluno.estudante, aluno.sexo,
                data_nascimento, aluno.bloqueado,
                data_bloqueio
            ))

    # Frame para o Treeview com barras de rolagem
    frame_tree = tk.Frame(janela)
    frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Canvas para suportar barras de rolagem
    canvas = tk.Canvas(frame_tree)
    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Posicionamento dos widgets
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame interno no canvas
    tree_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=tree_frame, anchor="nw")

    # Treeview
    colunas = (
        "ID", "ID Matriz", "Turno", "Série", "Turma", "Matrícula", "Estudante", "Sexo",
        "Data Nascimento", "Bloqueado", "Data Bloqueio"
    )
    tree = ttk.Treeview(tree_frame, columns=colunas, show='headings')
    for col in colunas:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    # Definir larguras iniciais das colunas (proporcionais)
    larguras_iniciais = {
        "ID": 50,
        "ID Matriz": 80,
        "Turno": 100,
        "Série": 60,
        "Turma": 80,
        "Matrícula": 120,
        "Estudante": 200,  # Maior para nomes longos
        "Sexo": 80,
        "Data Nascimento": 100,
        "Bloqueado": 80,
        "Data Bloqueio": 100
    }
    for col in colunas:
        tree.column(col, width=larguras_iniciais.get(col, 100), anchor="w")

    # Função para ajustar larguras das colunas dinamicamente
    def ajustar_colunas(event=None):
        largura_total = canvas.winfo_width() - 20  # Ajuste para margens
        if largura_total < 100:  # Evitar divisão por zero
            return

        # Calcular proporção baseada nas larguras iniciais
        total_largura_inicial = sum(larguras_iniciais.values())
        for col in colunas:
            proporcao = larguras_iniciais.get(col, 100) / total_largura_inicial
            nova_largura = max(50, int(largura_total * proporcao))  # Mínimo de 50px
            tree.column(col, width=nova_largura)

        # Atualizar região de rolagem
        tree_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Vincular redimensionamento
    canvas.bind("<Configure>", ajustar_colunas)
    janela.bind("<Configure>", ajustar_colunas)

    # Atualizar região de rolagem inicial
    def configurar_scroll(event=None):
        tree_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    tree.bind("<Configure>", configurar_scroll)

    def editar_aluno():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Por favor, selecione um aluno para editar.")
            return
        valores = tree.item(selected_item)['values']

        # Converter turno
        turno = valores[2]
        if turno == 'Matutino':
            turno = 'M'
        elif turno == 'Vespertino':
            turno = 'V'
        elif turno == 'Noturno':
            turno = 'N'
        print(f"Turno convertido em editar_aluno: {turno}")

        # Converter data_nascimento
        data_nascimento = None
        if valores[8]:
            try:
                data_nascimento = datetime.strptime(valores[8], '%d/%m/%Y').date()
            except (ValueError, TypeError):
                try:
                    data_nascimento = datetime.strptime(valores[8], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    print(f"Data de Nascimento inválida em editar_aluno: {valores[8]}")

        # Converter data_bloqueio
        data_bloqueio = None
        if valores[10] and valores[10].strip():
            try:
                data_bloqueio = datetime.strptime(valores[10], '%d/%m/%Y').date()
            except (ValueError, TypeError):
                try:
                    data_bloqueio = datetime.strptime(valores[10], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    print(f"Data de Bloqueio inválida em editar_aluno: {valores[10]}")
        print(f"Data de bloqueio em editar_aluno: {data_bloqueio}")

        aluno = Aluno(
            id=valores[0],
            id_matriz=valores[1],
            turno=turno,
            serie=valores[3],
            turma=valores[4],
            matricula=valores[5],
            estudante=valores[6],
            sexo=valores[7],
            data_nascimento=data_nascimento,
            bloqueado=valores[9],
            data_bloqueio=data_bloqueio
        )
        editar_aluno_window(aluno, atualizar_lista)

    def excluir_aluno():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Por favor, selecione um aluno para excluir.")
            return
        valores = tree.item(selected_item)['values']
        aluno = Aluno(
            id=valores[0],
            id_matriz=valores[1],
            turno=valores[2],
            serie=valores[3],
            turma=valores[4],
            matricula=valores[5],
            estudante=valores[6],
            sexo=valores[7],
            data_nascimento=valores[8],
            bloqueado=valores[9],
            data_bloqueio=valores[10]
        )
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