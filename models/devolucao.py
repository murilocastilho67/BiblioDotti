from database.conexao import conectar
from datetime import datetime
from models.exemplar import Exemplar


class Devolucao:
    def __init__(self, emprestimo_id, data_devolucao=None, observacoes=None):
        self.emprestimo_id = emprestimo_id
        self.data_devolucao = data_devolucao or datetime.now().date()
        self.observacoes = observacoes
        self.multa = 0.0

    def calcular_multa(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT data_prevista_devolucao FROM tb_emprestimo WHERE id=%s", (self.emprestimo_id,))
        data_prevista = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if self.data_devolucao > data_prevista:
            dias_atraso = (self.data_devolucao - data_prevista).days
            self.multa = dias_atraso * 2.00  # R$2,00 por dia de atraso
        else:
            self.multa = 0.00

    def salvar(self):
        # Verifica se o empréstimo existe
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_exemplar FROM tb_emprestimo WHERE id=%s", (self.emprestimo_id,))
        emprestimo = cursor.fetchone()
        if not emprestimo:
            cursor.close()
            conn.close()
            return False, "Empréstimo não encontrado."

        # Calcula a multa
        self.calcular_multa()

        # Salva a devolução
        query = """
        INSERT INTO tb_devolucao (id_emprestimo, data_devolucao, observacoes, multa)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.emprestimo_id, self.data_devolucao, self.observacoes, self.multa))

        # Atualiza o status do exemplar
        cursor.execute("UPDATE tb_exemplar SET disponivel=TRUE WHERE id=%s", (emprestimo[0],))

        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Devolução registrada com sucesso! Multa: R${self.multa:.2f}"

    @classmethod
    def listar_pendentes(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT e.id, a.estudante, l.titulo, e.data_emprestimo, e.data_prevista_devolucao
        FROM tb_emprestimo e
        JOIN tb_aluno a ON e.id_aluno = a.id
        JOIN tb_exemplar ex ON e.id_exemplar = ex.id
        JOIN tb_livro l ON ex.id_livro = l.id
        LEFT JOIN tb_devolucao d ON e.id = d.id_emprestimo
        WHERE d.id IS NULL
        """
        cursor.execute(query)
        pendentes = cursor.fetchall()
        cursor.close()
        conn.close()
        return pendentes