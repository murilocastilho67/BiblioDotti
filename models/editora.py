from database.conexao import conectar

class Editora:
    def __init__(self, descricao):
        self.descricao = descricao

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "INSERT INTO tb_editoria (descricao) VALUES (%s)"
        cursor.execute(query, (self.descricao,))
        conn.commit()
        cursor.close()
        conn.close()

    def editar(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "UPDATE tb_editoria SET descricao=%s WHERE id=%s"
        cursor.execute(query, (self.descricao, self.id))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_editoria WHERE id=%s"
        cursor.execute(query, (self.id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_editoria"
        cursor.execute(query)
        editoras = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(*editora) for editora in editoras]
