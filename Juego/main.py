import os # Importacion de SISTEMA OPERATIVO. Comprobacion de la existencia de archivos
import sys # No es tan necesario pero es una recomendacion para una mejor optimizacion del programa
import pygame # Importacion de la Biblioteca pygame

from modules.ventana import ventana_principal # "Lienzo"/Pantalla principal
from modules.ventana import ICONO, NOMBRE_JUEGO as NOMBRE, FONDO_JUEGO # Visuales de la pantalla 
from modules.ventana import ANCHO_PANTALLA_P as ANCHO, LARGO_PANTALLA_P as ALTO # Dimensiones de la pantalla
from modules.configs import FPS, RELOJ # Configuraciones nucleo main
# MENU #
from modules.ventana import ESTADO_MENU, ESTADO_JUGAR, ESTADO_SALIR, ESTADO_PUNTOS, ESTADO_AUDIO,ESTADO_CREDITOS,FUENTE_GENERAL# Estados en el juego
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

# Ladrillos:

from modules.entidades.ladrillos import crear_ladrillos, dibujar_ladrillos, colisionar_con_ladrillos

# agregando la importacion para sl sistema de puntos
from modules.fin_juego import ejecutar_pantalla_fin
# pantalla del puntaje
from modules.pantalla_ranking import ejecutar_ranking
#sonido
from modules.sonido import ejecutar_sonidos
from modules.cronometro import actualizar_cronometro,dibujar_cronometro,se_acabo
#vidas
from modules.entidades.vidas import dibujar_vidas, perder_vida
#creditos
from modules.credi import ejecutar_creditos
#sonidos 
from modules.entidades.ladrillos import cargar_sonidos_ladrillos
from modules.entidades.vidas import cargar_sonidos,sonido_game_over
from modules.mus_princi import iniciar_sonidos_juego
pygame.init()
pygame.font.init()
pygame.mixer.init()
# Configs. Ventana principal: (visual y nombre)
pygame.display.set_caption(NOMBRE)
pygame.display.set_icon(ICONO)
#llamados de sonidos
sonido_ladri=cargar_sonidos_ladrillos()
cargar_sonidos()
def ejecutar_juego(pantalla, reloj):
    """
    Bucle principal del estado JUGAR.
    Maneja paleta, pelota, movimiento y colisiones.
    """
    iniciar_sonidos_juego(True,volumen_inicio=1.0,volumen_musica=0.4)
    # ---- Crear entidades mutables ---- #
    VIDAS=3 
    perdediendo_vida=False
    pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota) 
    ladrillos = crear_ladrillos(ANCHO)
    tiempo_restante=90
    fuente_cronometro=pygame.font.SysFont("arial" ,35, bold= True)
    # @~LAU-NOTA:~
    # no se puede retirar porque sus elementos van mutando siempre # NO TOCAR # 
    # es posible moverlo, pero modularizarlo no... es complejo de momento
    # --- LADRILLOS ---
    
    #Variable del puntajegi
    puntaje_actual = 0
    #fuente para el puntaje:
    fuente_hud = pygame.font.SysFont("Arial", 30, bold=True)
    
    jugando = True
    while jugando:
        reloj.tick(FPS)
        pantalla.blit(FONDO_JUEGO, (0, 0))

        # ---- Eventos ----
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ESTADO_SALIR

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return ESTADO_MENU
                #TRUCO TECLA K
                if evento.key == pygame.K_k:
                    ladrillos.clear()

        # 1) movimiento de entidades
        movimiento_paleta(paleta_rect)
        vel_x, vel_y = movimiento_pelota(pelota_rect, paleta_rect, vel_x, vel_y, ANCHO, ALTO)
        if pelota_rect.top > ALTO and not perdediendo_vida:
            perdediendo_vida=True
            VIDAS, game_over = perder_vida(VIDAS)
            pelota_rect.center = (POS_X_PELOTA, POS_Y_PELOTA)
            vel_y = -abs(vel_y)

            if game_over:
                if sonido_game_over:
                    sonido_game_over.play()
                return ejecutar_pantalla_fin(pantalla, reloj, puntaje_actual, False)
        if pelota_rect.top <= ALTO:
            perdediendo_vida= False
        # 2) colisión pelota <-> ladrillos (ahora recibe drops/objetos), y puntaje
        vel_y, puntos_nuevos = colisionar_con_ladrillos(pelota_rect, vel_y, ladrillos,sonido_ladri)
        puntaje_actual += puntos_nuevos
        
        print(f"Ladrillos restantes: {len(ladrillos)}")
        if len(ladrillos) == 10:
            print("VICTORIA DETECTADA")
            return ejecutar_pantalla_fin(pantalla,reloj, puntaje_actual, True)
        
        
        


        # 4) dibujado entidades y ladrillos
        dibujar_entidad(pantalla, paleta_img, paleta_rect)
        dibujar_entidad(pantalla, pelota_img, pelota_rect)
        dibujar_ladrillos(pantalla, ladrillos)
        dibujar_vidas(VIDAS)
        dibujar_cronometro(pantalla,fuente_cronometro,tiempo_restante,posicion=(20, ALTO-50))
        #dibujando puntaje
        texto_superficie = fuente_hud.render(f"PUNTOS: {puntaje_actual}", True, (255, 255, 255))
        
        # Lo ubicamos a la derecha (Ancho pantalla - Ancho texto - Margen)
        pos_x = pantalla.get_width() - texto_superficie.get_width() - 20
        pos_y = 450 # Un poco separado del techo
        
        pantalla.blit(texto_superficie, (pos_x, pos_y))
        dt= 1/FPS
        tiempo_restante=actualizar_cronometro(tiempo_restante, dt)
        if se_acabo(tiempo_restante):
            return ejecutar_pantalla_fin(pantalla,RELOJ,puntaje_actual,False)
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
        
        elif estado_actual == ESTADO_PUNTOS:   
            # llamamos a la funcion de los trofeos
            estado_actual = ejecutar_ranking(ventana_principal, RELOJ)
            
        elif estado_actual == ESTADO_AUDIO:    
            estado_actual = ejecutar_sonidos(ventana_principal, RELOJ)
        elif estado_actual == ESTADO_CREDITOS:
            print(">>> MAIN ENTRO A CREDITOS")

    # 🔥 BLOQUEA TODO HASTA QUE CREDITOS TERMINE
            while estado_actual == ESTADO_CREDITOS:
                estado_actual = ejecutar_creditos(ventana_principal, RELOJ)

                # Si el juego nos dice que salgamos, detenemos el bucle principal
        elif estado_actual == ESTADO_SALIR:
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