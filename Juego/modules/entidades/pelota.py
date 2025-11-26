import os
import pygame

from ..ventana import LARGO_PANTALLA_P
# FUNCIONES PRINCIPALES DE LA PELOTA #

# Configuracion #
velocidades_xx = 5
velocidades_yy = 5
colores = ()
# Configuracion Wine/Vino#
velocidad_wine_xx = 5
velocidad_wine_yy = 5
colores = ()
# Funcion crear pelota 
def crear_pelota(x, y, tamano, color=(255, 255, 255), velocidad_x=velocidades_xx, velocidad_y=-velocidades_yy):
    ruta_imagen = "assets/images/pelotas/prueba_pelota.png"
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

pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(350, LARGO_PANTALLA_P - 140, 40) # Pelota ORIGINAL

#LUEGO CREAR LA VERSION WINE#