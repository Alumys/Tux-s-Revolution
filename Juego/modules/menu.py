import pygame

# ===========================
# IMPORTS DESDE modules.ventana (RESPETADO)
# ===========================
from modules.ventana import (
    LARGO_PANTALLA_P,
    FONDO_MENU,
    TITULO_JUEGO,
    BOTON_OPCION,
    BOTON_SELECCION,
    FUENTE_GENERAL
)

# ===========================
# CONFIGURACIONES ORIGINALES TUYAS (USADAS)
# ===========================
ANCHO_PANTALLA = 800  
CENTRO_X = ANCHO_PANTALLA // 2

INICIO_Y = 250          # ← USADO PARA LA BASE DEL MENÚ
ESPACIADO = 130         # ← USADO PARA DISTANCIA VERTICAL REAL

ALTO_BOTON = 60
ANCHO_BOTON = 300

textos_botones = ["JUGAR", "PUNTUACIÓN", "AUDIO", "CRÉDITOS", "SALIR"]

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MENU = (0, 102, 204)
AMARILLO = (255, 255, 0)

# ===========================
# NUEVAS CONSTANTES (AGREGADAS Y DOCUMENTADAS)
# ===========================
# Estas NO existían, por eso se documentan.
# Solo controlan la separación horizontal en el menú doble columna.

# --- distancia horizontal desde el centro hacia la izquierda
POS_MENU_X_OFFSET = 260      

# --- distancia horizontal desde el centro hacia la derecha
# (es igual pero con signo opuesto, por claridad se explicita)
POS_MENU_COL_IZQ = CENTRO_X - POS_MENU_X_OFFSET  
POS_MENU_COL_DER = CENTRO_X + POS_MENU_X_OFFSET  

# --- factor para ajustar que el menú doble columna INICIE justo donde tu INICIO_Y indicaba
POS_MENU_Y_INICIO = INICIO_Y + 35  

# --- creciente vertical REAL basado EN TU ESPACIADO
POS_MENU_Y_ESPACIADO = ESPACIADO  


# ===========================================================
# FUNCIÓN DE ACCIÓN CENTRAL (RESPETADA)
# ===========================================================
def manejar_acciones_boton(indice: int) -> str:
    if indice == 0:
        print(">>> Iniciando el juego principal...")
        return "JUGAR"
    elif indice == 1:
        print(">>> Mostrando puntuaciones altas...")
        return "PUNTOS"
    elif indice == 2:
        print(">>> Abriendo audio...")
        return "AUDIO"
    elif indice == 3:
        print(">>> Mostrando los créditos...")
        return "MENU"
    elif indice == 4:
        print(">>> Acción de Salir")
        return "SALIR"
    return "MENU"


# ===========================================================
# EJECUCIÓN DEL MENÚ
# ===========================================================
def ejecutar_menu(pantalla, reloj):

    botones_data = []

    for i, texto in enumerate(textos_botones):

        # -----------------------------------------
        # POSICIONAMIENTO EN DOS COLUMNAS
        # Usando tus constantes INICIO_Y y ESPACIADO
        # -----------------------------------------

        if texto == "SALIR":
            # Botón centrado al final
            pos_x = CENTRO_X
            pos_y = POS_MENU_Y_INICIO + (2 * POS_MENU_Y_ESPACIADO) - 200
        else:
            # Ejemplo:
            #   0 → izquierda
            #   1 → derecha
            #   2 → izquierda
            #   3 → derecha
            if i % 2 == 0:
                pos_x = POS_MENU_COL_IZQ
            else:
                pos_x = POS_MENU_COL_DER

            # Alineación vertical basada en tu ESPACIADO real
            pos_y = POS_MENU_Y_INICIO + (i // 2) * POS_MENU_Y_ESPACIADO

        rect_colision = pygame.Rect(
            pos_x - ANCHO_BOTON // 2,
            pos_y - ALTO_BOTON // 2,
            ANCHO_BOTON,
            ALTO_BOTON
        )

        botones_data.append({
            "centro_x": pos_x,
            "centro_y": pos_y,
            "rect": rect_colision,
            "puntos": []  # respetado
        })

    # ===========================================================
    # LOOP DEL MENÚ
    # ===========================================================
    bucle_principal_menu = True

    while bucle_principal_menu:

        reloj.tick(60)
        posicion_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SALIR"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, data in enumerate(botones_data):
                    if data["rect"].collidepoint(evento.pos):
                        nuevo_estado = manejar_acciones_boton(i)
                        if nuevo_estado != "MENU":
                            return nuevo_estado

        # Fondo
        pantalla.blit(FONDO_MENU, (0, 0))

        # Panel
        panel_surface = pygame.Surface((ANCHO_PANTALLA, LARGO_PANTALLA_P), pygame.SRCALPHA)
        pantalla.blit(panel_surface, (0, 0))
        pantalla.blit(TITULO_JUEGO, (145, -30))

        # Botones
        for i, data in enumerate(botones_data):

            esta_encima = data["rect"].collidepoint(posicion_mouse)
            imagen_boton = BOTON_SELECCION if esta_encima else BOTON_OPCION

            rect_boton = imagen_boton.get_rect(center=(data["centro_x"], data["centro_y"]))
            pantalla.blit(imagen_boton, rect_boton)

            superficie_texto = FUENTE_GENERAL.render(textos_botones[i], True, NEGRO)
            rect_texto = superficie_texto.get_rect(center=(data["centro_x"], data["centro_y"]))
            pantalla.blit(superficie_texto, rect_texto)

        pygame.display.flip()

    return "SALIR"
