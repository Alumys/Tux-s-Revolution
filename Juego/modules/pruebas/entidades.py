import pygame

# FUNCIONES PRINCIPALES DE ENTIDADES # 

# Visualizador de entidades/seres # 
def dibujar_entidad(pantalla, imagen, rect):
    pantalla.blit(imagen, rect)