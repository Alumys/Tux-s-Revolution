import pygame
from creacion_de_ladrillos.tamaño_ladrillo import ALTO_LADRILLO, ANCHO_LADRILLO, COLOR_LADRILLO


imagen_ladrillo = pygame.image.load("ladrillo.png").convert_alpha()
# Escalamos la imagen al tamaño definido para los ladrillos
IMAGEN_LADRILLO_ESCALADA = pygame.transform.scale(
    imagen_ladrillo, 
    (ANCHO_LADRILLO, ALTO_LADRILLO)
)