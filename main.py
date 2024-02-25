import customtkinter as ctk
from pygame.mixer import init, Sound, music
from PIL import Image
import buscador

# init mixer
init()


class Root(ctk.CTk):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)

        # Variaves
        self.linha = None
        self.listaMusicas = None
        self.telaAnterior = None
        self.telaAtual = ctk.CTkFrame(self)
        self.imgHome = ctk.CTkImage(Image.open('uix/home.png'))
        self.imgMusica = ctk.CTkImage(Image.open('uix/musica.png'))
        self.imgPasta = ctk.CTkImage(Image.open('uix/pasta.png'))
        self.imgConfiguaracao = ctk.CTkImage(Image.open('uix/configuracao.png'))

        # Configuaracao da janela
        self.title('MidiaPlay')
        self.minsize(600, 300)
        self.configure(bg_color='#101010', fg_color='#101010')
        self.bind('<Configure>', self.redimensionar)

        # Crinado o menu dock
        self.menuDock = ctk.CTkFrame(
            self, 40, 300, corner_radius=0, fg_color='#13052b')
        self.menuDock.place(x=0, y=0)
        ctk.CTkButton(self.menuDock, text='', image=self.imgHome, width=28,
                      fg_color='transparent', command=lambda: self.mudaLinha_Tela(posy=0, tela='home')).pack()
        ctk.CTkButton(self.menuDock, text='', image=self.imgMusica, width=28,
                      fg_color='transparent', command=lambda: self.mudaLinha_Tela(posy=28, tela='musica')).pack()
        ctk.CTkButton(self.menuDock, text='', image=self.imgPasta, width=28,
                      fg_color='transparent', command=lambda: self.mudaLinha_Tela(posy=56)).pack()

        self.espacoMenu = ctk.CTkLabel(self.menuDock, text='')
        self.espacoMenu.pack()
        
        self.mudaLinha_Tela()

        ctk.CTkButton(self.menuDock, text='',  width=28,
                      image=self.imgConfiguaracao, fg_color='transparent').pack()

        self.listaMusicas = buscador.buscador('/home', ('.mp3', '.ogg'))

    def redimensionar(self, event=None):
        altura = self.winfo_height()
        largura = self.winfo_width()
        
        self.espacoMenu.configure(height=altura - 115)
        self.telaAtual.configure(width=largura - 40, height=altura)

    def mudaLinha_Tela(self, posy=0, tela='home'):

        if self.linha:
            self.linha.destroy()
        self.linha = ctk.CTkLabel(self.menuDock, fg_color='red', text='')
        self.linha.place(x=2, y=posy)

        match tela:
            case self.telaAnterior:
                return
            case 'home':
                self.telaAtual.destroy()
                self.telaHome(init=True)
                
            case 'musica':
                self.telaAtual.destroy()
                self.telaHome(init=True)
        self.telaAnterior = tela    
        
    def telaHome(self, init=False): 
        if init:
            altura = self.winfo_height()
            largura = self.winfo_width()
            self.telaAtual = ctk.CTkFrame(self, largura, altura, fg_color='transparent')
            self.telaAtual.place(x=33,y=0)
            #self.telaAtual.bind('<Configure>', self.tela1)
            telaPlaylist = ctk.CTkScrollableFrame(self.telaAtual,largura, altura, fg_color='transparent', corner_radius=0)
            telaPlaylist.place(x=0,y=2)
            
            if self.listaMusicas:
                for musica in self.listaMusicas:
                    ctk.CTkButton(telaPlaylist,text=musica[0], fg_color='#101010',anchor='w', image=self.imgPasta).pack()
                    ctk.CTkLabel(telaPlaylist, fg_color='#53396b', height=0, width=100, text='',font=("arial", 1)).pack()
            
            
if __name__ == "__main__":
    Root().mainloop()
