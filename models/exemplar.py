from database.conexao import conectar

class Exemplar:
    def __init__(self, id, livro_id, codigo_exemplar, disponivel=True):
        self.id = id
        self.livro_id = livro_id
        self.codigo_exemplar = codigo_exemplar
        self.disponivel = disponivel

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_exemplar (id_livro, codigo_exemplar, disponivel)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (self.livro_id, self.codigo_exemplar, self.disponivel))
        conn.commit()
        self.id = cursor.lastrowid
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_exemplar SET id_livro=%s, codigo_exemplar=%s, disponivel=%s WHERE id=%s"
        cursor.execute(query, (self.livro_id, self.codigo_exemplar, self.disponivel, self.id))
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
        query = "SELECT id, id_livro, codigo_exemplar, disponivel FROM tb_exemplar"
        cursor.execute(query)
        exemplares = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*exemplar) for exemplar in exemplares]

    @classmethod
    def buscar_por_livro(cls, livro_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT id, id_livro, codigo_exemplar, disponivel FROM tb_exemplar WHERE id_livro=%s"
        cursor.execute(query, (livro_id,))
        exemplares = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*exemplar) for exemplar in exemplares]

    @classmethod
    def buscar_disponiveis_por_livro(cls, livro_id):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT id, id_livro, codigo_exemplar, disponivel FROM tb_exemplar WHERE id_livro=%s AND disponivel=TRUE"
        cursor.execute(query, (livro_id,))
        exemplares = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*exemplar) for exemplar in exemplares]