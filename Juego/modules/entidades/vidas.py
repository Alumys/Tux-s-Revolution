import pygame
from modules.ventana import ventana_principal
sonido_perder_vida=None
sonido_game_over=None
corazon_ima=pygame.image.load("C:/juego/Tux-s-Revolution/Juego/assets/images/corazon.png")
corazon_ima = pygame.transform.scale(corazon_ima, (35, 35))

VIDAS = 3
def cargar_sonidos():
    global sonido_perder_vida
    sonido_perder_vida = pygame.mixer.Sound(
        "C:/juego/Tux-s-Revolution/Juego/assets/sounds/perder_vida.wav"
    )
    sonido_perder_vida.set_volume(0.7)
    sonido_game_over=pygame.mixer.Sound("C:/juego/Tux-s-Revolution/Juego/assets/sounds/perder.wva.wav")
    sonido_game_over.set_volume(0.8)


def dibujar_vidas(VIDAS:int):
    for i in range(VIDAS):
        ventana_principal.blit(corazon_ima, (10 + i * 40, 10))

def perder_vida(VIDAS: int) -> tuple[int, bool]:
    VIDAS -= 1
    if sonido_perder_vida:
        sonido_perder_vida.play()
    if VIDAS <= 0:
        if sonido_game_over:
            sonido_game_over.play()
            pygame.time.delay(800)
        print("game over")
        
        return VIDAS, True
    return VIDAS, False