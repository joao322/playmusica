import sqlite3

try:
    conexao = sqlite3.connect('dados/banco-dados.db') 
except sqlite3.OperationalError:
    os.makedirs('dados')
    conexao = sqlite3.connect('dados/banco-dados.db')
    curso.execute(" CREATE TABLE dados(nome TEXT, idade INTER)")
curso = conexao.cursor()
curso.execute('INSERT INTO dados VALUES("joao", 12)')
print(curso.execute('SELECT * FROM dados WHERE nome = "oao" ').fetchall())