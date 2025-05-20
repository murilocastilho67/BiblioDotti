import pandas as pd
from database.conexao import conectar


def importar_livros(arquivo_excel):
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(arquivo_excel)

        conn = conectar()
        cursor = conn.cursor()

        # Dicionários para armazenar IDs de entidades já inseridas
        autores = {}
        categorias = {}
        editoras = {}
        tipos = {}
        cores = {}
        livros = {}  # Chave: (titulo, id_autor, id_categoria, id_editora, id_tipo, id_cor)

        # Contador para exemplares
        exemplar_counter = 1

        # Iterar sobre as linhas do DataFrame
        for index, row in df.iterrows():
            # Extrair dados da planilha
            titulo = str(row['Titulo']).strip()
            autor = str(row['Autor']).strip()
            categoria = str(row['Categoria']).strip()
            editora = str(row['Editora']).strip()
            tipo = str(row['Tipo']).strip()
            cor = str(row['Cor']).strip()

            # Verificar/criar autor
            if autor not in autores:
                cursor.execute("SELECT id FROM tb_autor WHERE nome = %s", (autor,))
                result = cursor.fetchone()
                if result:
                    autores[autor] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_autor (nome) VALUES (%s)", (autor,))
                    autores[autor] = cursor.lastrowid

            # Verificar/criar categoria
            if categoria not in categorias:
                cursor.execute("SELECT id FROM tb_categoria WHERE nome = %s", (categoria,))
                result = cursor.fetchone()
                if result:
                    categorias[categoria] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_categoria (nome) VALUES (%s)", (categoria,))
                    categorias[categoria] = cursor.lastrowid

            # Verificar/criar editora
            if editora not in editoras:
                cursor.execute("SELECT id FROM tb_editora WHERE nome = %s", (editora,))
                result = cursor.fetchone()
                if result:
                    editoras[editora] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_editora (nome) VALUES (%s)", (editora,))
                    editoras[editora] = cursor.lastrowid

            # Verificar/criar tipo
            if tipo not in tipos:
                cursor.execute("SELECT id FROM tb_tipo WHERE nome = %s", (tipo,))
                result = cursor.fetchone()
                if result:
                    tipos[tipo] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_tipo (nome) VALUES (%s)", (tipo,))
                    tipos[tipo] = cursor.lastrowid

            # Verificar/criar cor
            if cor not in cores:
                cursor.execute("SELECT id FROM tb_cor WHERE nome = %s", (cor,))
                result = cursor.fetchone()
                if result:
                    cores[cor] = result[0]
                else:
                    cursor.execute("INSERT INTO tb_cor (nome) VALUES (%s)", (cor,))
                    cores[cor] = cursor.lastrowid

            # Chave única para o livro
            livro_key = (titulo, autores[autor], categorias[categoria], editoras[editora], tipos[tipo], cores[cor])

            # Verificar se o livro já existe
            if livro_key not in livros:
                cursor.execute("""
                    SELECT id FROM tb_livro 
                    WHERE titulo = %s AND id_autor = %s AND id_categoria = %s 
                    AND id_editora = %s AND id_tipo = %s AND id_cor = %s
                """, (titulo, autores[autor], categorias[categoria], editoras[editora], tipos[tipo], cores[cor]))
                result = cursor.fetchone()
                if result:
                    livros[livro_key] = result[0]
                else:
                    cursor.execute("""
                        INSERT INTO tb_livro (titulo, id_autor, id_categoria, id_editora, id_tipo, id_cor, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (titulo, autores[autor], categorias[categoria], editoras[editora], tipos[tipo], cores[cor],
                          'Disponível'))
                    livros[livro_key] = cursor.lastrowid

            # Inserir exemplar
            codigo_exemplar = f"EXEMP-{exemplar_counter:03d}"
            cursor.execute("""
                INSERT INTO tb_exemplar (id_livro, codigo_exemplar, disponivel)
                VALUES (%s, %s, %s)
            """, (livros[livro_key], codigo_exemplar, True))
            exemplar_counter += 1

            print(f"Exemplar {codigo_exemplar} para '{titulo}' inserido com sucesso.")

        conn.commit()
        print("Importação concluída com sucesso!")

    except Exception as e:
        print(f"Erro durante a importação: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    arquivo_excel = "relacao_livros.xlsx"
    importar_livros(arquivo_excel)