import sys # No es tan necesario pero es una recomendacion para una mejor optimizacion del programa
import pygame # Importacion de la Biblioteca pygame

from modules.ventana import ANCHO_PANTALLA_P as ANCHO
from modules.ventana import LARGO_PANTALLA_P as LARGO
from modules.ventana import ICONO

pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")
from modules.ventana import ventana_principal # "Lienzo"/Pantalla principal
from modules.ventana import ESTADO_MENU, ESTADO_JUGAR, ESTADO_SALIR # Estados en el juego
from modules.ventana import ANCHO_PANTALLA_P as ANCHO, LARGO_PANTALLA_P as ALTO # Dimensiones de la pantalla
from modules.ventana import ICONO, NOMBRE_JUEGO as NOMBRE # Visuales de la pantalla 
from modules.configs import FPS, RELOJ # Configuraciones nucleo main
from modules.menu import ejecutar_menu # Menu completo
from modules.creacion_de_ladrillos.tamaño_ladrillo import ANCHO_LADRILLO, ALTO_LADRILLO, COLOR_LADRILLO

pygame.init()

# Configs. Ventana principal: (visual y nombre)
pygame.display.set_caption(NOMBRE)

pygame.display.set_icon(ICONO)

corazon_imagen= pygame.image.load("Juego/assets/images/corazon.png")



corazon_imagen=pygame.transform.scale(corazon_imagen, (35, 35))


VIDAS= 3 # comenzamos con 3 vidas 


#funcion para mostrar los corazones
def mostrar_corazones():
    for i in range(VIDAS):
         ventana_principal.blit(corazon_imagen, (10 + i * 40, 10)) #separa los corazones por 40 pixeles 
                                                                # 10 es la posision x del primer corazon 


#hecemos una funcion 
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
    

# --- Bucle de Juego --- #
def ejecutar_juego(pantalla:tuple, reloj:object)->str:
    """
    Gestiona el bucle de la partida (estado JUGAR).

    Args:
        pantalla(tuple): Superficie de Pygame para el dibujado.
        reloj(object): Objeto pygame.time.Clock para control de FPS.
    
    Returns: 
        str: estado de salida ("MENU" si se pulsa ESC, "SALIR" si se cierra la ventana).
    """
    # Aquí se debe implementar toda la lógica de juego: movimientos, colisiones, etc. # RECORDAR!
    
#aca creeamos los ladrillos (5 filas x 10 columnas)
    LADRILLOS= []  ##lista,aca se van a guardar los ladrillos 



    for fila in range(5): # aca se imprimira 5 filas
        for columna in range(10): #aca se imprimira 10 columnas 
            x = columna * (ANCHO_LADRILLO + 10)     #10 pixeles de separacion horizontal
            y = fila * (ALTO_LADRILLO + 10)         # 10 pixeles de separacion vertical

            ladrillo=pygame.Rect(x,y, ANCHO_LADRILLO, ALTO_LADRILLO)  # (aca creamos ladrillos con tamaño y
            LADRILLOS.append(ladrillo) # lo guarda en la lista vacia      posicion )                      





    # Ejemplo de un bucle de juego simple
    jugando = True
    while jugando:
        reloj.tick(FPS)
        pantalla.fill((30, 80, 90)) # Un fondo de color diferente para el juego
        
        # --- Lógica del juego aca (movimiento de personaje, enemigos, etc.) ---
        # Por ejemplo, podemos tener una función dibujar_personaje(pantalla) en otro módulo.
       
       
# #aca vamos a pegar los ladrillos en la ventana  

        for i in LADRILLOS:
                pygame.draw.rect(ventana_principal,COLOR_LADRILLO, i )   #en ventan_principal es donde dibujar
                                                            #color_ladrillo ( color del ladrillo )
                                                            #i( posicion y tamaño del rectangulo ) 
                                                            #  la (i) recorre ladrillo po rladrillo )
       
       
        mostrar_corazones()

        
# #aca vamos a pegar los ladrillos en la ventana  
 

      
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