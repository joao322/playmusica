
import playsound
import customtkinter as ctk
import os

exetecaoMusica = ('.mp3', '.ogg')

# Configurando a janela
janela = ctk.CTk()
janela.geometry('1000x600')
janela.title('playsound')
janela.minsize(600, 400)

# Criando menu e configurando
menu = ctk.CTkFrame(janela, corner_radius=0, height=600)
menu.grid_anchor('e') # definido o menu fixado na esquerda 
menu.grid()



def buscador_musica(pasta):
    "buscar por todas as musica do diretorio "
    lista_musicas = []
    
    for raiz, *_, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            
            if any(exetecao in arquivo for exetecao in exetecaoMusica):
                lista_musicas.append(caminho_completo)
    
    lista_musicas.sort()
    return lista_musicas

# Iniciando a aplicasão            
class Playlist:
    def __init__(self):
        diretorio = '/home'
        playlist = buscador_musica(diretorio)  
        
        playsound.playsound(playlist[0])

if __name__ == '__main__':
    Playlist()
    janela.mainloop()
