from database.conexao import conectar

class Tipo:
    def __init__(self, descricao):
        self.descricao = descricao

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO tb_tipo (descricao) VALUES (%s)"
        cursor.execute(query, (self.descricao,))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_tipo SET descricao=%s WHERE id=%s"
        cursor.execute(query, (self.descricao, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_tipo WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_tipo"
        cursor.execute(query)
        tipos = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*tipo) for tipo in tipos]
