import os # Importacion de SISTEMA OPERATIVO. Comprobacion de la existencia de archivos
import sys # No es tan necesario pero es una recomendacion para una mejor optimizacion del programa
import pygame # Importacion de la Biblioteca pygame


from modules.ventana import ventana_principal # "Lienzo"/Pantalla principal
from modules.ventana import ICONO, NOMBRE_JUEGO as NOMBRE # Visuales de la pantalla 
from modules.ventana import ANCHO_PANTALLA_P as ANCHO, LARGO_PANTALLA_P as ALTO # Dimensiones de la pantalla
from modules.configs import FPS, RELOJ # Configuraciones nucleo main
# MENU #
from modules.ventana import ESTADO_MENU, ESTADO_JUGAR, ESTADO_SALIR # Estados en el juego
from modules.menu import ejecutar_menu # Menu completo
# ENTIDADES #
from modules.entidades.entidades import dibujar_entidad # graficador de entidades
# paleta:
from modules.entidades.paleta import crear_paleta # creador de paletas
from modules.entidades.paleta import movimiento_paleta # movimiento de paleta
from modules.entidades.paleta import paleta_rect, paleta_img # Parametros de dibujado MOVIMIENTO / VISUAL
# pelota:
from modules.entidades.pelota import crear_pelota # creador de pelotas
from modules.entidades.pelota import tamano_pelota,POS_Y_PELOTA, POS_X_PELOTA # valores pelota
from modules.entidades.pelota import movimiento_pelota # movimiento de pelota

pygame.init()

# Configs. Ventana principal: (visual y nombre)
pygame.display.set_caption(NOMBRE)

pygame.display.set_icon(ICONO)

def ejecutar_juego(pantalla, reloj):
    """
    Bucle principal del estado JUGAR.
    Maneja paleta, pelota, movimiento y colisiones.
    """

    # ---- Crear entidades mutables ---- #
    pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota) 
    # @~LAU-NOTA:~
    # no se puede retirar porque sus elementos van mutando siempre # NO TOCAR # 
    # es posible moverlo, pero modularizarlo no... es complejo de momento

    jugando = True
    while jugando:
        reloj.tick(FPS)
        pantalla.fill((30, 80, 90))

        # ---- Eventos ----
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ESTADO_SALIR

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return ESTADO_MENU

        # MOVIMIENTOS ENTIDADES
        movimiento_paleta(paleta_rect) # @~LAU~ nota-PALETA: luego colocar un condicional para el RED HAT
        vel_x, vel_y = movimiento_pelota(pelota_rect, paleta_rect, vel_x, vel_y, ANCHO, ALTO) # @~LAU~ nota-PELOTA: luego colocar un condicional para wine

        # blitteo/dibujado
        dibujar_entidad(pantalla, paleta_img, paleta_rect)
        dibujar_entidad(pantalla, pelota_img, pelota_rect)

        pygame.display.flip()

    return ESTADO_SALIR

def main()->None:
    """
    Inicializa Pygame y ejecuta el bucle 
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