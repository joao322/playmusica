import sqlite3
import os

# Configurando o banco de dados
caminho_banco = 'dados/banco.db'
if not os.path.exists(caminho_banco):
    os.makedirs('dados')
conexao = sqlite3.connect(caminho_banco)

cursor = conexao.cursor()

# Criando a tabla se ela nao existe 
cursor.execute('CREATE TABLE IF NOT EXISTS dados(caminho TEXT, nome TEXT, duracao FLOAT)')
conexao.commit()

def buscar_musicas(diretorio):
    "buscar por aquivos de musica altomaticamente."
    listaCaminhoMusica = cursor.execute('SELECT caminho FROM dados').fetchall()
    for caminhoMusica in listaCaminhoMusica:
        if not os.path.exists(caminhoMusica):
            cursor.execute('DELET * FROM dados WHERE caminho = ?', (caminhoMusica,))
            conexao.commit()
    filtros = ('.mp3, .ogg')
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            if any(filtro in arquivo for filtro in filtros) and not cursor.execute('SELECT * FROM dados WHERE caminho = ?', (caminho_arquivo,)).fetchone():
                cursor.execute('INSERT INTO dados(caminho, nome, duracao) VALUES(?, ?, ?)', (caminho_arquivo, arquivo.split(".")[0], 0.0))
                conexao.commit()
                
buscar_musicas('/home')   
