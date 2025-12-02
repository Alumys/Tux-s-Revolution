import pygame

# Importamos colores y constantes (ajusta si tus rutas son diferentes)
try:
    from modules.dependencias_menu.m_colores import BLANCO, NEGRO, AZUL_MENU, AMARILLO, ROJO, VERDE
except ImportError:
    BLANCO, NEGRO, AZUL_MENU, AMARILLO, ROJO, VERDE = (255, 255, 255), (0, 0, 0), (0, 102, 204), (255, 255, 0), (200, 0, 0), (0, 200, 0)

def ejecutar_opciones(pantalla, reloj):
    """
    Pantalla de configuración de volumen.
    """
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_botones = pygame.font.Font(None, 40)
    
    # Definimos los rectángulos de los botones
    # (Centro X, Y, Ancho, Alto)
    ancho_p = pantalla.get_width()
    centro_x = ancho_p // 2
    
    btn_menos = pygame.Rect(centro_x - 150, 300, 50, 50)
    btn_mas = pygame.Rect(centro_x + 100, 300, 50, 50)
    btn_mute = pygame.Rect(centro_x - 75, 400, 150, 50)
    
    viendo_opciones = True
    
    while viendo_opciones:
        reloj.tick(60)
        
        # Obtenemos el volumen actual (va de 0.0 a 1.0)
        volumen_actual = pygame.mixer.music.get_volume()
        
        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SALIR"
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    viendo_opciones = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_mas.collidepoint(evento.pos):
                    # Subir volumen (tope 1.0)
                    nuevo_vol = min(1.0, volumen_actual + 0.1)
                    pygame.mixer.music.set_volume(nuevo_vol)
                    print(f"Volumen: {nuevo_vol:.1f}")
                    
                if btn_menos.collidepoint(evento.pos):
                    # Bajar volumen (tope 0.0)
                    nuevo_vol = max(0.0, volumen_actual - 0.1)
                    pygame.mixer.music.set_volume(nuevo_vol)
                    print(f"Volumen: {nuevo_vol:.1f}")

                if btn_mute.collidepoint(evento.pos):
                    # Mutear (Poner a 0)
                    pygame.mixer.music.set_volume(0.0)
                    print("Muteado")

        # --- DIBUJADO ---
        pantalla.fill(NEGRO)
        
        # Título y Valor actual
        texto_titulo = fuente_titulo.render("OPCIONES DE AUDIO", True, BLANCO)
        pantalla.blit(texto_titulo, texto_titulo.get_rect(center=(centro_x, 100)))
        
        texto_valor = fuente_titulo.render(f"{int(volumen_actual * 100)}%", True, AMARILLO)
        pantalla.blit(texto_valor, texto_valor.get_rect(center=(centro_x, 325)))

        # Dibujar Botones
        pygame.draw.rect(pantalla, ROJO, btn_menos)
        pygame.draw.rect(pantalla, VERDE, btn_mas)
        pygame.draw.rect(pantalla, AZUL_MENU, btn_mute)
        
        # Textos de los botones
        pantalla.blit(fuente_botones.render("-", True, BLANCO), (btn_menos.x + 18, btn_menos.y + 12))
        pantalla.blit(fuente_botones.render("+", True, BLANCO), (btn_mas.x + 15, btn_mas.y + 12))
        pantalla.blit(fuente_botones.render("MUTEAR", True, BLANCO), (btn_mute.x + 20, btn_mute.y + 12))

        # Instrucción volver
        texto_volver = fuente_botones.render("ESC para volver", True, (150, 150, 150))
        pantalla.blit(texto_volver, texto_volver.get_rect(center=(centro_x, 550)))

        pygame.display.flip()
        
    return "MENU"