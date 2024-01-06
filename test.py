import customtkinter as ctk
from pygame.mixer import init, Sound, music
import os
import sqlite3

caminhoBanco = 'dados/banco.db'

if not os.path.exists(caminhoBanco):
    os.makedirs('dados')
conexao = sqlite3.connect(caminhoBanco)
cursor = conexao.cursor()

# Criando a tabela se ela não existe
cursor.execute(
    'CREATE TABLE IF NOT EXISTS dados(caminho TEXT, nome TEXT, duracao FLOAT)')
conexao.commit()

# init mixer
init()


class Root(ctk.CTk):
    def __init__(self, **kwargs):
        global conexao, cursor
        super().__init__(**kwargs)
        # Variaves
        self.listaMusicas = []
        self.cursor = cursor
        self.conexao = conexao

        # Configuaracao da janela
        self.title('MidiaPlay')
        self.minsize(600, 300)
        self.configure(bg_color='#200937', fg_color='#200937')
        
        # Crinado o menu dock
        self.menuDock = ctk.CTkFrame(self, 40, corner_radius=0, fg_color='#13052b',)
        self.menuDock.place(x=0, y=0)
        
        
    def buscador(self, diretorio, filtro):
        '''Buscar por arquivos pelo sistema presisar do diretorio e o filtro '''
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho = os.path.join(raiz, arquivo)
                if cursor.execute("SELECT * FROM dados WHERE caminho = ? ", (caminho,)).fetchone() != None:
                    pass
                elif any(filtro in arquivo):
                    self.listaMusicas.append(
                        (arquivo.split(".")[0], caminho, self.convesorTempo(Sound.get_length())))
                    self.cursor.execute(
                        "INSERT INTO dados(nome, caminho, duracao) VALUES(?,?,?)", self.listaMusicas[-1])

    def convesorTempo(self, tempoSegundo):
        return float(f'{int(tempoSegundo // 60)}.{int(tempoSegundo % 60)}')


if __name__ == "__main__":
    Root().mainloop()
