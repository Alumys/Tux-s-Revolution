
# Función para iniciar la música de la partida
#def iniciar_musica_juego(ruta_musica="C:/juego/Tux-s-Revolution/Juego/assets/sounds/sonido_juego.mp3", volumen=1.0):
"""
#   # Detiene cualquier música anterior y reproduce la música de la partida en loop.
    """
 #   pygame.mixer.music.stop()  # Detiene música anterior
  #  pygame.mixer.music.load(ruta_musica)
   # pygame.mixer.music.set_volume(volumen)
    #pygame.mixer.music.play(-1)  # Loop infinito

import pygame
import os

# Rutas fijas dentro del módulo
RUTA_VOZ_INICIO = "C:/juego/Tux-s-Revolution/Juego/assets/sounds/comienzo.mp3"
RUTA_MUSICA_JUEGO = "C:/juego/Tux-s-Revolution/Juego/assets/sounds/loop_juego.mp3"

def iniciar_sonidos_juego(esperar_inicio=True, volumen_inicio=1.0, volumen_musica=1.0):
    """
    Reproduce la voz de inicio y luego la música de fondo en loop.
    """
    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    # Voz de inicio
    if os.path.exists(RUTA_VOZ_INICIO):
        sonido_inicio = pygame.mixer.Sound(RUTA_VOZ_INICIO)
        sonido_inicio.set_volume(volumen_inicio)
        sonido_inicio.play()
        if esperar_inicio:
            duracion = int(sonido_inicio.get_length() * 1000)
            pygame.time.delay(duracion)
    else:
        print(f"⚠️ Audio de inicio no encontrado: {RUTA_VOZ_INICIO}")

    # Música del juego en loop
    if os.path.exists(RUTA_MUSICA_JUEGO):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(RUTA_MUSICA_JUEGO)
        pygame.mixer.music.set_volume(volumen_musica)
        pygame.mixer.music.play(-1)
    else:
        print(f"⚠️ Música de juego no encontrada: {RUTA_MUSICA_JUEGO}")


def sonido_victoria(volumen=1.0):
    """Reproduce un sonido cuando el jugador gana."""
    sonido_win = pygame.mixer.Sound("C:/juego/Tux-s-Revolution/Juego/assets/sounds/victoria.mp3")
    sonido_win.set_volume(1.0)
    sonido_win.play(0) #0=suena una sola vez