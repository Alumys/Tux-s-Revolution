import pygame, os

CREDITOS = [
    ("Araceli", r"C:\juego\Tux-s-Revolution\Juego\assets\images\ara.png.png"),
    ("StrTimO", r"C:\juego\Tux-s-Revolution\Juego\assets\images\timo.png.png"),
    ("AlumYs", r"C:\juego\Tux-s-Revolution\Juego\assets\images\lauta.png.png")
]


def ejecutar_creditos(_, reloj):
    pantalla = pygame.display.get_surface()
    w, h = pantalla.get_size()
    cx = w // 2
    f_titulo, f_texto = pygame.font.Font(None, 60), pygame.font.Font(None, 40)

    creditos = []
    for nombre, ruta in CREDITOS:
        img = pygame.transform.scale(pygame.image.load(ruta).convert_alpha(), (80, 80)) if os.path.exists(ruta) else pygame.Surface((80,80))
        if not os.path.exists(ruta): img.fill((255,0,0))
        creditos.append((f_texto.render(nombre, True, (255,255,255)), img))

    while True:
        reloj.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "SALIR"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: return "MENU"

        pantalla.fill((30,30,30))
        pantalla.blit(f_titulo.render("CRÉDITOS", True, (255,255,0)), (cx-150, 80))
        y = 200
        for surf, img in creditos:
            pantalla.blit(img, (cx-100, y-40))
            pantalla.blit(surf, surf.get_rect(center=(cx+50, y)))
            y += 120
        pantalla.blit(f_texto.render("ESC para volver", True, (180,180,180)), (cx-120, h-50))
        pygame.display.update()
