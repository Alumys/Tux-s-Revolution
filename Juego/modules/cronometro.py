import pygame

def actualizar_cronometro(tiempo_restante, dt):
    """Resta dt (en segundos) al tiempo restante y retorna el nuevo valor."""
    tiempo_restante -= dt
    if tiempo_restante < 0:
        tiempo_restante = 0
    return tiempo_restante

def dibujar_cronometro(pantalla, fuente, tiempo_restante, color=(255, 255, 255), posicion=(20, 550)):
    """Dibuja el cronómetro en pantalla."""
    minutos = int(tiempo_restante // 60)
    segundos = int(tiempo_restante % 60)
    texto = fuente.render(f"TIEMPO: {minutos:02d}:{segundos:02d}", True, color)
    pantalla.blit(texto, posicion)

def se_acabo(tiempo_restante):
    """Retorna True si el tiempo llegó a 0."""
    return tiempo_restante <= 0
