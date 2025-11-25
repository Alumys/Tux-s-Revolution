import os
import pygame

# ---------------------------------------------------------------
# FUNCION: crear_paleta
# Crea la paleta del jugador.
#
# - Si existe "assets/paleta.png" → usa esa imagen.
# - Si NO existe → crea un rectángulo del color indicado.
#
# Retorna:
# - rect   → posición y colisión
# - imagen → superficie ya lista para dibujar
# ---------------------------------------------------------------
def crear_paleta(x, y, ancho, alto, color=(255, 255, 255)):
    # Definir ruta de la imagen por defecto
    ruta_imagen = "assets/pj_jugables" 

    # Crear rectángulo base que controla posición y colisiones
    paleta_rect = pygame.Rect(x, y, ancho, alto)

    # Verificar si la imagen existe realmente en el disco
    if os.path.exists(ruta_imagen):
        # Cargar imagen real de la paleta
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        # Ajustar la imagen al tamaño pedido
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    else:
        # Si la imagen no existe, se crea un rectángulo color sólido
        imagen = pygame.Surface((ancho, alto))
        imagen.fill(color)

    return paleta_rect, imagen





# ---------------------------------------------------------------
# FUNCION: crear_pelota
# Crea la pelota del juego.
#
# - Si existe "assets/pelota.png" → usa esa imagen.
# - Si NO existe → se dibuja un círculo blanco o del color elegido.
#
# Retorna:
# - rect
# - imagen
# - velocidad_x
# - velocidad_y
# ---------------------------------------------------------------
def crear_pelota(x, y, tamano, color=(255, 255, 255), velocidad_x=5, velocidad_y=-5):
    ruta_imagen = "assets/images/pj_jugables/pelotas"

    # Rectángulo que usa la pelota para moverse y colisionar
    pelota_rect = pygame.Rect(x, y, tamano, tamano)

    # Si existe la imagen de pelota
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (tamano, tamano))
    else:
        # Creamos un cuadrado transparente con un círculo dentro
        imagen = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        pygame.draw.circle(imagen, color, (tamano // 2, tamano // 2), tamano // 2)

    return pelota_rect, imagen, velocidad_x, velocidad_y









# ---------------------------------------------------------------
# FUNCION: dibujar_entidad
# Dibuja cualquier entidad que tenga rect + imagen
# General para cualquier objeto del juego.
# ---------------------------------------------------------------
def dibujar_entidad(pantalla, imagen, rect): # utilidad general
    pantalla.blit(imagen, rect)



















## Creacion de personaje y ##

personaje_rect, personaje_imagen = crear_paleta(350, 550, 120, 20, color=(0, 255, 0)) # Creacion del personaje (rect e surface/imagen)