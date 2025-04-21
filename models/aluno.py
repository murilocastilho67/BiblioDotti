from database.conexao import conectar

class Aluno:
    def __init__(self, nome, turma_id, bloqueado, data_bloqueio):
        self.nome = nome
        self.turma_id = turma_id
        self.bloqueado = bloqueado
        self.data_bloqueio = data_bloqueio

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_alunos (nome, turma_id, bloqueado, data_bloqueio)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.nome, self.turma_id, self.bloqueado, self.data_bloqueio))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE tb_alunos SET nome=%s, turma_id=%s, bloqueado=%s, data_bloqueio=%s
        WHERE id=%s
        """
        cursor.execute(query, (self.nome, self.turma_id, self.bloqueado, self.data_bloqueio, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_alunos WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_alunos"
        cursor.execute(query)
        alunos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*aluno) for aluno in alunos]
