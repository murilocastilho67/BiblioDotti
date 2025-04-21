from database.conexao import conectar

class Emprestimo:
    def __init__(self, aluno_id, exemplar_id, data_emprestimo, data_devolucao_prevista, observacoes=None):
        self.aluno_id = aluno_id
        self.exemplar_id = exemplar_id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista
        self.observacoes = observacoes

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_emprestimo (aluno_id, exemplar_id, data_emprestimo, data_devolucao_prevista, observacoes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.aluno_id, self.exemplar_id, self.data_emprestimo, self.data_devolucao_prevista, self.observacoes))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE tb_emprestimo SET aluno_id=%s, exemplar_id=%s, data_emprestimo=%s, data_devolucao_prevista=%s, observacoes=%s
        WHERE id=%s
        """
        cursor.execute(query, (self.aluno_id, self.exemplar_id, self.data_emprestimo, self.data_devolucao_prevista, self.observacoes, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_emprestimo WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_emprestimo"
        cursor.execute(query)
        emprestimos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*emprestimo) for emprestimo in emprestimos]

    @classmethod
    def listar_ativos(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_emprestimo WHERE data_devolucao IS NULL"
        cursor.execute(query)
        emprestimos_ativos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*emprestimo) for emprestimo in emprestimos_ativos]
