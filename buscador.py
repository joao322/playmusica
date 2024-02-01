import os
import sqlite3
from pygame.mixer import init, Sound

caminhoBanco = 'dados/banco.db'
init()

if not os.path.exists(caminhoBanco):
    os.makedirs('dados')
conexao = sqlite3.connect(caminhoBanco)
cursor = conexao.cursor()
listaMusicas = []

# Criando a tabela se ela não existe
cursor.execute(
    'CREATE TABLE IF NOT EXISTS dados(caminho TEXT, nome TEXT, duracao FLOAT)')
conexao.commit()


def buscador(diretorio, filtro):
    '''Buscar por arquivos pelo sistema presisar do diretorio e o filtro '''
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho = os.path.join(raiz, arquivo)
            if cursor.execute("SELECT * FROM dados WHERE caminho = ? ", (caminho,)).fetchone() != None:
               pass
            if any(filtra in arquivo for filtra in filtro) and arquivo.count('.') == 1:
                listaMusicas.append(
                    (arquivo.split(".")[0], caminho, convesorTempo(Sound(caminho).get_length())))
                cursor.execute(
                    "INSERT INTO dados(nome, caminho, duracao) VALUES(?,?,?)", listaMusicas[-1])
            
    return listaMusicas

def convesorTempo(tempoSegundo):
    return float(f'{int(tempoSegundo // 60)}.{int(tempoSegundo % 60)}')
