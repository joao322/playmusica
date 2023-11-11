import sqlite3
import os
from pygame import mixer
import customtkinter as ctk

# Configurando o banco de dados
caminho_banco = 'dados/banco.db'
if not os.path.exists(caminho_banco):
    os.makedirs('dados')
conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# Criando a tabela se ela não existe
cursor.execute(
    'CREATE TABLE IF NOT EXISTS dados(caminho TEXT, nome TEXT, duracao FLOAT)')
conexao.commit()
mixer.init()


class App(ctk.CTk):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.cursor = cursor
        # Configurando a janela
        self.title('playmisic')
        self.config(bg='black')
        self.listaMusic = ctk.CTkFrame(self)
        self.listaMusic.place(x=0, y=0)
        self.after(100, self.buscar_musicas)

    def playlist(self, arquivo):
        ctk.CTkButton(self.listaMusic, text=arquivo).pack()
        self.listaMusic.update()
    # Converte os segundo em minutos e segundos

    def converteTempo(self, tempoSegundo):
        return float(f'{int(tempoSegundo // 60)}.{int(tempoSegundo % 60)}')

    def buscar_musicas(self):
        # Verificando se tem arquivos inexistentes e removendo us
        diretorio = '/home'
        lista_caminho_musica = self.cursor.execute(
            'SELECT nome, caminho FROM dados').fetchall()
        for caminho_musica in lista_caminho_musica:
            caminho = caminho_musica[1]
            if not os.path.exists(caminho):
                self.cursor.execute(
                    'DELETE FROM dados WHERE caminho = ?', (caminho,))
                conexao.commit()
            else:
                self.playlist(caminho_musica[0])
        tempoAtualizarTela = 70

        # Busca por arquivos de música automaticamente
        filtros = ('.mp3', '.ogg')
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(raiz, arquivo)

                # Atualizar a tela
                if tempoAtualizarTela <= 0:
                    tempoAtualizarTela = 70
                    self.listaMusic.update()
                if any(filtro in arquivo for filtro in filtros):
                    self.cursor.execute('INSERT INTO dados VALUES(?, ?, ?)',(caminho_arquivo, arquivo.split(".")[0], self.converteTempo(
                        mixer.Sound(caminho_arquivo).get_length())))
                    conexao.commit()
                    self.playlist(arquivo.split(".")[0])

                tempoAtualizarTela -= 1
                 


App().mainloop()
