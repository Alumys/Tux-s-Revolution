import os
import pygame

# FUNCIONES PRINCIPALES DE LA PALETA #

# Funcion crear paleta 
def crear_paleta(x, y, ancho, alto, color=(255, 255, 255)):
    ruta_imagen = "imagenes/tux.png"
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


