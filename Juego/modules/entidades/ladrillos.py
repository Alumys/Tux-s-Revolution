import pygame
import random
import os

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

COLORES_NORMALES = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0),
    (0, 255, 0), (0, 128, 255), (0, 0, 255), (255, 0, 255)
]

COLORES_ESPECIALES = [
    (255, 0, 0), (255, 100, 200), (80, 110, 255), (230, 230, 230)
]

# ============================================================
# CARGAR SONIDOS
# ============================================================

def cargar_sonidos_ladrillos():
    """Carga los sonidos de los ladrillos y los devuelve en un diccionario"""
    sonidos = {}
    sonidos['romper'] = pygame.mixer.Sound("C:/juego/Tux-s-Revolution/Juego/assets/sounds/destruccion_bloc.wav")
    sonidos['golpe'] = pygame.mixer.Sound("C:/juego/Tux-s-Revolution/Juego/assets/sounds/metal.wav")
    sonidos['romper'].set_volume(1.0)
    sonidos['golpe'].set_volume(1.0)
    return sonidos

# ============================================================
# CARGAR IMÁGENES
# ============================================================

def cargar_imagen(nombre, ancho=ANCHO_IMAGEN, alto=ALTO_IMAGEN):
    ruta = os.path.join(RUTA_IMG, nombre)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    return None

# ============================================================
# GENERAR CATALOGO LADRILLOS
# ============================================================

def generar_catalogo_ladrillos():
    catalogo = []

    for i in range(7):
        catalogo.append({
            "tipo": "normal",
            "color": COLORES_NORMALES[i],
            "img": cargar_imagen(f"ladrillo_{i}.png")
        })

    for i in range(4):
        catalogo.append({
            "tipo": "especial",
            "color": COLORES_ESPECIALES[i],
            "img": cargar_imagen(f"especial_{i}.png", ANCHO_IMAGEN, ALTO_IMAGEN)
        })

    return catalogo

# ============================================================
# CREAR LADRILLOS
# ============================================================

def vidas_por_fila(fila):
    if fila == 0: return 3
    if fila == 1: return 2
    return 1

def crear_ladrillos(ancho_pantalla):
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

def colisionar_con_ladrillos(pelota_rect, vel_y, ladrillos, sonidos):
    puntos_ganados = 0

    for ladrillo in ladrillos:
        if pelota_rect.colliderect(ladrillo["rect"]):
            ladrillo["vida"] -= 1

            if ladrillo["vida"] > 0 and 'golpe' in sonidos:
                sonidos['golpe'].play()

            if ladrillo["vida"] <= 0 and 'romper' in sonidos:
                sonidos['romper'].play()
                ladrillos.remove(ladrillo)
                puntos_ganados = 100

            return -vel_y, puntos_ganados

    return vel_y, 0

# ============================================================
# DIBUJAR LADRILLOS
# ============================================================

def dibujar_ladrillos(pantalla, lista):
    for ladrillo in lista:
        if ladrillo["img"]:
            pantalla.blit(ladrillo["img"], ladrillo["rect"])
        else:
            pygame.draw.rect(pantalla, ladrillo["color"], ladrillo["rect"])
