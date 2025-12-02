import pygame
import random

# ---------------------------------------------------------
# FUNCION: Crear un drop (cubo) cuando un ladrillo especial se rompe
# ---------------------------------------------------------
def crear_drop(x, y, ancho=30, alto=30, color=None, ruta_imagen=None):
    """
    Crea un objeto que caerá desde el ladrillo especial.
    Puede usar color o imagen.
    """
    rect = pygame.Rect(x, y, ancho, alto)

    if ruta_imagen:
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.scale(imagen, (ancho, alto))
        color = None
    else:
        imagen = None
        if color is None:
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    return {
        "rect": rect,
        "imagen": imagen,
        "color": color,
        "velocidad": 3,
        "activo": True,   # si sigue cayendo
    }


# ---------------------------------------------------------
# FUNCION: Actualizar la caída del drop
# ---------------------------------------------------------
def actualizar_drop(drop, alto_pantalla):
    """
    Hace que el drop caiga y desaparezca si sale de pantalla.
    """
    if not drop["activo"]:
        return

    drop["rect"].y += drop["velocidad"]

    if drop["rect"].top > alto_pantalla:
        drop["activo"] = False


# ---------------------------------------------------------
# FUNCION: Dibujar drop
# ---------------------------------------------------------
def dibujar_drop(pantalla, drop):
    """
    Renderiza el drop usando imagen o color.
    """
    if not drop["activo"]:
        return

    if drop["imagen"]:
        pantalla.blit(drop["imagen"], drop["rect"])
    else:
        pygame.draw.rect(pantalla, drop["color"], drop["rect"])


# ---------------------------------------------------------
# FUNCION: Revisar colisión con la paleta
# ---------------------------------------------------------
def drop_colisiona_paleta(drop, paleta_rect):
    """
    Retorna True si colisiona y apaga el drop.
    """
    if drop["activo"] and drop["rect"].colliderect(paleta_rect):
        drop["activo"] = False
        return True

    return False
