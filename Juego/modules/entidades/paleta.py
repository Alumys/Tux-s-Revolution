import os
import pygame

from ..ventana import LARGO_PANTALLA_P, ANCHO_PANTALLA_P

# ! Configurar definiendo los valores de las variables/constantes !#
# Configuracion de movimiento #
velocidades_xx = 6

# colisiones/limites
LIMIT_IZQUIERDA = 0 # comienzo de la pantalla X
LIMIT_DERECHA = ANCHO_PANTALLA_P# fin de la pantalla derecha X

# posicionamiento 
POS_X_PALETA = ANCHO_PANTALLA_P - 450 # Se le suma mas de la mitad porque sino hay problemas de posicionamiento y volumen
POS_Y_PALETA = LARGO_PANTALLA_P - 100

# dimensiones
# nota: posiblemente despues se puedan hacer mas power ups con las dimensiones de la paleta :D
ancho_paleta = 120
alto_paleta = 20

ancho_imagen = 120

# Funcion crear paleta 
def crear_paleta(x, y, ancho, alto, color=(255, 255, 255)):
    ruta_imagen = "assets/images/pj_jugables/paleta_tux.png"
    paleta_rect = pygame.Rect(x, y, ancho, alto)  # Rect para colisiones
    alto_pj = 120  # Alto visual de la imagen
    ancho_pj = 150
    # Visual/Frontend
    if os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (ancho_pj, alto_pj))  # Escalado
    else:
        imagen = pygame.Surface((ancho, alto))
        imagen.fill(color)

    return paleta_rect, imagen


# Funcion Movimiento de Paleta 

def movimiento_paleta(paleta_rect, velocidad=velocidades_xx, limite_izq=LIMIT_IZQUIERDA, limite_der=LIMIT_DERECHA):
    """ Mueve la paleta según las teclas presionadas. """
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] and paleta_rect.left > limite_izq:
        paleta_rect.x -= velocidad
    if teclas[pygame.K_RIGHT] and paleta_rect.right < limite_der:
        paleta_rect.x += velocidad

# VARIABLES/VALORES A COMUNICAR CON MAIN.PY 
# valores rect para funcionamiento y surface/imagen para lo visual
paleta_rect, paleta_img = crear_paleta(POS_X_PALETA,POS_Y_PALETA, ancho_paleta, alto_paleta) 