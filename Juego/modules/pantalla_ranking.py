import pygame
from modules.puntuaciones import cargar_ranking
# Importamos tus colores (ajusta si la ruta es diferente)
try:
    from modules.dependencias_menu.m_colores import BLANCO, NEGRO, AZUL_MENU, AMARILLO
except ImportError:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    AZUL_MENU = (0, 102, 204)
    AMARILLO = (255, 255, 0)

def ejecutar_ranking(pantalla, reloj):
    """
    Muestra la lista de los mejores puntajes.
    Vuelve al menú cuando se presiona ESCAPE.
    """
    # 1. Cargar la lista de datos AL INICIO (para no leer el disco 60 veces por segundo)
    lista_top_5 = cargar_ranking()
    
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_lista = pygame.font.Font(None, 40)
    
    # Título pre-renderizado
    titulo_sup = fuente_titulo.render("MEJORES PUNTAJES", True, AMARILLO)
    titulo_rect = titulo_sup.get_rect(center=(pantalla.get_width() // 2, 100))
    
    mostrar_ranking = True
    while mostrar_ranking:
        reloj.tick(60)
        
        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SALIR"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Al presionar ESC, volvemos al menú
                    return "MENU"
        
        # --- DIBUJADO ---
        pantalla.fill(NEGRO)
        pantalla.blit(titulo_sup, titulo_rect)
        
        # Dibujar la lista
        if not lista_top_5:
            texto_vacio = fuente_lista.render("Aún no hay puntajes registrados.", True, BLANCO)
            pantalla.blit(texto_vacio, texto_vacio.get_rect(center=(pantalla.get_width()//2, 250)))
        else:
            # Iteramos para dibujar cada linea
            start_y = 200
            for i, datos in enumerate(lista_top_5):
                texto = f"{i+1}. {datos['nombre']}  -  {datos['puntos']} pts"
                linea_sup = fuente_lista.render(texto, True, BLANCO)
                linea_rect = linea_sup.get_rect(center=(pantalla.get_width() // 2, start_y + i * 50))
                pantalla.blit(linea_sup, linea_rect)
        
        # Instrucción para volver
        texto_volver = fuente_lista.render("Presiona ESC para volver", True, AZUL_MENU)
        pantalla.blit(texto_volver, texto_volver.get_rect(center=(pantalla.get_width()//2, 550)))

        pygame.display.flip()
        
    return "MENU"