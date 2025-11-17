import pygame

from modules.ventana import ANCHO_PANTALLA_P as ANCHO
from modules.ventana import LARGO_PANTALLA_P as LARGO
from modules.ventana import ICONO

pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")
pygame.display.set_icon(ICONO)

corriendo = True # bandera de bucle principal
while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        pygame.display.update() # Actualizador de pantalla

pygame.quit()
