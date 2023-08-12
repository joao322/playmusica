import sqlite3
import playsound
import customtkinter as ctk
import os

filtro = ('.mp3', '.ogg')
janela_size = {'x': 100, 'y': 600}

# Configurando a janela
janela = ctk.CTk()
janela.geometry('1000x600')
janela.title('playsound')
janela.minsize(600, 400)
try:
    conexao = sqlite3.connect('dados/banco-dados.db') 

except sqlite3.OperationalError:
    os.makedirs('dados')
    conexao = sqlite3.connect('dados/banco-dados.db')
    curso = conexao.cursor()
    curso.execute("CREATE TABLE dado(caminho_musica Text)")

# Iniciando a aplicasão    
class App:
    def __init__(self) -> None:
        global scroll
        ctk.CTkButton(janela, text='arquivos', command=self.menuBurg ,width=30, height=20).place(x=0, y=0)
        scroll = ctk.CTkScrollableFrame(janela, 180, janela_size['y'] - 30)
        scroll.place(x=0,y=24)
        

        if curso.execute("SELECT * FROM dados").fetchall() != []:
        janela.after(10, self.update)      
        janela.after(10, self.buscar)
        janela.mainloop()
        
    def buscar(self):
        "buscar por todas as musica do diretorio"
        
        diretorio = '/home'
        notificasao = ctk.CTkLabel(janela, text='o sistema ficara mais lento e quanto buscar por arquivos...')
        notificasao.place(x=60, y=0)
        for raiz, *_, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                # Filtrando os arquivos 
                if any(exetecao in arquivo for exetecao in filtro) and curso.execute("SELECT * FROM dados WHERE caminho_musica = ?", caminho_completo) == []:
                    ctk.CTkButton(scroll, text=arquivo, width=175).pack(pady=2, ipadx=10)
                    curso.execute("INSERT INTO dados VALUES(caminho_musica = ?)", caminho_completo)
                    conexao.commit()
                    scroll.update()
                    
                    
        notificasao.place_forget()
    def update(self):
        if janela_size['y'] != janela.winfo_height():             
            janela_size['y'] = janela.winfo_height()
            scroll.configure(height=janela_size['y'] -30) 
        janela.after(1, self.update)
        
    def fechar_MenuBurg(self, evento):
        largura = burg.winfo_width() + burg.winfo_x()
        altura = burg.winfo_height() + burg.winfo_y()
        if largura < evento.x or altura < evento.y:
            janela.unbind('<Button-1>')
            burg.place_forget()

    def menuBurg(self):
        global burg
        janela.bind('<Button-1>', self.fechar_MenuBurg)
        try: 
            burg.update()
        except NameError:
            burg = ctk.CTkFrame(janela)
            ctk.CTkButton(burg, 200, text='buscar manualmente').pack(pady=2, ipadx=10)
            ctk.CTkButton(burg, 200, text='musicas exicluidas').pack(pady=2, ipadx=10)
            ctk.CTkButton(burg, 200, text='buscar automaticamente', command=self.buscar).pack(pady=2, ipadx=10)
        else:
            burg.place_forget()

        burg.place(x=0, y=20)
        

if __name__ == '__main__':
    App()
    janela.mainloop()
