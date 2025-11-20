import pygame

# Funciones PRINCIPALES #

# --- Bucle de Juego --- #
def ejecutar_juego(pantalla, reloj):
    """
    Función que gestiona el bucle de la partida (estado JUGAR).
    Aquí se debe implementar toda la lógica de juego: movimientos, colisiones, etc.

    pantalla: Superficie de Pygame para el dibujado.
    reloj: Objeto pygame.time.Clock para control de FPS.
    return: string con el estado de salida ("MENU" si se pulsa ESC, "SALIR" si se cierra la ventana).
    
    """
    
    # Ejemplo de un bucle de juego simple
    jugando = True
    while jugando:
        reloj.tick(FPS)
        pantalla.fill((30, 80, 30)) # Un fondo de color diferente para el juego
        
        # --- Lógica del juego aca (movimiento de personaje, enemigos, etc.) ---
        # Por ejemplo, podemos tener una función dibujar_personaje(pantalla) en otro módulo.
        
        # --- Manejo de Eventos del Juego ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ESTADO_SALIR # Si cierran la ventana, salimos del juego
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: # Si presionan ESC, volvemos al menú
                    return ESTADO_MENU
            # Otros eventos del juego (movimiento, disparos, etc.)
            
        pygame.display.flip()
        
    return ESTADO_SALIR # Si el bucle del juego termina por alguna otra razón