import pygame

def dibujar_vidas(pantalla, vidas_restantes, fuente):
    """
    Dibuja el contador de vidas en la esquina superior izquierda.
    """
    # Color Rojo para que resalte
    ROJO = (255, 50, 50)
    
    # Renderizar texto
    texto_vidas = fuente.render(f"VIDAS: {vidas_restantes}", True, ROJO)
    
    # Dibujar en pantalla (x=10, y=10)
    pantalla.blit(texto_vidas, (10, 10))