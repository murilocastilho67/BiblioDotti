from database.conexao import conectar

class Livro:
    def __init__(self, codigo, titulo, autor_id, categoria_id, editora_id, tipo_id, status, cor):
        self.codigo = codigo
        self.titulo = titulo
        self.autor_id = autor_id
        self.categoria_id = categoria_id
        self.editora_id = editora_id
        self.tipo_id = tipo_id
        self.status = status
        self.cor = cor

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_livros (codigo, titulo, autor_id, categoria_id, editora_id, tipo_id, status, cor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.codigo, self.titulo, self.autor_id, self.categoria_id, self.editora_id, self.tipo_id, self.status, self.cor))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE tb_livros SET codigo=%s, titulo=%s, autor_id=%s, categoria_id=%s, editora_id=%s, tipo_id=%s, status=%s, cor=%s
        WHERE id=%s
        """
        cursor.execute(query, (self.codigo, self.titulo, self.autor_id, self.categoria_id, self.editora_id, self.tipo_id, self.status, self.cor, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_livros WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_livros"
        cursor.execute(query)
        livros = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*livro) for livro in livros]