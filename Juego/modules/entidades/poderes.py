# modules/poderes/poderes.py
import time

# CONFIGURACIÓN / CONSTANTES
AUMENTO_VEL_PALETA = 5
DURACION_PALETA_RAPIDA = 8

AUMENTO_VEL_PELOTA = 4
DURACION_PELOTA_RAPIDA = 10
DURACION_CONTROL_INVERTIDO = 10

CANTIDAD_PERFORACIONES = 5

DURACION_CONGELAR_JUEGO = 4

# ESTADO GLOBAL
estado_poderes = {
    "paleta_rapida": {"activo": False, "tiempo_fin": 0},
    "pelota_rapida": {"activo": False, "tiempo_fin": 0,
                      "control_invertido_activo": False, "tiempo_fin_invertido": 0},
    "pelota_perforadora": {"activo": False, "golpes_restantes": 0},
    "juego_congelado": {"activo": False, "tiempo_fin": 0}
}

# FUNCIONES
def activar_paleta_rapida(vel_paleta):
    estado = estado_poderes["paleta_rapida"]
    estado["activo"] = True
    estado["tiempo_fin"] = time.time() + DURACION_PALETA_RAPIDA
    return vel_paleta + AUMENTO_VEL_PALETA

def activar_pelota_rapida(vel_x, vel_y):
    estado = estado_poderes["pelota_rapida"]
    if not estado["activo"]:
        estado["activo"] = True
        estado["tiempo_fin"] = time.time() + DURACION_PELOTA_RAPIDA
        return vel_x * 1.3, vel_y * 1.3
    estado["control_invertido_activo"] = True
    estado["tiempo_fin_invertido"] = time.time() + DURACION_CONTROL_INVERTIDO
    return vel_x, vel_y

def controles_invertidos():
    return estado_poderes["pelota_rapida"]["control_invertido_activo"]

def activar_pelota_perforadora():
    estado = estado_poderes["pelota_perforadora"]
    estado["activo"] = True
    estado["golpes_restantes"] = CANTIDAD_PERFORACIONES

def usar_perforacion():
    estado = estado_poderes["pelota_perforadora"]
    if not estado["activo"]:
        return
    estado["golpes_restantes"] -= 1
    if estado["golpes_restantes"] <= 0:
        estado["activo"] = False

def pelota_perforadora_activa():
    return estado_poderes["pelota_perforadora"]["activo"]

def activar_congelar_juego():
    estado = estado_poderes["juego_congelado"]
    estado["activo"] = True
    estado["tiempo_fin"] = time.time() + DURACION_CONGELAR_JUEGO

def perder_vida():
    pass

def juego_esta_congelado():
    return estado_poderes["juego_congelado"]["activo"]

def aplicar_poder(tipo, vel_paleta, vel_x, vel_y):
    # tipo: 0 paleta rapida, 1 pelota rapida/invertir, 2 perforadora, 3 congelar
    if tipo == 0:
        vel_paleta = activar_paleta_rapida(vel_paleta)
    elif tipo == 1:
        vel_x, vel_y = activar_pelota_rapida(vel_x, vel_y)
    elif tipo == 2:
        activar_pelota_perforadora()
    elif tipo == 3:
        activar_congelar_juego()
        perder_vida()
    return vel_paleta, vel_x, vel_y

def actualizar_poderes(vel_paleta_base, vel_x_base, vel_y_base):
    ahora = time.time()
    # paleta
    estado = estado_poderes["paleta_rapida"]
    if estado["activo"] and ahora >= estado["tiempo_fin"]:
        estado["activo"] = False
    vel_paleta = vel_paleta_base + (AUMENTO_VEL_PALETA if estado["activo"] else 0)
    # pelota rapida
    estado = estado_poderes["pelota_rapida"]
    if estado["activo"] and ahora >= estado["tiempo_fin"]:
        estado["activo"] = False
    if estado["activo"]:
        vel_x = vel_x_base * 1.3
        vel_y = vel_y_base * 1.3
    else:
        vel_x = vel_x_base
        vel_y = vel_y_base
    if estado["control_invertido_activo"] and ahora >= estado["tiempo_fin_invertido"]:
        estado["control_invertido_activo"] = False
    # congelar
    estado = estado_poderes["juego_congelado"]
    if estado["activo"] and ahora >= estado["tiempo_fin"]:
        estado["activo"] = False
    return vel_paleta, vel_x, vel_y
