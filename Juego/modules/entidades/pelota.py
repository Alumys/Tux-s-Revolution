import os
import pygame

from ..ventana import LARGO_PANTALLA_P

# ! Configurar definiendo los valores de las variables/constantes !#
# velocidad de movimiento #
velocidades_xx = 5
velocidades_yy = 5
colores = ()

# posicionamiento
POS_X_PELOTA = 350 
POS_Y_PELOTA = LARGO_PANTALLA_P - 160

# dimensiones 
tamano_pelota = 50  
# @~Lau nota:~
# Configuracion Wine/Vino:
# Luego colocar el codigo despues, ya sea rama_araceli/rama_lauta

# Funcion crear pelota 
def crear_pelota(x, y, tamano, color=(255, 255, 255), velocidad_x=velocidades_xx, velocidad_y=-velocidades_yy):
    ruta_imagen = "assets/images/pelotas/terminal.png"
    pelota_rect = pygame.Rect(x, y, tamano, tamano)  # Rect colisiones

    # Visual/Frontend
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (tamano, tamano))
    else:
        imagen = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        pygame.draw.circle(imagen, color, (tamano // 2, tamano // 2), tamano // 2)

    return pelota_rect, imagen, velocidad_x, velocidad_y


# Funcion Movimiento de Pelota 

def movimiento_pelota(pelota_rect, paleta_rect, vel_x, vel_y, ancho, alto):
    """ Mueve la pelota y maneja todas las colisiones. """

    # --- Movimiento ---
    pelota_rect.x += vel_x
    pelota_rect.y += vel_y

    # --- Colisiones laterales ---
    if pelota_rect.left <= 0 or pelota_rect.right >= ancho:
        vel_x *= -1

    # --- Colisión arriba ---
    if pelota_rect.top <= 0:
        vel_y *= -1

    # --- Colisión con paleta ---
    if pelota_rect.colliderect(paleta_rect):
        vel_y *= -1

    return vel_x, vel_y

#LUEGO CREAR LA VERSION WINE#
