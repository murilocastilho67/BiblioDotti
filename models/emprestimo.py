from database.conexao import conectar
from datetime import datetime, timedelta
from models.aluno import Aluno
from models.exemplar import Exemplar


class Emprestimo:
    def __init__(self, id_aluno, id_exemplar, data_emprestimo=None, data_prevista_devolucao=None, observacoes=None):
        self.id_aluno = id_aluno
        self.id_exemplar = id_exemplar
        self.data_emprestimo = data_emprestimo or datetime.now().date()
        self.data_prevista_devolucao = data_prevista_devolucao or (self.data_emprestimo + timedelta(days=7))
        self.observacoes = observacoes

    def validar(self):
        # Verifica se o aluno existe e não está bloqueado
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT bloqueado FROM tb_aluno WHERE id=%s", (self.id_aluno,))
        aluno = cursor.fetchone()
        cursor.close()
        conn.close()
        if not aluno:
            return False, "Aluno não encontrado."
        if aluno[0] == 'Sim':
            return False, "Aluno está bloqueado para empréstimos."

        # Verifica se o exemplar existe e está disponível
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT disponivel FROM tb_exemplar WHERE id=%s", (self.id_exemplar,))
        exemplar = cursor.fetchone()
        cursor.close()
        conn.close()
        if not exemplar:
            return False, "Exemplar não encontrado."
        if not exemplar[0]:
            return False, "Exemplar não está disponível."

        return True, ""

    def salvar(self):
        # Valida antes de salvar
        valido, mensagem = self.validar()
        if not valido:
            return False, mensagem

        # Salva o empréstimo
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_emprestimo (id_aluno, id_exemplar, data_emprestimo, data_prevista_devolucao, observacoes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
        self.id_aluno, self.id_exemplar, self.data_emprestimo, self.data_prevista_devolucao, self.observacoes))

        # Atualiza o status do exemplar
        cursor.execute("UPDATE tb_exemplar SET disponivel=FALSE WHERE id=%s", (self.id_exemplar,))

        conn.commit()
        self.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return True, "Empréstimo realizado com sucesso!"

    @classmethod
    def listar_ativos(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT e.id, e.id_aluno, e.id_exemplar, e.data_emprestimo, e.data_prevista_devolucao, e.observacoes
        FROM tb_emprestimo e
        LEFT JOIN tb_devolucao d ON e.id = d.id_emprestimo
        WHERE d.id IS NULL
        """
        cursor.execute(query)
        emprestimos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(id_aluno=row[1], id_exemplar=row[2], data_emprestimo=row[3], data_prevista_devolucao=row[4],
                    observacoes=row[5]) for row in emprestimos]