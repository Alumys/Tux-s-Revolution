import sys # No es tan necesario pero es una recomendacion para una mejor optimizacion del programa
import pygame

from modules.ventana import ANCHO_PANTALLA_P as ANCHO, LARGO_PANTALLA_P as ALTO # Dimensiones de la pantalla
from modules.ventana import ICONO, NOMBRE_JUEGO as NOMBRE # Visuales de la pantalla 
from modules.configs import FPS, RELOJ
from modules.menu import ejecutar_menu # Menu completo

pygame.init()

# Configuración de la ventana principal
ventana_principal = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(NOMBRE)
pygame.display.set_icon(ICONO)

# --- Definición de Estados del Juego ---
ESTADO_MENU = "MENU"
ESTADO_JUGAR = "JUGAR"
ESTADO_SALIR = "SALIR"

# --- Funciones de Estados ---

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

# --- Bucle Principal del Aplicación ---

def main():
    """
    Función principal de la aplicación. Inicializa Pygame y ejecuta el bucle
    de gestión de estados hasta que se alcanza el estado SALIR.
    
    """
    
    # La variable que controla en qué parte del juego estamos
    estado_actual = ESTADO_MENU 
    
    corriendo = True # Esta es tu bandera original del bucle principal
    while corriendo:
        
        if estado_actual == ESTADO_MENU:
            # Llamamos a la función que ejecuta el menú
            # Esta función PAUSA el bucle principal hasta que el menú devuelve un estado
            estado_actual = ejecutar_menu(ventana_principal, RELOJ)
            
            # Si el menú nos dice que salgamos, detenemos el bucle principal
            if estado_actual == ESTADO_SALIR:
                corriendo = False
                
        elif estado_actual == ESTADO_JUGAR:
            # Llamamos a la función que ejecuta la partida
            estado_actual = ejecutar_juego(ventana_principal, RELOJ)
            
            # Si el juego nos dice que salgamos, detenemos el bucle principal
            if estado_actual == ESTADO_SALIR:
                corriendo = False
            # Si el juego devuelve ESTADO_MENU, el bucle continuará y pasará al if ESTADO_MENU

        # Nota: Aquí no hay un pygame.display.update() global porque
        # cada función de estado (menu, juego) se encarga de su propia actualización.
        # Si tuvieras un estado de "Cargando" que quisiera dibujar algo diferente,
        # lo pondrías aquí o dentro de la función de ese estado.

    # --- Fin del Bucle Principal ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()