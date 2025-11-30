import os # Importacion de SISTEMA OPERATIVO. Comprobacion de la existencia de archivos
import sys # No es tan necesario pero es una recomendacion para una mejor optimizacion del programa
import pygame # Importacion de la Biblioteca pygame


from modules.ventana import ANCHO_PANTALLA_P as ANCHO
from modules.ventana import LARGO_PANTALLA_P as LARGO
from modules.ventana import ICONO

pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")

# VENTANA #
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
#ladrillos 
from modules.creacion_de_ladrillos.tamaño_ladrillo import ALTO_LADRILLO, ANCHO_LADRILLO, COLOR_LADRILLO
pygame.init()

# Configs. Ventana principal: (visual y nombre)
pygame.display.set_caption(NOMBRE)
pygame.display.set_icon(ICONO)
#corazon_imagen= pygame.image.load("c:/Users/dario/Downloads/corazon.png")
#corazon_imagen=pygame.transform.scale(corazon_imagen, (35, 35))


def coli_ladrillos(pelota_rect, bricks, vel_x, vel_y, tamano_pelota):
    """Maneja las colisiones con los ladrillos."""
    for brick in bricks[:]:
        if pelota_rect.colliderect(brick):
            bricks.remove(brick)
            # Calcular la distancia entre el centro de la pelota y el ladrillo
            distancia_x = pelota_rect.centerx - brick.centerx
            distancia_y = pelota_rect.centery - brick.centery
            # Cambiar la dirección de la pelota
            if abs(distancia_x) > abs(distancia_y):
                vel_x *= -1
            else:
                vel_y *= -1
            break
    return vel_x, vel_y


VIDAS= 3
LADRILLOS= []  ##lista,aca se van a guardar los ladrillos 


def reducir_vida(VIDAS: int)-> tuple[int,bool]:
    """
    gestiona la perdida de vida disminuye el contador 

    args:
        1.(int) el numero de vidas despues de la resta 
        2.(booleano) true si es juego termino (vidas <= 0) false si continua
    
    
    """

#restamos si pierde una vida
    VIDAS -=1

#aca vamos a comprobar si se perdio las 3 vidas

    if VIDAS <= 0:
        print("GAME OVER ")

    #devolvemos el nuevo valor y true para indicar el fin del juego
        return (VIDAS, True)

    #devolvemos el numvo valor y false para indicar que el juego continua
    # es decir si vidas > 0

    else:
        return(VIDAS, False)


for fila in range(5): # aca se imprimira 5 filas
    for columna in range(11): #aca se imprimira 10 columnas 
        x = columna * (ANCHO_LADRILLO + 10)     #10 pixeles de separacion horizontal
        y = fila * (ALTO_LADRILLO + 10)         # 10 pixeles de separacion vertical

        ladrillo=pygame.Rect(x,y, ANCHO_LADRILLO, ALTO_LADRILLO)  # (aca creamos ladrillos con tamaño y
        LADRILLOS.append(ladrillo) # lo guarda en la lista vacia      posicion )                      

VIDAS= 3 # comenzamos con 3 vidas 


#funcion para mostrar los corazones
def mostrar_corazones(vidas_restantes ):
    for i in range(vidas_restantes):
         #ventana_principal.blit(corazon_imagen, (10 + i * 40, 10)) #separa los corazones por 40 pixeles 
        rect_vida=pygame.Rect(15 + i * 60, 15,50, 50)                                                     # 10 es la posision x del primer corazon 
        pygame.draw.rect(ventana_principal,(255, 0, 0), rect_vida )


def reiniciar_paleta(rect):
    paleta_rect.centerx = ANCHO // 2
    

def ejecutar_juego(pantalla, reloj):
    """
    Bucle principal del estado JUGAR.
    Maneja paleta, pelota, movimiento y colisiones.
    """
    VIDAS= 3
    puntuacion=0
    
    LADRILLOS= []  ##lista,aca se van a guardar los ladrillosf

    for fila in range(5): # aca se imprimira 5 filas
      for columna in range(11): #aca se imprimira 10 columnas 
        x = columna * (ANCHO_LADRILLO + 10)     #10 pixeles de separacion horizontal

        y = fila * (ALTO_LADRILLO + 10)         # 10 pixeles de separacion vertical

        ladrillo=pygame.Rect(x,y, ANCHO_LADRILLO, ALTO_LADRILLO)  # (aca creamos ladrillos con tamaño y
        LADRILLOS.append(ladrillo) # lo guarda en la lista vacia      posicion )                      

    # ---- Crear entidades mutables ---- #
    pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota) 
    paleta_rect.centerx=ANCHO // 2

    pelota_en_juego=False

    pelota_rect.centerx=paleta_rect.centerx
    pelota_rect.bottom=paleta_rect.top
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
                if evento.key == pygame.K_SPACE and not pelota_en_juego:
                    pelota_en_juego=True
                    

        # MOVIMIENTOS ENTIDADES
        movimiento_paleta(paleta_rect) # @~LAU~ nota-PALETA: luego colocar un condicional para el RED HAT
        if pelota_en_juego:
            vel_x, vel_y = movimiento_pelota(pelota_rect, paleta_rect, vel_x, vel_y, ANCHO, ALTO) # @~LAU~ nota-PELOTA: luego colocar un condicional para wine
            vel_x, vel_y = coli_ladrillos(pelota_rect, LADRILLOS, vel_x, vel_y, tamano_pelota)
            puntuacion +=1
            if not LADRILLOS:
                print("ganaste")
                return ESTADO_MENU, VIDAS, puntuacion
        else:
            pelota_rect.centerx=pelota_rect.centerx
            pelota_rect.bottom=paleta_rect.top
        # blitteo/dibujado
        dibujar_entidad(pantalla, paleta_img, paleta_rect)
        dibujar_entidad(pantalla, pelota_img, pelota_rect)
        
        for i in LADRILLOS:
            pygame.draw.rect(ventana_principal,COLOR_LADRILLO, i ) 
        
        mostrar_corazones(VIDAS)
        pygame.display.flip()
        
        if pelota_rect.bottom > ALTO:
            VIDAS , juego_terminado=reducir_vida(VIDAS)
            if juego_terminado:
                return ESTADO_MENU, VIDAS, puntuacion
                return ESTADO_SALIR
            pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota)
            paleta_rect.centerx = ANCHO // 2

            
            pelota_en_juego=False

def main()->None:
    """
    Inicializa Pygame y ejecuta el bucle 
    de gestión de estados hasta que se alcanza el estado SALIR.
    """
    # La variable que controla en qué parte del juego estamos
    estado_actual = ESTADO_MENU 
    VIDAS= 3
    puntuacion=0
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
            estado_actual, puntuacion,VIDAS=ejecutar_juego(ventana_principal, RELOJ)
            print(estado_actual)
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