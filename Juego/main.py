import pygame

from assets.modules.ventana import ANCHO_PANTALLA_P as ANCHO
from assets.modules.ventana import LARGO_PANTALLA_P as LARGO

pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")

corriendo = True # bandera de bucle principal
while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        pygame.display.update() # Actualizador de pantalla

pygame.quit()
