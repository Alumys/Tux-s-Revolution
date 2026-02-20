import os
import pygame

def efecto_velocidad_tux(velocidad_actual):
    """
    Recibe la velocidad actual y devuelve una velocidad más rápida (10).
    Si ya es rápido, se queda igual.
    """
    if velocidad_actual < 10:
        print(">>> POWER UP: ¡Super Velocidad Activada!")
        return 10  # Nueva velocidad rápida
    else:
        return velocidad_actual # Ya tenía el poder

def efecto_vida_extra(vidas_actuales):
    """
    Suma 1 vida.
    """
    print(">>> POWER UP: +1 Vida")
    return vidas_actuales + 1