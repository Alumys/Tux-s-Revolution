import pygame
import time

from .pelota import crear_pelota, movimiento_pelota
from .ladrillos import colisionar_con_ladrillos

def actualizar_pelotas(
    pelotas, paleta_rect, ladrillos, sonidos,
    ancho, alto, tamano_pelota, estado
):
    """
    Actualiza todas las pelotas:
    - Mueve la pelota normal
    - Genera UNA pelota extra solo una vez por juego
    - La extra dura 3 segundos y quita vida si se pierde
    """

    tiempo_actual = time.time()

    # Inicializamos la variable que controla si la extra ya salió
    if not hasattr(actualizar_pelotas, "extra_creada"):
        actualizar_pelotas.extra_creada = False

    for pelota in pelotas[:]:

        # -------------------
        # Movimiento normal
        # -------------------
        pelota["vx"], pelota["vy"] = movimiento_pelota(
            pelota["rect"],
            paleta_rect,
            pelota["vx"],
            pelota["vy"],
            ancho,
            alto
        )

        # -------------------
        # Colisión con ladrillos
        # -------------------
        pelota["vy"], puntos, tipo_ladrillo = colisionar_con_ladrillos(
            pelota["rect"],
            pelota["vy"],
            ladrillos,
            sonidos
        )

        # -------------------
        # Generar pelota extra
        # -------------------
        if (
            puntos > 0
            and tipo_ladrillo == "normal"   # solo ladrillos fáciles
            and not actualizar_pelotas.extra_creada
            and not pelota.get("extra")     # la normal no genera otra extra
        ):
            r, img, vx, vy = crear_pelota(
                pelota["rect"].centerx,
                pelota["rect"].centery,
                tamano_pelota
            )

            pelotas.append({
                "rect": r,
                "img": img,
                "vx": vx,
                "vy": -abs(vy),
                "extra": True,
                "inicio": tiempo_actual
            })

            actualizar_pelotas.extra_creada = True  # marcamos que ya salió

        # -------------------
        # Eliminar pelota extra después de 3 segundos
        # -------------------
        if pelota.get("extra") and tiempo_actual - pelota["inicio"] >= 3:
            pelotas.remove(pelota)
            # restar una vida si la extra no fue devuelta
            if "vidas" in estado:
                estado["vidas"] -= 1
