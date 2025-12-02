import os
import sys
import pygame
import random

from modules.ventana import ANCHO_PANTALLA_P as ANCHO
from modules.ventana import LARGO_PANTALLA_P as LARGO
from modules.ventana import ICONO

pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Tux's REVOLUTION")

# VENTANA #
from modules.ventana import ventana_principal  # "Lienzo"/Pantalla principal
from modules.ventana import ICONO, NOMBRE_JUEGO as NOMBRE  # Visuales de la pantalla
from modules.ventana import ANCHO_PANTALLA_P as ANCHO, LARGO_PANTALLA_P as ALTO  # Dimensiones
from modules.configs import FPS, RELOJ  # Configuraciones nucleo main
# MENU #
from modules.ventana import ESTADO_MENU, ESTADO_JUGAR, ESTADO_SALIR  # Estados en el juego
from modules.menu import ejecutar_menu  # Menu completo
# ENTIDADES #
from modules.entidades.entidades import dibujar_entidad  # graficador de entidades
# paleta:
from modules.entidades.paleta import crear_paleta  # creador de paletas (si no lo usas aquí está)
# from modules.entidades.paleta import movimiento_paleta  # NO lo usamos para permitir invertir/bloquear controles
from modules.entidades.paleta import paleta_rect, paleta_img  # Parametros de dibujado MOVIMIENTO / VISUAL
# pelota:
from modules.entidades.pelota import crear_pelota  # creador de pelotas
from modules.entidades.pelota import tamano_pelota, POS_Y_PELOTA, POS_X_PELOTA  # valores pelota
from modules.entidades.pelota import movimiento_pelota  # movimiento de pelota (lo usamos para rebotes normales)
# ladrillos
from modules.creacion_de_ladrillos.tamaño_ladrillo import ALTO_LADRILLO, ANCHO_LADRILLO, COLOR_LADRILLO

pygame.display.set_caption(NOMBRE)
pygame.display.set_icon(ICONO)


# ---------------------------
# COLORES (ladrillos / poderes)
# ---------------------------
COLOR_NORMAL = (0, 180, 0)    # Verde: ladrillo normal (sin poder)
COLOR_SOMBRERO = (255, 0, 0)  # Rojo: Sombrero (RED HAT)
COLOR_VINO = (150, 0, 150)    # Violeta: Vino
COLOR_TACHO = (180, 180, 180) # Gris claro: Tacho de basura
COLOR_KERNEL = (30, 30, 30)   # Negro/oscuro: Kernel Panic

# ---------------------------
# CONFIGURACIÓN PODERES
# ---------------------------
PODER_SOMBRERO = "sombrero"
PODER_VINO = "vino"
PODER_TACHO = "tacho"
PODER_KERNEL = "kernel"

TIPOS_PODER = [PODER_SOMBRERO, PODER_VINO, PODER_TACHO, PODER_KERNEL]
PROB_PODER = 20  # % de probabilidad de que un ladrillo tenga poder al generarse
DURACION_PODER_MS = 5000  # 5 segundos en ms


# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def coli_ladrillos(pelota_rect, ladrillos, vel_x, vel_y, tamano_pelota, rompe_ladrillos):
    """
    Maneja las colisiones con los ladrillos.
    - ladrillos: lista de [rect, poder] donde poder puede ser None o un string
    - si rompe_ladrillos == True elimina ladrillo sin rebotar
    Devuelve: vel_x, vel_y, powerup_nuevo (dict) o None
    """
    powerup_nuevo = None

    for entry in ladrillos[:]:
        rect, poder = entry
        if pelota_rect.colliderect(rect):
            if rompe_ladrillos:
                # elimina sin rebotar
                ladrillos.remove(entry)
                if poder is not None:
                    powerup_nuevo = {
                        "tipo": poder,
                        "rect": pygame.Rect(rect.centerx - 16, rect.centery - 16, 32, 32),
                        "vel": 3,
                        "creado_en": pygame.time.get_ticks()
                    }
                return vel_x, vel_y, powerup_nuevo

            # eliminación normal + rebote
            ladrillos.remove(entry)

            distancia_x = pelota_rect.centerx - rect.centerx
            distancia_y = pelota_rect.centery - rect.centery

            if abs(distancia_x) > abs(distancia_y):
                vel_x *= -1
            else:
                vel_y *= -1

            # si tenía poder, generamos el powerup que cae
            if poder is not None:
                powerup_nuevo = {
                    "tipo": poder,
                    "rect": pygame.Rect(rect.centerx - 16, rect.centery - 16, 32, 32),
                    "vel": 3,
                    "creado_en": pygame.time.get_ticks()
                }

            break

    return vel_x, vel_y, powerup_nuevo


