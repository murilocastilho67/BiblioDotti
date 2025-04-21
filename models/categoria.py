from database.conexao import conectar

class Categoria:
    def __init__(self, descricao):
        self.descricao = descricao

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO tb_categoria (descricao) VALUES (%s)"
        cursor.execute(query, (self.descricao,))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_categoria SET descricao=%s WHERE id=%s"
        cursor.execute(query, (self.descricao, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_categoria WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_categoria"
        cursor.execute(query)
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*categoria) for categoria in categorias]
