"""
Sistema completo de ladrillos para Breakout.
Incluye:
- 11 tipos diferentes (7 normales, 4 especiales)
- Vidas basadas en la fila
- Drops para ladrillos especiales
"""

import pygame
import random
import os
from modules.entidades.tiradas_objetos import crear_drop

# ============================================================
# CONFIGURACIÓN
# ============================================================

FILAS = 5
COLUMNAS = 10

ANCHO_LADRILLO = 100
ALTO_LADRILLO = 50

ANCHO_IMAGEN = 110
ALTO_IMAGEN = 100

ESPACIADO = 0

RUTA_IMG = "assets/images/ladrillos/"

# ---- Colores para normales ----
COLORES_NORMALES = [
    (255, 0, 0),      # rojo
    (255, 128, 0),    # naranja
    (255, 255, 0),    # amarillo
    (0, 255, 0),      # verde
    (0, 128, 255),    # azul medio
    (0, 0, 255),      # azul
    (255, 0, 255),    # rosa
]

# ---- Colores para especiales ----
COLORES_ESPECIALES = [
    (255, 0, 0),
    (255, 100, 200),
    (80, 110, 255),
    (230, 230, 230)
]

# ============================================================
# CARGAR IMAGEN
# ============================================================

def cargar_imagen(nombre, ancho=ANCHO_IMAGEN, alto=ALTO_IMAGEN):
    """Carga una imagen si existe, y la escala al tamaño del ladrillo."""
    ruta = os.path.join(RUTA_IMG, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    return None


# ============================================================
# GENERAR 11 TIPOS DE LADRILLOS
# ============================================================

def generar_catalogo_ladrillos():
    """
    Devuelve una lista de 11 tipos de ladrillos:
    - 7 normales
    - 4 especiales
    Cada tipo contiene:
      color, imagen, tipo ("normal"/"especial")
    """
    catalogo = []

    # ---- 7 normales ----
    for i in range(7):
        catalogo.append({
            "tipo": "normal",
            "color": COLORES_NORMALES[i],
            "img": cargar_imagen(f"ladrillo_{i}.png")
        })

    # ---- 4 especiales ----
    for i in range(4):
        catalogo.append({
            "tipo": "especial",
            "color": COLORES_ESPECIALES[i],
            "img": cargar_imagen(f"especial_{i}.png", ANCHO_IMAGEN, ALTO_IMAGEN)
        })

    return catalogo


# ============================================================
# CREACIÓN DE LADRILLOS
# ============================================================

def vidas_por_fila(fila):
    """
    Determina cuántos golpes necesita un ladrillo dependiendo de la fila.
    Fila 0: 3 golpes
    Fila 1: 2 golpes
    Fila 2-3-4: 1 golpe
    """
    if fila == 0:
        return 3
    elif fila == 1:
        return 2
    return 1


def crear_ladrillos(ancho_pantalla):
    """
    Crea una parrilla de ladrillos 5x10.
    Mezcla los 11 tipos definidos en un catálogo.
    Asigna vidas según la fila.
    """
    inicio_x = (ancho_pantalla - (COLUMNAS * (ANCHO_LADRILLO + ESPACIADO))) // 2

    catalogo = generar_catalogo_ladrillos()
    ladrillos = []

    for fila in range(FILAS):
        for col in range(COLUMNAS):

            tipo = random.choice(catalogo)

            x = inicio_x + col * (ANCHO_LADRILLO + ESPACIADO)
            y = 30 + fila * (ALTO_LADRILLO + ESPACIADO)

            ladrillos.append({
                "rect": pygame.Rect(x, y, ANCHO_LADRILLO, ALTO_LADRILLO),
                "img": tipo["img"],
                "color": tipo["color"],
                "tipo": tipo["tipo"],
                "vida": vidas_por_fila(fila) if tipo["tipo"] == "normal" else 1
            })

    return ladrillos


# ============================================================
# COLISIONES
# ============================================================

def colisionar_con_ladrillos(pelota_rect, vel_y, ladrillos, drops):
    """
    Maneja colisión con cualquier ladrillo.
    - Resta vida
    - Si vida llega a 0 → eliminar
    - Si es especial → crear drop
    Retorna: nueva vel_y
    """

    for ladrillo in ladrillos:
        if pelota_rect.colliderect(ladrillo["rect"]):

            # ↓ Resta vida
            ladrillo["vida"] -= 1

            # ↓ Si el ladrillo muere...
            if ladrillo["vida"] <= 0:

                # Si era especial → drop
                if ladrillo["tipo"] == "especial":
                    drops.append(crear_drop(ladrillo["rect"].centerx,
                                            ladrillo["rect"].centery))

                # Eliminar ladrillo
                ladrillos.remove(ladrillo)

            # Siempre rebota
            return -vel_y

    return vel_y


# ============================================================
# DIBUJAR
# ============================================================

def dibujar_ladrillos(pantalla, lista):
    """Dibuja ladrillos con imagen o color."""
    for ladrillo in lista:
        if ladrillo["img"]:
            pantalla.blit(ladrillo["img"], ladrillo["rect"])
        else:
            pygame.draw.rect(pantalla, ladrillo["color"], ladrillo["rect"])
