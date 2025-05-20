import pandas as pd
from database.conexao import conectar
from datetime import datetime


def importar_alunos(arquivo_excel):
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(arquivo_excel)

        conn = conectar()
        cursor = conn.cursor()

        # Dicionário para armazenar turmas já inseridas (evitar duplicatas)
        turmas = {}

        # Contador de alunos inseridos e ignorados
        inseridos = 0
        ignorados = 0

        # Iterar sobre as linhas do DataFrame
        for index, row in df.iterrows():
            # Extrair dados da planilha
            matriz = int(row['Matriz'])
            turno = str(row['Turno']).strip()
            serie = int(row['Série'])
            turma = str(row['Turma']).strip()
            matricula = str(row['Matrícula']).strip()
            estudante = str(row['Estudante']).strip()
            sexo = str(row['Sexo']).strip()
            data_nasc_str = row['Data Nasc.']

            # Converter data de nascimento para formato MySQL (YYYY-MM-DD)
            try:
                data_nasc = pd.to_datetime(data_nasc_str, format='%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError as e:
                print(f"Erro na conversão da data para {estudante}: {e}")
                ignorados += 1
                continue

            # Verificar se a matrícula já existe
            cursor.execute("SELECT id FROM tb_aluno WHERE matricula = %s", (matricula,))
            if cursor.fetchone():
                print(f"Matrícula {matricula} ({estudante}) já existe, ignorando.")
                ignorados += 1
                continue

            # Criar nome da turma para tb_turma (ex.: "5269-M-6-601")
            nome_turma = f"{matriz}-{turno}-{serie}-{turma}"

            # Verificar se a turma já existe em tb_turma
            if nome_turma not in turmas:
                cursor.execute("SELECT id FROM tb_turma WHERE nome = %s", (nome_turma,))
                result = cursor.fetchone()
                if result:
                    turmas[nome_turma] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_turma (nome) VALUES (%s)", (nome_turma,))
                    turmas[nome_turma] = cursor.lastrowid

            id_turma = turmas[nome_turma]

            # Inserir aluno em tb_aluno
            cursor.execute("""
                INSERT INTO tb_aluno (id_matriz, turno, serie, turma, matricula, estudante, sexo, data_nascimento, bloqueado, data_bloqueio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (matriz, turno, serie, id_turma, matricula, estudante, sexo, data_nasc, 'Não', None))

            print(f"Aluno {estudante} inserido com sucesso.")
            inseridos += 1

        conn.commit()
        print(f"Importação concluída! {inseridos} alunos inseridos, {ignorados} ignorados.")

    except Exception as e:
        print(f"Erro durante a importação: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    arquivo_excel = "relacao_alunos.xlsx"
    importar_alunos(arquivo_excel)