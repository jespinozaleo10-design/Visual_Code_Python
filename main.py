import pygame
import sys
import subprocess
import os

pygame.init()
ANCHO, ALTO = 700, 520  # Ajustamos el tamaño para una cuadrícula cómoda
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lanzador Arcade Station - 6 en 1 Pro")
reloj = pygame.time.Clock()

fuente_tit = pygame.font.SysFont("Impact", 45)
fuente_btn = pygame.font.SysFont("Arial", 20, bold=True)

COLOR_FONDO = (12, 10, 22)
COLOR_TEXTO = (255, 255, 255)

if getattr(sys, 'frozen', False):
    RUTA_BASE = sys._MEIPASS
else:
    RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

# 2. Definición de los 6 Botones organizados en 2 columnas (3 filas cada una)
botones = [
    {
        "rect": pygame.Rect(60, 150, 260, 60),
        "texto": "🚀 Space Shooter",
        "script": os.path.join(RUTA_BASE, "_Space_Arcade", "space_arcade_pro.py"),
        "color": (0, 255, 200)
    },
    {
        "rect": pygame.Rect(380, 150, 260, 60),
        "texto": "🐦 Flappy Neon",
        "script": os.path.join(RUTA_BASE, "_Flappy_Neon", "flappy_bird_neon.py"),
        "color": (255, 215, 0)
    },
    {
        "rect": pygame.Rect(60, 250, 260, 60),
        "texto": "🧱 Neon Tetris",
        "script": os.path.join(RUTA_BASE, "_tetris_game", "tetris_game.py"),
        "color": (255, 0, 128)
    },
    {
        "rect": pygame.Rect(380, 250, 260, 60),
        "texto": "🏃 Neon Plumber (Mario)",
        "script": os.path.join(RUTA_BASE, "_mario_neon", "mario_game.py"),
        "color": (255, 50, 50)
    },
    {
        "rect": pygame.Rect(60, 350, 260, 60),
        "texto": "🥋 Neon Fighter (Lucha)",
        "script": os.path.join(RUTA_BASE, "_lucha_2d", "fighting_game.py"),
        "color": (0, 150, 255)
    },
    {
        "rect": pygame.Rect(380, 350, 260, 60),
        "texto": "🏓 Pong Pro",
        "script": os.path.join(RUTA_BASE, "_pong_pro", "pong_game.py"),
        "color": (150, 255, 0)
    }
]

def lanzar_juego(ruta_script):
    if not os.path.exists(ruta_script):
        print(f"\n[ERROR] No se encontró el archivo en la ruta:\n{ruta_script}")
        return

    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    
    try:
        if getattr(sys, 'frozen', False):
            with open(ruta_script, "r", encoding="utf-8") as archivo_juego:
                codigo_juego = archivo_juego.read()
                
            global pantalla
            pygame.quit()
            entorno_local = {"__name__": "__main__"}
            exec(codigo_juego, entorno_local)
            pygame.init()
        else:
            subprocess.run([sys.executable, ruta_script])
            
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Lanzador Arcade Station - 6 en 1 Pro")

while True:
    pantalla.fill(COLOR_FONDO)
    pos_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for btn in botones:
                if btn["rect"].collidepoint(pos_mouse):
                    lanzar_juego(btn["script"])

    # Renderizar el Título Centralizado
    txt_tit = fuente_tit.render("ARCADE STATION MULTIPLAY", True, (0, 255, 255))
    pantalla.blit(txt_tit, (ANCHO // 2 - txt_tit.get_width() // 2, 40))
    
    # Dibujar la cuadrícula de botones
    for btn in botones:
        esta_encima = btn["rect"].collidepoint(pos_mouse)
        color_actual = btn["color"] if esta_encima else (30, 30, 50)
        
        pygame.draw.rect(pantalla, color_actual, btn["rect"], border_radius=10)
        pygame.draw.rect(pantalla, btn["color"], btn["rect"], 2, border_radius=10)
        
        color_txt = COLOR_FONDO if esta_encima else COLOR_TEXTO
        txt_btn = fuente_btn.render(btn["texto"], True, color_txt)
        pantalla.blit(txt_btn, (btn["rect"].centerx - txt_btn.get_width() // 2, btn["rect"].centery - txt_btn.get_height() // 2))

    pygame.display.flip()
    reloj.tick(60)
