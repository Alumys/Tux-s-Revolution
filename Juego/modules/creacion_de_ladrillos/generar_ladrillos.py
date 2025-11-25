import pygame
from creacion_de_ladrillos.tamaño_ladrillo import ALTO_LADRILLO, ANCHO_LADRILLO, COLOR_LADRILLO
from modules.ventana import ventana_principal # "Lienzo"/Pantalla principal



#aca creeamos los ladrillos (5 filas x 10 columnas)
LADRILLOS= []  ##lista,aca se van a guardar los ladrillos 



for fila in range(5): # aca se imprimira 5 filas
    for columna in range(12): #aca se imprimira 10 columnas 
        x = columna * (ANCHO_LADRILLO + 10)     #10 pixeles de separacion horizontal
        y = fila * (ALTO_LADRILLO + 10)         # 10 pixeles de separacion vertical

        ladrillo=pygame.Rect(x,y, ANCHO_LADRILLO, ALTO_LADRILLO)  # (aca creamos ladrillos con tamaño y
        LADRILLOS.append(ladrillo) # lo guarda en la lista vacia      posicion )                      




# #aca vamos a pegar los ladrillos en la ventana  
 

for i in LADRILLOS:
    pygame.draw.rect(ventana_principal,COLOR_LADRILLO, i )   #en ventan_principal es donde dibujar
                                                            #color_ladrillo ( color del ladrillo )
                                                            #i( posicion y tamaño del rectangulo ) 
                                                            #  la (i) recorre ladrillo po rladrillo )