def reducir_vida(vidas: int) -> tuple[int, bool]:
    vidas -= 1
    if vidas <= 0:
        print("GAME OVER ")
        return vidas, True
    else:
        return vidas, False


def mostrar_corazones(pantalla, vidas_restantes):
    for i in range(vidas_restantes):
        rect_vida = pygame.Rect(15 + i * 60, 15, 50, 50)
        pygame.draw.rect(pantalla, (255, 0, 0), rect_vida)


# ---------------------------
# EJECUTAR JUEGO (TODO LOCAL)
# ---------------------------
def ejecutar_juego(pantalla, reloj):
    """
    Bucle principal del estado JUGAR.
    Maneja paleta, pelota, movimiento, colisiones y poderes.
    Devuelve: (estado_siguiente, puntuacion, vidas)
    """
    vidas = 3
    puntuacion = 0

    # Generar ladrillos como [rect, poder]
    LADRILLOS = []
    for fila in range(5):
        for columna in range(11):
            x = columna * (ANCHO_LADRILLO + 10)
            y = fila * (ALTO_LADRILLO + 10)
            rect = pygame.Rect(x, y, ANCHO_LADRILLO, ALTO_LADRILLO)

            if random.randint(1, 100) <= PROB_PODER:
                poder = random.choice(TIPOS_PODER)
            else:
                poder = None

            LADRILLOS.append([rect, poder])

    # Crear entidades
    pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota)
    base_vel_x, base_vel_y = vel_x, vel_y  # guardamos veloc. base para restaurar al terminar poderes

    paleta_rect.centerx = ANCHO // 2

    pelota_en_juego = False
    pelota_rect.centerx = paleta_rect.centerx
    pelota_rect.bottom = paleta_rect.top

    # SISTEMA DE PODERES (local)
    powerups_en_escena = []  # list of dicts {"tipo","rect","vel","creado_en"}
    paleta_rapida = False
    paleta_rapida_inicio = 0

    pelota_rapida = False
    pelota_rapida_inicio = 0
    vino_contador = 0

    rompe_ladrillos = False
    rompe_inicio = 0

    kernel_panic = False
    kernel_inicio = 0
    # para restaurar velocidades cuando termina kernel_panic (guardadas al activarse)
    pelota_vel_guardada_x = None
    pelota_vel_guardada_y = None

    jugando = True
    while jugando:
        reloj.tick(FPS)
        pantalla.fill((30, 80, 90))

        # ---- Eventos ----
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return ESTADO_SALIR, puntuacion, vidas

            if evento.type == pygame.KEYDOWN:
                # lanzar pelota solo si no hay kernel_panic
                if evento.key == pygame.K_SPACE and not pelota_en_juego and not kernel_panic:
                    pelota_en_juego = True

        # ---- MOVIMIENTO DE PALETA (manual para soportar invertir/bloquear) ----
        keys = pygame.key.get_pressed()

        velocidad_paleta = 8
        if paleta_rapida:
            velocidad_paleta = 12

        if kernel_panic:
            # paleta inmovilizada -> no aplicamos movimiento
            pass
        else:
            invertidos = (vino_contador >= 2)
            mov = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])  # 1,0,-1
            if invertidos:
                mov = -mov
            paleta_rect.x += mov * velocidad_paleta

            # mantener en pantalla
            if paleta_rect.left < 0:
                paleta_rect.left = 0
            if paleta_rect.right > ANCHO:
                paleta_rect.right = ANCHO

        # ---- MOVIMIENTO DE LA PELOTA ----
        if pelota_en_juego and not kernel_panic:
            # comportamiento normal (usa tu función existente)
            vel_x, vel_y = movimiento_pelota(pelota_rect, paleta_rect, vel_x, vel_y, ANCHO, ALTO)
        elif pelota_en_juego and kernel_panic:
            # la pelota está quieta durante kernel_panic (vel_x, vel_y ya puestos a 0 al activarse)
            pass

        # ---- COLISIÓN con ladrillos (puede devolver powerup) ----
        vel_x, vel_y, power_nuevo = coli_ladrillos(pelota_rect, LADRILLOS, vel_x, vel_y, tamano_pelota, rompe_ladrillos)
        if power_nuevo:
            powerups_en_escena.append(power_nuevo)

        # ---- puntuación ----
        if pelota_en_juego:
            puntuacion += 1

        # ---- ganar si no quedan ladrillos ----
        if not LADRILLOS:
            print("ganaste")
            return ESTADO_MENU, puntuacion, vidas

        # ---- si la pelota no está en juego mantenerla sobre paleta ----
        if not pelota_en_juego:
            pelota_rect.centerx = paleta_rect.centerx
            pelota_rect.bottom = paleta_rect.top

        # ---- DIBUJADO ENTIDADES ----
        dibujar_entidad(pantalla, paleta_img, paleta_rect)
        dibujar_entidad(pantalla, pelota_img, pelota_rect)

        # DIBUJAR LADRILLOS con color segun su poder
        for entry in LADRILLOS:
            rect, poder = entry
            if poder == PODER_SOMBRERO:
                color = COLOR_SOMBRERO
            elif poder == PODER_VINO:
                color = COLOR_VINO
            elif poder == PODER_TACHO:
                color = COLOR_TACHO
            elif poder == PODER_KERNEL:
                color = COLOR_KERNEL
            else:
                color = COLOR_NORMAL
            pygame.draw.rect(pantalla, color, rect)

        # ---- MOVER Y DIBUJAR powerups que caen ----
        tiempo_actual = pygame.time.get_ticks()
        for p in powerups_en_escena[:]:
            p["rect"].y += p["vel"]

            if p["tipo"] == PODER_SOMBRERO:
                color_item = COLOR_SOMBRERO
            elif p["tipo"] == PODER_VINO:
                color_item = COLOR_VINO
            elif p["tipo"] == PODER_TACHO:
                color_item = COLOR_TACHO
            elif p["tipo"] == PODER_KERNEL:
                color_item = COLOR_KERNEL
            else:
                color_item = (255, 255, 255)

            pygame.draw.rect(pantalla, color_item, p["rect"])

            # Si la paleta atrapa el item -> activar efecto
            if p["rect"].colliderect(paleta_rect):
                tipo = p["tipo"]

                # --- SOMBRERO: paleta mas rapida 5s ---
                if tipo == PODER_SOMBRERO:
                    paleta_rapida = True
                    paleta_rapida_inicio = tiempo_actual

                # --- VINO: pelota mas rapida 5s; si agarra 2 vinos invierte controles ---
                elif tipo == PODER_VINO:
                    if not pelota_rapida:
                        pelota_rapida = True
                        pelota_rapida_inicio = tiempo_actual
                        # guardamos base y multiplicamos las velocidades actuales
                        base_vel_x, base_vel_y = vel_x, vel_y
                        if vel_x != 0:
                            vel_x = int(vel_x * 1.5) if abs(vel_x) >= 1 else vel_x
                        if vel_y != 0:
                            vel_y = int(vel_y * 1.5) if abs(vel_y) >= 1 else vel_y
                    else:
                        # renovar tiempo (extiende efecto)
                        pelota_rapida_inicio = tiempo_actual
                    vino_contador += 1

                # --- TACHO: pelota atraviesa ladrillos 5s ---
                elif tipo == PODER_TACHO:
                    rompe_ladrillos = True
                    rompe_inicio = tiempo_actual

                # --- KERNEL PANIC: inmoviliza paleta + deja pelota quieta + pierdes 1 vida ---
                elif tipo == PODER_KERNEL:
                    kernel_panic = True
                    kernel_inicio = tiempo_actual
                    # guardamos velocidad actual de la pelota para restaurar despues
                    pelota_vel_guardada_x = vel_x
                    pelota_vel_guardada_y = vel_y
                    # dejamos la pelota completamente quieta
                    vel_x = 0
                    vel_y = 0
                    # restar una vida al recibirlo
                    vidas -= 1
                    if vidas <= 0:
                        return ESTADO_MENU, puntuacion, vidas

                # eliminar item de escena
                powerups_en_escena.remove(p)

            # si el item cae fuera de pantalla lo quitamos
            elif p["rect"].top > ALTO:
                powerups_en_escena.remove(p)

        # ---- CONTROLAR DURACION DE PODERES (5s = DURACION_PODER_MS) ----
        # Sombrero
        if paleta_rapida and (tiempo_actual - paleta_rapida_inicio > DURACION_PODER_MS):
            paleta_rapida = False

        # Vino
        if pelota_rapida and (tiempo_actual - pelota_rapida_inicio > DURACION_PODER_MS):
            # restaurar velocidad base si la guardamos
            if 'base_vel_x' in locals() and 'base_vel_y' in locals():
                vel_x, vel_y = base_vel_x, base_vel_y
            pelota_rapida = False
            vino_contador = 0

        # Tacho
        if rompe_ladrillos and (tiempo_actual - rompe_inicio > DURACION_PODER_MS):
            rompe_ladrillos = False

        # Kernel Panic: restaurar paleta y pelota a los 5s
        if kernel_panic and (tiempo_actual - kernel_inicio > DURACION_PODER_MS):
            kernel_panic = False
            # restaurar velocidad de la pelota si la teníamos guardada
            if pelota_vel_guardada_x is not None and pelota_vel_guardada_y is not None:
                vel_x = pelota_vel_guardada_x
                vel_y = pelota_vel_guardada_y
            pelota_vel_guardada_x = None
            pelota_vel_guardada_y = None

        # ---- dibujar corazones y flip pantalla ----
        mostrar_corazones(pantalla, vidas)
        pygame.display.flip()

        # ---- si la pelota cae fuera de la pantalla ----
        if pelota_rect.bottom > ALTO:
            vidas, juego_terminado = reducir_vida(vidas)
            if juego_terminado:
                return ESTADO_MENU, puntuacion, vidas
            # recrear pelota y restaurar velocidades base
            pelota_rect, pelota_img, vel_x, vel_y = crear_pelota(POS_X_PELOTA, POS_Y_PELOTA, tamano_pelota)
            base_vel_x, base_vel_y = vel_x, vel_y
            paleta_rect.centerx = ANCHO // 2
            pelota_en_juego = False

    # fin del while jugando
    pygame.quit()
    return ESTADO_MENU, puntuacion, vidas


# ---------------------------
# MAIN
# ---------------------------
def main() -> None:
    estado_actual = ESTADO_MENU
    vidas = 3
    puntuacion = 0
    corriendo = True
    while corriendo:
        if estado_actual == ESTADO_MENU:
            estado_actual = ejecutar_menu(ventana_principal, RELOJ)
            if estado_actual == ESTADO_SALIR:
                corriendo = False

        elif estado_actual == ESTADO_JUGAR:
            estado_actual, puntuacion, vidas = ejecutar_juego(ventana_principal, RELOJ)
            print(estado_actual)
            if estado_actual == ESTADO_SALIR:
                corriendo = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
