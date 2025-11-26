import pygame
import os
# --------------------------------------------------------------
# FUNCIONES DE CREACIÓN
# --------------------------------------------------------------

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


def crear_pelota(x, y, tamano, color=(255, 255, 255), velocidad_x=5, velocidad_y=-5):
    ruta_imagen = "imagenes/terminal.png"
    pelota_rect = pygame.Rect(x, y, tamano, tamano)  # Rect colisiones

    # Visual/Frontend
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (tamano, tamano))
    else:
        imagen = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        pygame.draw.circle(imagen, color, (tamano // 2, tamano // 2), tamano // 2)

    return pelota_rect, imagen, velocidad_x, velocidad_y

# --------------------------------------------------------------
# FUNCIONES DE MOVIMIENTO
# --------------------------------------------------------------

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


# --------------------------------------------------------------
# INICIALIZACIÓN
# --------------------------------------------------------------

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout - Demo de Paleta y Pelota")

clock = pygame.time.Clock()

# Crear paleta y pelota
paleta_rect, paleta_img = crear_paleta(350, 500, 120, 20, color=(0, 255, 0))
pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(350, 450, 40)


# --------------------------------------------------------------
# GAME LOOP
# --------------------------------------------------------------

running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento paleta
    movimiento_personaje(paleta_rect, velocidad=6, limite_der=ANCHO)

    # Movimiento pelota
    vel_x, vel_y = movimiento_pelota(
        pelota_rect,
        paleta_rect,
        vel_x,
        vel_y,
        ANCHO,
        ALTO
    )

    # ----------------------------------------------------------
    # DIBUJADO
    # ----------------------------------------------------------

    pantalla.fill((0, 0, 0))

    dibujar_entidad(pantalla, paleta_img, paleta_rect)
    dibujar_entidad(pantalla, pelota_img, pelota_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
