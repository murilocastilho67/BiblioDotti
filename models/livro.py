from database.conexao import conectar

class Livro:
    def __init__(self, titulo, autor_id, categoria_id, editora_id, tipo_id, cor_id):
        self.titulo = titulo
        self.autor_id = autor_id
        self.categoria_id = categoria_id
        self.editora_id = editora_id
        self.tipo_id = tipo_id
        self.cor_id = cor_id

    def salvar(self):
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
            INSERT INTO tb_livro (titulo, id_autor, id_categoria, id_editora, id_tipo, id_cor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.titulo, self.autor_id, self.categoria_id, self.editora_id, self.tipo_id, self.cor_id)

        cursor.execute(query, valores)
        conexao.commit()
        livro_id = cursor.lastrowid  # <--- Aqui pegamos o ID do livro recém-inserido
        cursor.close()
        conexao.close()

        return livro_id

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE tb_livros SET codigo=%s, titulo=%s, autor_id=%s, categoria_id=%s, editora_id=%s, tipo_id=%s, status=%s, cor=%s
        WHERE id=%s
        """
        cursor.execute(query, (self.codigo, self.titulo, self.autor_id, self.categoria_id,
                               self.editora_id, self.tipo_id, self.status, self.cor, self.id))
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
        query = "SELECT codigo, titulo, autor_id, categoria_id, editora_id, tipo_id, status, cor FROM tb_livros"
        cursor.execute(query)
        livros = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*livro) for livro in livros]
