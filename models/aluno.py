from database.conexao import conectar

class Aluno:
    def __init__(self, id_matriz, turno, serie, turma, matricula, estudante, sexo, data_nascimento, bloqueado, data_bloqueio=None, id=None):
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
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_aluno"
        cursor.execute(query)
        alunos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*aluno) for aluno in alunos]
