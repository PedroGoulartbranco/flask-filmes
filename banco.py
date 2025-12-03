import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


#cursor.execute("""CREATE TABLE usuarios (
#       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#        nome varchar(100) NOT NULL,
#       email varchar(100) NOT NULL,
#        senha varchar(10) NOT NULL
#)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sugestoes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nome_musica VARCHAR(200) NOT NULL,
    artista VARCHAR(200), 
    data_sugestao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
)
""")

conexao.commit()
conexao.commit()