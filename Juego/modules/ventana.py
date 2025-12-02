import pygame

# --- Definición de Estados del Juego --- #
ESTADO_MENU = "MENU"
ESTADO_JUGAR = "JUGAR"
ESTADO_SALIR = "SALIR"

# DIMENSIONES PROGRAMA ABIERTO #
ANCHO_PANTALLA_P = 800
LARGO_PANTALLA_P = 600

# ICONO Y NOMBRE DEL PROYECTO #
NOMBRE_JUEGO = "TUX'S REVOLUTION" 
ICONO = pygame.image.load('assets/images/iconos/icono_revolucion.png') 

# CREACION DE VARIABLES PARA SU USO #
ventana_principal = pygame.display.set_mode((ANCHO_PANTALLA_P, LARGO_PANTALLA_P))

# IMAGEN DE FONDO 
FONDO_JUEGO = pygame.image.load('assets/images/fondos/fondo_juego.png').convert()
FONDO_JUEGO = pygame.transform.scale(FONDO_JUEGO, (800, 600))