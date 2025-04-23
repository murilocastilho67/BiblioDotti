CREATE DATABASE IF NOT EXISTS db_biblioteca_dotti;
USE db_biblioteca_dotti;

-- AUTOR
CREATE TABLE tb_autor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- CATEGORIA
CREATE TABLE tb_categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- EDITORA
CREATE TABLE tb_editora (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- TIPO
CREATE TABLE tb_tipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- TURMA
CREATE TABLE tb_turma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- LIVRO
CREATE TABLE tb_livro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    id_autor INT,
    id_categoria INT,
    id_editora INT,
    id_tipo INT,
    cor VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Disponível',

    FOREIGN KEY (id_autor) REFERENCES tb_autor(id),
    FOREIGN KEY (id_categoria) REFERENCES tb_categoria(id),
    FOREIGN KEY (id_editora) REFERENCES tb_editora(id),
    FOREIGN KEY (id_tipo) REFERENCES tb_tipo(id)
);

-- EXEMPLAR (um livro pode ter vários exemplares físicos)
CREATE TABLE tb_exemplar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_livro INT NOT NULL,
    codigo_exemplar VARCHAR(50) NOT NULL UNIQUE,
    disponivel BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (id_livro) REFERENCES tb_livro(id)
);

-- ALUNO
CREATE TABLE tb_aluno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    id_turma INT,

    FOREIGN KEY (id_turma) REFERENCES tb_turma(id)
);

-- EMPRÉSTIMO
CREATE TABLE tb_emprestimo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_exemplar INT NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_prevista_devolucao DATE NOT NULL,
    observacoes TEXT,

    FOREIGN KEY (id_aluno) REFERENCES tb_aluno(id),
    FOREIGN KEY (id_exemplar) REFERENCES tb_exemplar(id)
);

-- DEVOLUÇÃO
CREATE TABLE tb_devolucao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_emprestimo INT NOT NULL,
    data_devolucao DATE NOT NULL,
    observacoes TEXT,

    FOREIGN KEY (id_emprestimo) REFERENCES tb_emprestimo(id)
);

-- COR
CREATE TABLE tb_cor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

select * from tb_autor
select * from tb_categoria
select * from tb_cor
select * from tb_livro
select * from tb_editora
select * from tb_tipo
select * from tb_exemplar



ALTER TABLE tb_livro DROP COLUMN cor;
ALTER TABLE tb_livro ADD COLUMN id_cor INT;
ALTER TABLE tb_livro ADD CONSTRAINT fk_cor FOREIGN KEY (id_cor) REFERENCES tb_cor(id);


