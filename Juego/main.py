import pygame
import sys # Importa sys para un manejo de salida limpio

from modules.ventana import ANCHO_PANTALLA_P as ANCHO
from modules.ventana import LARGO_PANTALLA_P as LARGO
from modules.ventana import ICONO
from modules.ventana_di import (ANCHO_PANTALLA , ALTO_PANTALLA,CENTRO_X,INICIO_Y,ESPACIADO,
                                            ANCHO_BOTON,ALTO_BOTON,BLANCO,NEGRO,AZUL_MENU,AMARILLO,GRIS_PANEL)

pygame.init() # Asegúrate que esto esté antes de usar fuentes

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")
pygame.display.set_icon(ICONO)


def manejar_acciones_boton(indice):
    """
    Maneja las acciones basadas en el índice del botón pulsado.
    Ahora devuelve el estado siguiente (string).
    """
    match indice:
        case 0: print(">>> Iniciando el juego principal..."); return "jugar"
        case 1: print(">>> Conectando al lobby..."); return "menu"
        case 2: print(">>> Mostrando puntuaciones altas..."); return "menu"
        case 3: print(">>> Abriendo opciones..."); return "menu"
        case 4: print(">>> Mostrando los créditos..."); return "menu"
        case 5: return "salir" # Devuelve "salir" para indicar salida

# DATOS DEL MENÚ Y POSICIONES
fuente_titulo = pygame.font.Font(None, 80)
fuente_opciones = pygame.font.Font(None, 40)

textos_botones = ["JUGAR", "MULTIJUGADOR", "PUNTUACIÓN", "OPCIONES DE JUEGO", "CRÉDITOS", "SALIR"]
# Almacenamos los puntos del polígono, el Rect para colisiones y la posición Y del texto
botones_data = []

# Corregido el nombre de la función y la indentación interna
def inicializar_botones_menu():
    for i, texto in enumerate(textos_botones):
        pos_y_centro = INICIO_Y + i * ESPACIADO + (20 if texto == "SALIR" else 0)

        # Calcular los 4 vértices del diamante
        puntos_diamante = [
            (CENTRO_X, pos_y_centro - ALTO_BOTON // 2),
            (CENTRO_X + ANCHO_BOTON // 2, pos_y_centro),
            (CENTRO_X, pos_y_centro + ALTO_BOTON // 2),
            (CENTRO_X - ANCHO_BOTON // 2, pos_y_centro)
        ]

        rect_colision = pygame.Rect(CENTRO_X - ANCHO_BOTON // 2, pos_y_centro - ALTO_BOTON // 2, ANCHO_BOTON, ALTO_BOTON)
        botones_data.append({"puntos": puntos_diamante, "centro_y": pos_y_centro, "rect": rect_colision})

# Corregido el uso de 'pantalla' por 'ventana_principal'
def dibujar_menu():
    ventana_principal.fill(BLANCO)

    # Dibujamos el panel de fondo
    panel_surface = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
    pygame.draw.rect(panel_surface, GRIS_PANEL, panel_surface.get_rect(), border_radius=50)
    ventana_principal.blit(panel_surface, (0, 0))

    texto_titulo = fuente_titulo.render("TUX REVOLUTION", True, NEGRO)
    rect_titulo = texto_titulo.get_rect(center=(CENTRO_X, 100))
    ventana_principal.blit(texto_titulo, rect_titulo)

    posicion_mouse = pygame.mouse.get_pos()

    for i, data in enumerate(botones_data):
        if data["rect"].collidepoint(posicion_mouse):
             color = AMARILLO
        else:
             color = AZUL_MENU

        # Dibujamos la forma de polígono (diamante) visualmente
        pygame.draw.polygon(ventana_principal, color, data["puntos"])

        # Renderizamos el texto
        superficie_texto = fuente_opciones.render(textos_botones[i], True, NEGRO)
        rect_texto = superficie_texto.get_rect(center=(CENTRO_X, data["centro_y"]))
        ventana_principal.blit(superficie_texto, rect_texto)

# --- Configuración Inicial ---
inicializar_botones_menu() # Llama a la función corregida
estado_actual = "menu" # Define que el programa inicia en el menú


corriendo = True # bandera de bucle principal
while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        

        if estado_actual == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, data in enumerate(botones_data):
                    if data["rect"].collidepoint(evento.pos):
                        accion = manejar_acciones_boton(i)
                        if accion == "salir":
                            corriendo = False
                        elif accion == "jugar":
                            estado_actual = "juego" 
        elif estado_actual == "juego":
             # Ejemplo: presionar ESCAPE para volver al menú
             if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                 estado_actual = "menu"

    if estado_actual == "menu":
        dibujar_menu() # Dibuja todos los elementos del menú
    elif estado_actual == "juego":
        # Aquí es donde pondrás tu código del juego real más adelante
        ventana_principal.fill((0, 100, 0)) # Fondo verde temporal de ejemplo
        font = pygame.font.Font(None, 50)
        text = font.render("AQUÍ VA TU JUEGO", True, BLANCO)
        ventana_principal.blit(text, (100, 100))

    # --- Actualizador de Pantalla Único (movido al final) ---
    pygame.display.update() 

pygame.quit()
