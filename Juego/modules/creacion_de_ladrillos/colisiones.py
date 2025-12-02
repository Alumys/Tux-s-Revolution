from creacion_de_ladrillos.tamaño_ladrillo import ALTO_LADRILLO, ANCHO_LADRILLO, COLOR_LADRILLO
from creacion_de_ladrillos.generar_ladrillos import LADRILLOS
# Inside the game loop





def coli_ladrillos(pelota_rect, bricks, vel_x, vel_y, tamano_pelota):
    """Maneja las colisiones con los ladrillos."""
    for brick in bricks[:]:
        if pelota_rect.colliderect(brick):
            bricks.remove(brick)
            # Calcular la distancia entre el centro de la pelota y el ladrillo
            distancia_x = pelota_rect.centerx - brick.centerx
            distancia_y = pelota_rect.centery - brick.centery
            # Cambiar la dirección de la pelota
            if abs(distancia_x) > abs(distancia_y):
                vel_x *= -1
            else:
                vel_y *= -1
            break
    return vel_x, vel_y
