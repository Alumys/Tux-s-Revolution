import pygame
import os
import random

#from tiradas_objetos import crear_drop

# ============================================================
# CONFIG GENERAL
# ============================================================

FILAS = 5
COLUMNAS = 10
ANCHO_LADRILLO = 70
ALTO_LADRILLO = 25
ESPACIADO = 5

RUTA_IMG = "assets/ladrillos"

# -------------------------
# COLORES NORMALES
# -------------------------
COLORES_NORMALES = [
    (255, 0, 0),      # rojo
    (255, 128, 0),    # naranja
    (255, 255, 0),    # amarillo
    (0, 255, 0),      # verde
    (0, 128, 255),    # azul medio
    (0, 0, 255),      # azul
    (255, 0, 255),    # rosa
]

# -------------------------
# COLORES DE PODERES (4)
# -------------------------
COLORES_ESPECIALES = [
    (255, 0, 0),       # rojo (power-up)
    (255, 100, 200),   # rosa especial
    (80, 110, 255),    # azul marino claro
    (230, 230, 230),   # blanco grisáceo
]

# ============================================================
# CARGA DE IMAGEN SI EXISTE
# ============================================================

def cargar_imagen(nombre, ancho, alto):
    ruta = os.path.join(RUTA_IMG, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        img = pygame.transform.scale(img, (ancho, alto))
        return img
    return None


# ============================================================
# GENERADOR DE LOS 11 TIPOS DE LADRILLOS
# ============================================================

def generar_catalogo_ladrillos():
    """
    Devuelve una lista de 11 definiciones diferentes de ladrillos:
    - 7 normales (con imagen opcional)
    - 4 especiales (con imagen opcional)
    """
    catalogo = []

    # ---- 7 LADRILLOS NORMALES ----
    for i in range(7):
        color = COLORES_NORMALES[i % len(COLORES_NORMALES)]
        img = cargar_imagen(f"normal_{i}.png", ANCHO_LADRILLO, ALTO_LADRILLO)

        catalogo.append({
            "tipo": "normal",
            "color": color,
            "img": img
        })

    # ---- 4 LADRILLOS ESPECIALES ----
    for i in range(4):
        color = COLORES_ESPECIALES[i]
        img = cargar_imagen(f"especial_{i}.png", ANCHO_LADRILLO, ALTO_LADRILLO)

        catalogo.append({
            "tipo": "especial",
            "color": color,
            "img": img
        })

    return catalogo


# ============================================================
# CREAR LA PARRILLA DE LADRILLOS
# ============================================================

def crear_ladrillos(ancho_pantalla):
    """
    Crea una parrilla de ladrillos usando 11 tipos diferentes mezclados al azar.
    """
    inicio_x = (ancho_pantalla - (COLUMNAS * (ANCHO_LADRILLO + ESPACIADO))) // 2

    # Generamos catálogo base (11 tipos distintos)
    catalogo = generar_catalogo_ladrillos()

    ladrillos = []

    for fila in range(FILAS):
        for col in range(COLUMNAS):

            # Elegimos un tipo al azar del catálogo
            tipo = random.choice(catalogo)

            x = inicio_x + col * (ANCHO_LADRILLO + ESPACIADO)
            y = 50 + fila * (ALTO_LADRILLO + ESPACIADO)

            rect = pygame.Rect(x, y, ANCHO_LADRILLO, ALTO_LADRILLO)

            ladrillos.append({
                "rect": rect,
                "img": tipo["img"],
                "color": tipo["color"],
                "tipo": tipo["tipo"],   # normal / especial
            })

    return ladrillos


# ============================================================
# COLISIÓN – LA PELOTA ROMPE EL LADRILLO
# ============================================================

def colisionar_con_ladrillos(pelota_rect, vel_y, lista_ladrillos):
    """
    Elimina ladrillo y rebota la pelota.
    En un futuro: si ladrillo["tipo"] == "especial" → lanzar power-up.
    """
    for ladrillo in lista_ladrillos:
        if pelota_rect.colliderect(ladrillo["rect"]):
            lista_ladrillos.remove(ladrillo)
            return -vel_y
    return vel_y


# ============================================================
# DIBUJADO
# ============================================================

def dibujar_ladrillos(pantalla, lista):
    for ladrillo in lista:
        if ladrillo["img"]:
            pantalla.blit(ladrillo["img"], ladrillo["rect"])
        else:
            pygame.draw.rect(pantalla, ladrillo["color"], ladrillo["rect"])
