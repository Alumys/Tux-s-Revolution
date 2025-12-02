import pygame
# CONSTANTES # 

pygame.init()
# display/pantalla principal#
ANCHO_PANTALLA_P = 800
LARGO_PANTALLA_P = 600

# Icono #
ICONO = pygame.image.load('assets/images/icono_temprano.png')

# --- Definición de Estados del Juego --- #
ESTADO_MENU = "MENU"
ESTADO_JUGAR = "JUGAR"
ESTADO_SALIR = "SALIR"

# DIMENSIONES PROGRAMA ABIERTO #
ANCHO_PANTALLA_P = 800
LARGO_PANTALLA_P = 600

# ICONO Y NOMBRE DEL PROYECTO #
NOMBRE_JUEGO = "TUX'S REVOLUTION" 
ICONO = pygame.image.load('assets/images/icono_temprano.png') 

# CREACION DE VARIABLES PARA SU USO #
ventana_principal = pygame.display.set_mode((ANCHO_PANTALLA_P, LARGO_PANTALLA_P))

