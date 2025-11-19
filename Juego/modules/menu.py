import pygame

# --- CONSTANTES Y CONFIGURACIÓN ---
from modules.ventana import LARGO_PANTALLA_P
ANCHO_PANTALLA = 800  # Mantener para la lógica interna del menú
CENTRO_X = ANCHO_PANTALLA // 2
INICIO_Y = 225
ESPACIADO = 64
ALTO_DIAMANTE = 60 # Este valor sera el alto del diamante
                 
ANCHO_DIAMANTE = 300  # Este valor sera el alto del diamante

# Colores (Estas constantes de color son utiles para usar aca)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MENU = (0, 102, 204)
AMARILLO = (255, 255, 0)
GRIS_PANEL = (30, 30, 45, 180) # Con Alpha (transparencia)

# DATOS DEL MENÚ Y POSICIONES
textos_botones = ["JUGAR", "MULTIJUGADOR", "PUNTUACIÓN", "OPCIONES DE JUEGO", "CRÉDITOS", "SALIR"] # Creamos una lista con las opciones

# FUNCIÓN DE ACCIÓN CENTRAL
# Modificada para devolver un string que represente el nuevo estado
def manejar_acciones_boton(indice):
    """
    Función de acción central del menú. Determina el siguiente estado
    del juego basándose en el botón (índice) presionado.

    prametro indice: Índice (0-5) del botón seleccionado.
    return: string con el nuevo estado ("JUGAR", "SALIR" o "MENU").
    
    
    """
    if indice == 0:
        print(">>> Iniciando el juego principal...")
        return "JUGAR" # Nuevo estado: Jugar
    elif indice == 1:
        print(">>> Conectando al lobby...")
        return "MENU" # Después de esta acción, volvemos al menú
    elif indice == 2:
        print(">>> Mostrando puntuaciones altas...")
        return "MENU" # Después de esta acción, volvemos al menú
    elif indice == 3:
        print(">>> Abriendo opciones...")
        return "MENU" # Después de esta acción, volvemos al menú
    elif indice == 4:
        print(">>> Mostrando los créditos...")
        return "MENU" # Después de esta acción, volvemos al menú
    elif indice == 5:
        print(">>> Acción de Salir")
        return "SALIR" # Nuevo estado: Salir
    return "MENU" # Por defecto, si no es una acción de cambio de pantalla, se queda en el menú


def ejecutar_menu(pantalla, reloj):
    """
    Función que ejecuta el bucle de estado del menú.
    Toma el control de la aplicación, dibuja los elementos y espera
    la entrada del usuario (mouse o cierre de ventana).

    pantalla: Superficie de Pygame donde se dibujará el menú.
    reloj: Objeto pygame.time.Clock para controlar los FPS del menú.
    return: string con el nuevo estado ("JUGAR" o "SALIR").
    
    """
    
    # Fuentes (Se inicializan aca, dentro de la función)
    fuente_titulo = pygame.font.Font(None, 80)
    fuente_opciones = pygame.font.Font(None, 40)

    # --- PREPARACIÓN DE BOTONES ---
    botones_data = []
    
    for i, texto in enumerate(textos_botones):
        # La posición Y se calcula en base al texto del botón y el espaciado
        # La lógica original para el desplazamiento de "SALIR" se mantiene
        pos_y_centro = INICIO_Y + i * ESPACIADO + (20 if texto == "SALIR" else 0)
        
        # Calcular los 4 vértices del diamante
        puntos_diamante = [
            (CENTRO_X, pos_y_centro - ALTO_DIAMANTE // 2),
            (CENTRO_X + ANCHO_DIAMANTE // 2, pos_y_centro),
            (CENTRO_X, pos_y_centro + ALTO_DIAMANTE // 2),
            (CENTRO_X - ANCHO_DIAMANTE // 2, pos_y_centro)
        ]
        
        # Crear el rect de colisión (necesario para .collidepoint)
        # Ajustamos el rect para que abarque el área visual del diamante
    
        rect_colision = pygame.Rect(CENTRO_X - ALTO_DIAMANTE // 2, pos_y_centro - ALTO_DIAMANTE // 2, ANCHO_DIAMANTE, ALTO_DIAMANTE)
        
        # Almacenamos todos los datos relevantes
        botones_data.append({"puntos": puntos_diamante, "centro_y": pos_y_centro, "rect": rect_colision})

    # Título (Ajustado para usar la fuente local)
    texto_titulo = fuente_titulo.render("TUX REVOLUTION", True, NEGRO)
    rect_titulo = texto_titulo.get_rect(center=(CENTRO_X, 100))
    
    # --- BUCLE PRINCIPAL DEL MENÚ ---
    bucle_principal_menu = True # Renombramos para evitar confusión con el de main.py
    while bucle_principal_menu:
        reloj.tick(60) # Controlamos los FPS del menú
        posicion_mouse = pygame.mouse.get_pos()
        
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "SALIR" # Si el usuario cierra la ventana, salimos del juego
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, data in enumerate(botones_data):
                    if data["rect"].collidepoint(evento.pos):
                        nuevo_estado = manejar_acciones_boton(i)
                        # Si la acción del botón es cambiar de estado, devolvemos ese estado
                        if nuevo_estado != "MENU":
                            return nuevo_estado
                        # Si la acción es "MENU" (ej. un botón de opciones), el bucle del menú continúa
                        
        # 2. Dibujado 
        pantalla.fill(BLANCO) # Fondo blanco
        
        # Dibujamos el panel de fondo
        panel_surface = pygame.Surface((ANCHO_PANTALLA, LARGO_PANTALLA_P), pygame.SRCALPHA) # Usa LARGO_PANTALLA_P del main.py
        pygame.draw.rect(panel_surface, GRIS_PANEL, panel_surface.get_rect(), border_radius=50)
        pantalla.blit(panel_surface, (0, 0))
        pantalla.blit(texto_titulo, rect_titulo)

        # Dibujado de botones (diamantes)
        for i, data in enumerate(botones_data):
            if data["rect"].collidepoint(posicion_mouse):
                color = AMARILLO
            else:
                color = AZUL_MENU
                
            pygame.draw.polygon(pantalla, color, data["puntos"])
            
            # Renderizamos el texto del botón
            superficie_texto = fuente_opciones.render(textos_botones[i], True, NEGRO)
            rect_texto = superficie_texto.get_rect(center=(CENTRO_X, data["centro_y"]))
            pantalla.blit(superficie_texto, rect_texto)
            
        pygame.display.flip()
        
    return "SALIR" # En caso de que el bucle del menú se rompa inesperadamente