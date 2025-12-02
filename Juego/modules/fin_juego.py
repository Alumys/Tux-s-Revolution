import pygame
from modules.puntuaciones import guardar_puntaje_en_ranking

# 1. IMPORTAMOS LOS COLORES EXISTENTES
try:
    from modules.dependencias_menu.m_colores import BLANCO, NEGRO, AZUL_MENU, AMARILLO
except ImportError:
    # Por si falla la importación, definimos respaldos
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    AZUL_MENU = (0, 102, 204)
    AMARILLO = (255, 255, 0)

# 2. DEFINIMOS COLORES EXTRA (Necesarios para Ganar/Perder)
ROJO_ERROR = (200, 50, 50)  # Para Game Over
VERDE_EXITO = (50, 200, 50) # Para Victoria

def ejecutar_pantalla_fin(pantalla, reloj, puntaje_final, gano_partida):
    """
    Muestra la pantalla de fin, pide nombre y guarda puntaje.
    """
    fuente_grande = pygame.font.Font(None, 70)
    fuente_mediana = pygame.font.Font(None, 40)
    
    # Configurar título y color según resultado
    if gano_partida:
        texto_titulo = "¡VICTORIA!"
        color_titulo = VERDE_EXITO
    else:
        texto_titulo = "GAME OVER"
        color_titulo = ROJO_ERROR
        
    nombre_ingresado = ""
    ingresando = True
    
    while ingresando:
        reloj.tick(30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SALIR"
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(nombre_ingresado.strip()) > 0:
                        ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    # Limite de 12 letras
                    if len(nombre_ingresado) < 12 and evento.unicode.isalnum():
                        nombre_ingresado += evento.unicode

        # --- DIBUJADO ---
        pantalla.fill(NEGRO)
        centro_x = pantalla.get_width() // 2

        # Título
        sup_titulo = fuente_grande.render(texto_titulo, True, color_titulo)
        rect_titulo = sup_titulo.get_rect(center=(centro_x, 150))
        pantalla.blit(sup_titulo, rect_titulo)
        
        # Puntaje
        sup_puntaje = fuente_mediana.render(f"Puntaje Final: {puntaje_final}", True, BLANCO)
        rect_puntaje = sup_puntaje.get_rect(center=(centro_x, 250))
        pantalla.blit(sup_puntaje, rect_puntaje)
        
        # Instrucción
        sup_instruccion = fuente_mediana.render("Ingresa tu nombre y dale Enter:", True, AMARILLO)
        rect_instruccion = sup_instruccion.get_rect(center=(centro_x, 350))
        pantalla.blit(sup_instruccion, rect_instruccion)
        
        # Input del nombre
        cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else " "
        sup_nombre = fuente_grande.render(nombre_ingresado + cursor, True, AZUL_MENU)
        rect_nombre = sup_nombre.get_rect(center=(centro_x, 420))
        
        pantalla.blit(sup_nombre, rect_nombre)
        pygame.display.flip()
        
    # Guardamos el puntaje
    guardar_puntaje_en_ranking(nombre_ingresado, puntaje_final)
    
    return "PUNTOS"