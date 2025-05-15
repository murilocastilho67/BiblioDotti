from database.conexao import conectar
from datetime import datetime


class Aluno:
    def __init__(self, id, id_matriz, turno, serie, turma, matricula, estudante, sexo, data_nascimento, bloqueado,
                 data_bloqueio=None):
        self.id = id
        self.id_matriz = id_matriz
        self.turno = turno
        self.serie = serie
        self.turma = turma
        self.matricula = matricula
        self.estudante = estudante
        self.sexo = sexo
        self.data_nascimento = data_nascimento
        self.bloqueado = bloqueado
        self.data_bloqueio = data_bloqueio

    def salvar(self):
        try:
            conn = conectar()
            cursor = conn.cursor()

            # Garantir que as datas estejam no formato correto
            if isinstance(self.data_nascimento, str):
                self.data_nascimento = datetime.strptime(self.data_nascimento, '%d/%m/%Y')
                print(f"Data de Nascimento formatada: {self.data_nascimento}")
            if self.data_bloqueio and isinstance(self.data_bloqueio, str):
                self.data_bloqueio = datetime.strptime(self.data_bloqueio, '%d/%m/%Y')
                print(f"Data de Bloqueio formatada: {self.data_bloqueio}")

            query = """
                INSERT INTO tb_aluno (id_matriz, turno, serie, turma, matricula, estudante, sexo, data_nascimento, bloqueado, data_bloqueio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (
                self.id_matriz, self.turno, self.serie, self.turma,
                self.matricula, self.estudante, self.sexo,
                self.data_nascimento, self.bloqueado, self.data_bloqueio
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao salvar aluno:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def editar(self):
        try:
            conn = conectar()
            cursor = conn.cursor()

            # Validar e corrigir o campo turno
            turno_map = {'Matutino': 'M', 'Vespertino': 'V', 'Noturno': 'N'}
            if self.turno in turno_map:
                self.turno = turno_map[self.turno]
            elif self.turno not in ('M', 'V', 'N'):
                print(f"Valor inválido para turno: {self.turno}. Convertendo para 'M' por padrão.")
                self.turno = 'M'  # Valor padrão caso seja inválido

            # Garantir que as datas estejam no formato correto
            if isinstance(self.data_nascimento, str):
                if self.data_nascimento.strip():
                    try:
                        self.data_nascimento = datetime.strptime(self.data_nascimento, '%d/%m/%Y').date()
                        print(f"Data de Nascimento formatada para edição (DD/MM/YYYY): {self.data_nascimento}")
                    except ValueError:
                        try:
                            self.data_nascimento = datetime.strptime(self.data_nascimento, '%Y-%m-%d').date()
                            print(
                                f"Data de Nascimento formatada (formato alternativo YYYY-MM-DD): {self.data_nascimento}")
                        except ValueError:
                            print(
                                f"Data de Nascimento inválida: {self.data_nascimento}. Definindo como None (não esperado).")
                            self.data_nascimento = None  # Não deve acontecer
                else:
                    print(f"Data de Nascimento é string vazia. Definindo como None (não esperado).")
                    self.data_nascimento = None  # Não deve acontecer
            elif isinstance(self.data_nascimento, datetime):
                self.data_nascimento = self.data_nascimento.date()
                print(f"Data de Nascimento já é datetime, convertida para date: {self.data_nascimento}")
            # Se já for date, não precisa converter

            # Tratar data_bloqueio
            if isinstance(self.data_bloqueio, str):
                if self.data_bloqueio.strip():
                    try:
                        self.data_bloqueio = datetime.strptime(self.data_bloqueio, '%d/%m/%Y').date()
                        print(f"Data de Bloqueio formatada para edição (DD/MM/YYYY): {self.data_bloqueio}")
                    except ValueError:
                        try:
                            self.data_bloqueio = datetime.strptime(self.data_bloqueio, '%Y-%m-%d').date()
                            print(f"Data de Bloqueio formatada (formato alternativo YYYY-MM-DD): {self.data_bloqueio}")
                        except ValueError:
                            print(f"Data de Bloqueio inválida: {self.data_bloqueio}. Definindo como None.")
                            self.data_bloqueio = None
                else:
                    print(f"Data de Bloqueio é string vazia. Definindo como None.")
                    self.data_bloqueio = None
            elif isinstance(self.data_bloqueio, datetime):
                self.data_bloqueio = self.data_bloqueio.date()
                print(f"Data de Bloqueio já é datetime, convertida para date: {self.data_bloqueio}")
            # Se self.data_bloqueio for None ou datetime.date, não precisa fazer nada
            print(f"Data de bloqueio antes da query: {self.data_bloqueio}")  # Log para depuração

            query = """
                UPDATE tb_aluno SET id_matriz=%s, turno=%s, serie=%s, turma=%s, matricula=%s, estudante=%s, sexo=%s, data_nascimento=%s, bloqueado=%s, data_bloqueio=%s
                WHERE id=%s
                """
            cursor.execute(query, (
                self.id_matriz, self.turno, self.serie, self.turma,
                self.matricula, self.estudante, self.sexo,
                self.data_nascimento, self.bloqueado, self.data_bloqueio, self.id
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao editar aluno:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def excluir(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            query = "DELETE FROM tb_aluno WHERE id=%s"
            cursor.execute(query, (self.id,))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao excluir aluno:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def listar(cls, turno=None, serie=None, turma=None, matricula=None, estudante=None):
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT id, id_matriz, turno, serie, turma, matricula, estudante, sexo, data_nascimento, bloqueado, data_bloqueio
            FROM tb_aluno
            WHERE 1=1
            """
        params = []

        if turno:
            query += " AND turno = %s"
            params.append(turno)

        if serie:
            query += " AND serie = %s"
            params.append(serie)

        if turma:
            query += " AND turma = %s"
            params.append(turma)

        if matricula:
            query += " AND matricula = %s"
            params.append(matricula)

        if estudante:
            query += " AND estudante LIKE %s"
            params.append(f"%{estudante}%")

        cursor.execute(query, tuple(params))
        alunos = cursor.fetchall()
        cursor.close()
        conn.close()

        alunos_formatados = []
        for aluno in alunos:
            aluno = list(aluno)

            # Convertendo as datas para string para exibição na interface gráfica
            if aluno[8]:
                aluno[8] = aluno[8].strftime('%d/%m/%Y') if isinstance(aluno[8], datetime) else aluno[8]
            if aluno[10]:
                aluno[10] = aluno[10].strftime('%d/%m/%Y') if isinstance(aluno[10], datetime) else aluno[10]

            # Converter o turno de M, V, N para Matutino, Vespertino e Noturno
            if aluno[2] == 'M':
                aluno[2] = 'Matutino'
            elif aluno[2] == 'V':
                aluno[2] = 'Vespertino'
            elif aluno[2] == 'N':
                aluno[2] = 'Noturno'

            alunos_formatados.append(cls(*aluno))

        return alunos_formatados
