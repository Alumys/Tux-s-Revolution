import os
import random
import pygame
from modules.entidades.poderes import efecto_velocidad_tux, efecto_vida_extra
"""
modules/entidades/tiradas_objetos.py

Módulo responsable por:
- crear drop (objeto que cae cuando se rompe un ladrillo especial)
- actualizar su caída
- dibujarlo
- detectar colisión con la paleta
- aplicar un efecto simple cuando la paleta recoge el drop

Las funciones están diseñadas para ser llamadas desde el loop principal.
"""
# ---------- CONSTANTES POR DEFECTO ----------
DEFAULT_ANCHO = 50
DEFAULT_ALTO = 50
DEFAULT_VEL = 3
RUTA_IMAGEN = 'assets/images/iconos/icono_revolucion.png'

# ---------- FUNCIÓN: crear_drop ----------
def crear_drop(x, y, ancho=DEFAULT_ANCHO, alto=DEFAULT_ALTO, color=None, ruta_imagen=RUTA_IMAGEN):
    """
    Crea y devuelve un diccionario que representa un drop.

    Args:
        cordenada_x(int): 
        cordenada_y(int): coordenadas iniciales (superior-izquierda).
        ancho(int): tamano largo.
        alto(int): tamano alto.
        color(tuple): color. Si es None se genera uno aleatorio suave.
        ruta_imagen(str): ruta a imagen opcional (si existe se usa).

    Returns:
        dict: {
            "rect": pygame.Rect,
            "imagen": Surface o None,
            "color": (r,g,b) o None,
            "velocidad": int,
            "activo": bool
        }
    """
    rect = pygame.Rect(x, y, ancho, alto)

    imagen = None
    # si existe ruta de imagen y archivo real -> cargar y escalar
    if ruta_imagen and os.path.exists(ruta_imagen):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (ancho, alto))

    # 1. Elegimos qué tipo de poder es (Vida o Velocidad)
    tipo_poder = random.choice(["vida", "velocidad"])
    
    # 2. Le asignamos el color según el tipo
    if tipo_poder == "vida":
        color = (255, 0, 0)
    else:
        color = (0, 255, 255)
        

    return {
        "rect": rect,
        "imagen": imagen,
        "color": color,
        "velocidad": 3,
        "activo": True,
        "tipo": tipo_poder
    }


# ---------- FUNCIÓN: actualizar_drop ----------
def actualizar_drop(drop, alto_pantalla):
    """
    Actualiza la posición del drop (lo hace caer).
    Marca inactivo si sale de la pantalla.
    """
    if not drop["activo"]:
        return
    drop["rect"].y += drop["velocidad"]
    if drop["rect"].top > alto_pantalla:
        drop["activo"] = False


# ---------- FUNCIÓN: dibujar_drop ----------
def dibujar_drop(pantalla, drop):
    """
    Dibuja el drop en pantalla usando imagen si existe, si no un rectángulo de color.
    """
    if not drop["activo"]:
        return
    if drop["imagen"]:
        pantalla.blit(drop["imagen"], drop["rect"])
    else:
        pygame.draw.rect(pantalla, drop["color"], drop["rect"])


# ---------- FUNCIÓN: drop_colisiona_paleta ----------
def drop_colisiona_paleta(drop, paleta_rect):
    """
    Chequea si el drop colisiona con la paleta.
    Si colisiona marca el drop como inactivo y retorna True.
    """
    if drop["activo"] and drop["rect"].colliderect(paleta_rect):
        drop["activo"] = False
        return True
    return False


def aplicar_power_up(drop, paleta_rect, vidas_actuales, velocidad_actual):
    """
    Aplica el efecto según el tipo del drop.
    Devuelve las vidas y la velocidad (posiblemente modificadas).
    """
    # 1. Identificamos qué poder es
    # Si por alguna razón no tiene tipo, asumimos que es velocidad
    tipo = drop.get("tipo", "velocidad") 
    
    # 2. Aplicamos el efecto correspondiente
    if tipo == "velocidad":
        # Llamamos a la funcion de poderes.py
        velocidad_actual = efecto_velocidad_tux(velocidad_actual)
        
    elif tipo == "vida":
        # Llamamos a la funcion de poderes.py
        vidas_actuales = efecto_vida_extra(vidas_actuales)
        
    # 3. Importante: Devolvemos AMBOS valores al main para que actualice el juego
    return vidas_actuales, velocidad_actual