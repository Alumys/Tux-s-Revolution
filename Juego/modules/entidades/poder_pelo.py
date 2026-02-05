import pygame
import time

from .pelota import crear_pelota, movimiento_pelota
from .ladrillos import colisionar_con_ladrillos

def actualizar_pelotas(
    pelotas, paleta_rect, ladrillos, sonidos,
    ancho, alto, tamano_pelota
):
    tiempo_actual = time.time()

    for pelota in pelotas[:]:

        pelota["vx"], pelota["vy"] = movimiento_pelota(
            pelota["rect"],
            paleta_rect,
            pelota["vx"],
            pelota["vy"],
            ancho,
            alto
        )

        pelota["vy"], puntos = colisionar_con_ladrillos(
            pelota["rect"],
            pelota["vy"],
            ladrillos,
            sonidos
        )

        # 🟣 generar pelota extra
        if puntos > 0 and not any(p.get("extra") for p in pelotas):

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

        # ⏱️ eliminar pelota extra
        if pelota.get("extra") and tiempo_actual - pelota["inicio"] >= 4:
            pelotas.remove(pelota)
