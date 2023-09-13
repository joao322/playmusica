import eyed3
import playsound

def reproduzirMusica(raquivo):
    playsound.

def capaMusica(arquivo) -> 'img':
    audio = eyed3.load(arquivo)
    if audio.tag:
        capas = audio.tag.images
        return capas
    
def duracaoMusica(arquivo) -> str:
    audio = eyed3.load(arquivo)

    duracaoSegundos = audio.info.time_secs
    duracaoMinutos = int(duracaoSegundos / 60)
    segundosRestantaes = int(duracaoSegundos % 60)
    
    return f'{duracaoMinutos}:{segundosRestantaes}'