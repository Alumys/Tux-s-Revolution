import pygame
import os

# --------------------------------------------------------------
# FUNCIONES DE CREACIÓN
# --------------------------------------------------------------

def crear_paleta(x, y, ancho, alto, color=(255, 255, 255)):
    ruta_imagen = "imagenes/tux.png"
    paleta_rect = pygame.Rect(x, y, ancho, alto) # Colisiones de la paleta (backend)
    alto_pj = 100 # Modificar esto para que quede mejor el pj en imagen
    
    # (Visual/Frontend)
    if os.path.exists(ruta_imagen): 
        imagen = pygame.image.load(ruta_imagen).convert_alpha() # Cargar imagen 
        imagen = pygame.transform.scale(imagen, (ancho, alto_pj)) # escalado del PJ para ponerlo con rect despues
    else: # Si no esta la ruta
        imagen = pygame.Surface((ancho, alto))
        imagen.fill(color)

    return paleta_rect, imagen


def crear_pelota(x, y, tamano, color=(255, 255, 255), velocidad_x=5, velocidad_y=-5):
    ruta_imagen = "imagenes/terminal.png"
    pelota_rect = pygame.Rect(x, y, tamano, tamano) # Colisiones de la pelota (backend)

    # (Visual/Frontend)
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (tamano, tamano))
    else:# si no esta la ruta
        imagen = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        pygame.draw.circle(imagen, color, (tamano // 2, tamano // 2), tamano // 2)

    return pelota_rect, imagen, velocidad_x, velocidad_y


def dibujar_entidad(pantalla, imagen, rect):
    pantalla.blit(imagen, rect)


# --------------------------------------------------------------
# INICIALIZACIÓN
# --------------------------------------------------------------

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout - Demo de Paleta y Pelota")

clock = pygame.time.Clock()

# Crear paleta y pelota usando tus funciones
paleta_rect, paleta_img = crear_paleta(350, 500, 120, 20, color=(0, 255, 0))
pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(390, 300, 60)


# --------------------------------------------------------------
# GAME LOOP
# --------------------------------------------------------------

running = True
while running:
    # ----- Eventos -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- Movimiento de la paleta -----
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        paleta_rect.x -= 6
    if teclas[pygame.K_RIGHT]:
        paleta_rect.x += 6

    # Mantener la paleta dentro de pantalla
    if paleta_rect.left < 0:
        paleta_rect.left = 0
    if paleta_rect.right > ANCHO:
        paleta_rect.right = ANCHO

    # ----- Movimiento de la pelota -----
    pelota_rect.x += vel_x
    pelota_rect.y += vel_y

    # Rebotes en bordes
    if pelota_rect.left <= 0 or pelota_rect.right >= ANCHO:
        vel_x *= -1
    if pelota_rect.top <= 0:
        vel_y *= -1

    # Rebote con paleta
    if pelota_rect.colliderect(paleta_rect):
        vel_y *= -1

    # ----- Dibujado -----
    pantalla.fill((0, 0, 0))  # Fondo negro

    dibujar_entidad(pantalla, paleta_img, paleta_rect)
    dibujar_entidad(pantalla, pelota_img, pelota_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
