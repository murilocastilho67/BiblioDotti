from database.conexao import conectar

class Exemplar:
    def __init__(self, livro_id, status):
        self.livro_id = livro_id
        self.status = status  # 'disponível' ou 'emprestado'

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_exemplar (livro_id, status)
        VALUES (%s, %s)
        """
        cursor.execute(query, (self.livro_id, self.status))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_exemplar SET status=%s WHERE id=%s"
        cursor.execute(query, (self.status, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_exemplar WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_exemplar"
        cursor.execute(query)
        exemplares = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*exemplar) for exemplar in exemplares]

    @classmethod
    def buscar_por_livro(cls, livro_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_exemplar WHERE livro_id=%s"
        cursor.execute(query, (livro_id,))
        exemplares = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*exemplar) for exemplar in exemplares]
