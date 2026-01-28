import pygame


pygame.font.init()

# --- Definición de Estados del Juego --- #
ESTADO_MENU = "MENU"
ESTADO_JUGAR = "JUGAR"
ESTADO_SALIR = "SALIR"
ESTADO_PUNTOS = "PUNTOS"
ESTADO_AUDIO = "AUDIO"
ESTADO_CREDITOS="CREDITOS"
# DIMENSIONES PROGRAMA ABIERTO #
ANCHO_PANTALLA_P = 800
LARGO_PANTALLA_P = 600

# CREACION DE VARIABLES PARA SU USO #
ventana_principal = pygame.display.set_mode((ANCHO_PANTALLA_P, LARGO_PANTALLA_P))


# ICONO Y NOMBRE DEL PROYECTO #
NOMBRE_JUEGO = "TUX'S REVOLUTION" 
ICONO = pygame.image.load('assets/images/iconos/icono_revolucion.png') 

# LOGO DEL TITULO
TITULO_JUEGO = pygame.image.load('assets/images/titulos/titulo_juego.png').convert_alpha()
TITULO_JUEGO = pygame.transform.scale(TITULO_JUEGO, (550, 250))

# IMAGEN DE FONDO JUEGO
FONDO_JUEGO = pygame.image.load('assets/images/fondos/fondo_juego.png').convert()
FONDO_JUEGO = pygame.transform.scale(FONDO_JUEGO, (800, 600))

# IMAGEN DE FONDO MENU
FONDO_MENU = pygame.image.load('assets/images/fondos/fondo_menu.png').convert()
FONDO_MENU = pygame.transform.scale(FONDO_JUEGO, (800, 600))

# OPCIONES del menu principal
BOTON_OPCION = pygame.image.load('assets/images/opciones/cuadro_opcion.png').convert_alpha()
BOTON_OPCION = pygame.transform.scale(BOTON_OPCION, (300, 200))
BOTON_SELECCION = pygame.image.load('assets/images/opciones/cuadro_seleccion.png').convert_alpha()
BOTON_SELECCION = pygame.transform.scale(BOTON_SELECCION, (300, 200))

# FUENTE
FUENTE_GENERAL = pygame.font.Font("assets/fonts/CARTNIST.TTF", 32)

