from database.conexao import conectar

class Turma:
    def __init__(self, id_turma, serie, periodo, tipo_ensino):
        self.id_turma = id_turma
        self.serie = serie
        self.periodo = periodo
        self.tipo_ensino = tipo_ensino

    def salvar(self):
        # Lógica para salvar uma turma no banco de dados
        conn = conectar()  # Usa a função conectar do módulo conexao
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_turma (serie, periodo, tipo_ensino)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (self.serie, self.periodo, self.tipo_ensino))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def listar(cls):
        # Lógica para listar todas as turmas do banco de dados
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM tb_turma"
        cursor.execute(query)
        turmas = cursor.fetchall()
        cursor.close()
        conn.close()
        return [cls(id_turma=row[0], serie=row[1], periodo=row[2], tipo_ensino=row[3]) for row in turmas]

    def editar(self):
        # Lógica para editar uma turma
        conn = conectar()
        cursor = conn.cursor()
        query = """
        UPDATE tb_turma
        SET serie = %s, periodo = %s, tipo_ensino = %s
        WHERE id = %s
        """
        cursor.execute(query, (self.serie, self.periodo, self.tipo_ensino, self.id_turma))
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self):
        # Lógica para excluir uma turma
        conn = conectar()
        cursor = conn.cursor()
        query = "DELETE FROM tb_turma WHERE id = %s"
        cursor.execute(query, (self.id_turma,))
        conn.commit()
        cursor.close()
        conn.close()
