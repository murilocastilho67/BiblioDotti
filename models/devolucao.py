from database.conexao import conectar

class Devolucao:
    def __init__(self, emprestimo_id, data_devolucao, observacoes=None):
        self.emprestimo_id = emprestimo_id
        self.data_devolucao = data_devolucao
        self.observacoes = observacoes

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_devolucao (emprestimo_id, data_devolucao, observacoes)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (self.emprestimo_id, self.data_devolucao, self.observacoes))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_devolucao SET data_devolucao=%s, observacoes=%s WHERE id=%s"
        cursor.execute(query, (self.data_devolucao, self.observacoes, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_devolucao WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_devolucao"
        cursor.execute(query)
        devolucoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*devolucao) for devolucao in devolucoes]

    @classmethod
    def listar_pendentes(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_devolucao WHERE data_devolucao IS NULL"
        cursor.execute(query)
        devolucoes_pendentes = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*devolucao) for devolucao in devolucoes_pendentes]
