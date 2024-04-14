import os
import sqlite3
from pygame import error
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


def buscador(diretorio, filtros):
    '''Buscar por arquivos pelo sistema presisar do diretorio e o filtro '''
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminhoArquivo = os.path.join(raiz, arquivo)
            
            if cursor.execute("SELECT * FROM dados WHERE caminho = ? ", (caminhoArquivo,)).fetchone() != None:
               pass
           
            if any(arquivo.endswith(filtro) for filtro in filtros):
                try:
                    listaMusicas.append(
                        (arquivo[:-4], caminhoArquivo, convesorTempo(Sound(caminhoArquivo).get_length())))
                except error as e:
                    listaMusicas.append((arquivo[:-4], caminhoArquivo, -1.0)) 
                    
                finally:
                    cursor.execute(
                        "INSERT INTO dados(nome, caminho, duracao) VALUES(?,?,?)", listaMusicas[-1])  
                    
    return listaMusicas

def convesorTempo(tempoSegundo):
    return float(f'{int(tempoSegundo // 60)}.{int(tempoSegundo % 60)}')
