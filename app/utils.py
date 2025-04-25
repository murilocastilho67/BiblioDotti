from database.conexao import conectar

def get_id(nome, tabela):
    conexao = conectar()
    cursor = conexao.cursor()
    query = f"SELECT id FROM tb_{tabela} WHERE nome = %s"
    cursor.execute(query, (nome,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else None


def carregar_opcoes_combobox(combobox, tabela):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT nome FROM {tabela}")  # Aqui você seleciona todos os nomes da tabela
    resultados = cursor.fetchall()
    conn.close()

    # Preenche a combobox com os resultados da consulta
    combobox['values'] = [resultado[0] for resultado in resultados]

