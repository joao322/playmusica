import sqlite3
import os

# Configurando o banco de dados
caminho_banco = 'dados/banco.db'
if not os.path.exists(caminho_banco):
    os.makedirs('dados')
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# Criando a tabela se ela não existe
cursor.execute('CREATE TABLE IF NOT EXISTS dados(caminho TEXT], nome TEXT, duracao FLOAT)')
conexao.commit()

def buscar_musicas(diretorio):
    # Verificando se tem arquivos inexistentes e removendo us
    lista_caminho_musica = cursor.execute('SELECT caminho FROM dados').fetchall()
    for caminho_musica in lista_caminho_musica:
        caminho = caminho_musica[0]
        if not os.path.exists(caminho):
            cursor.execute('DELETE FROM dados WHERE caminho = ?', (caminho,))
            conexao.commit()
    tempoAtualizarTela = 6
    
    # Busca por arquivos de música automaticamente
    filtros = ('.mp3', '.ogg')
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            
            # Atualizar a tela 
            if tempoAtualizarTela <= 0:
                tempoAtualizarTela = 6
                continue
                
            if any(filtro in arquivo.lower() for filtro in filtros):
                if not cursor.execute('SELECT * FROM dados WHERE caminho = ?', (caminho_arquivo,)).fetchone():
                    cursor.execute('INSERT INTO dados(caminho, nome, duracao) VALUES(?, ?, ?)', (caminho_arquivo, arquivo.split(".")[0], 0.0))
                    conexao.commit()
            else: 
                tempoAtualizarTela -=1
def 
buscar_musicas('/home')

 