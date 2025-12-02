import pygame
from modules.ventana import ventana_principal 

corazon_imagen= pygame.image.load("c:/Users/dario/Downloads/corazon.png")

corazon_imagen=pygame.transform.scale(corazon_imagen, (35, 35))

VIDAS= 3 # comenzamos con 3 vidas 


#funcion para mostrar los corazones
def mostrar_corazones():
    for i in range(VIDAS):
         ventana_principal.blit(corazon_imagen, (10 + i * 40, 10)) #separa los corazones por 40 pixeles 
                                                                # 10 es la posision x del primer corazon 

mostrar_corazones