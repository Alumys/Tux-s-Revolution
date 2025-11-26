import os
import pygame

from ..ventana import LARGO_PANTALLA_P, ANCHO_PANTALLA_P
# FUNCIONES PRINCIPALES DE LA PALETA #

# Configuracion de la paleta #
velocidades_xx = 6

# colisiones/limites
limit_izquierda = 0 # comienzo de la pantalla X
limit_derecha = ANCHO_PANTALLA_P# fin de la pantalla derecha X



# Funcion crear paleta 
def crear_paleta(x, y, ancho, alto, color=(255, 255, 255)):
    ruta_imagen = "assets/images/pj_jugables/prueba_personaje.png"
    paleta_rect = pygame.Rect(x, y, ancho, alto)  # Rect para colisiones
    alto_pj = 100  # Alto visual de la imagen

    # Visual/Frontend
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (ancho, alto_pj))  # Escalado
    else:
        imagen = pygame.Surface((ancho, alto))
        imagen.fill(color)

    return paleta_rect, imagen


# Funcion Movimiento de Paleta 

def movimiento_paleta(paleta_rect, velocidad=velocidades_xx, limite_izq=limit_izquierda, limite_der=limit_derecha):
    """ Mueve la paleta según las teclas presionadas. """
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] and paleta_rect.left > limite_izq:
        paleta_rect.x -= velocidad
    if teclas[pygame.K_RIGHT] and paleta_rect.right < limite_der:
        paleta_rect.x += velocidad

paleta_rect, paleta_img = crear_paleta(350, LARGO_PANTALLA_P - 100, 120, 20)