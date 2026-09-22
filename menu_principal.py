import pygame
import sys
import subprocess
import os

# 1. Inicialización básica
pygame.init()
ANCHO, ALTO = 600, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lanzador de Juegos Arcade - Python Pro")
reloj = pygame.time.Clock()

# Fuentes y Colores
fuente_tit = pygame.font.SysFont("Impact", 45)
fuente_btn = pygame.font.SysFont("Arial", 24)

COLOR_FONDO = (12, 10, 22)
COLOR_TEXTO = (255, 255, 255)

# TRUCO DE COMPILACIÓN CLAVE: Detectar si corre como archivo ejecutable .exe o script suelto
if getattr(sys, 'frozen', False):
    # Si es .exe, los archivos se extraen en la carpeta temporal de PyInstaller
    RUTA_BASE = sys._MEIPASS
else:
    # Si es desarrollo, usa la carpeta real del escritorio
    RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

# 2. Definición de Botones con sus respectivas rutas calculadas
botones = [
    {
        "rect": pygame.Rect(150, 180, 300, 60),
        "texto": "🚀 Jugar Space Shooter",
        "script": os.path.join(RUTA_BASE, "_Space_Arcade", "space_arcade_pro.py"),
        "color": (0, 255, 200)
    },
    {
        "rect": pygame.Rect(150, 280, 300, 60),
        "texto": "🐦 Jugar Flappy Neon",
        "script": os.path.join(RUTA_BASE, "_Flappy_Neon", "flappy_bird_neon.py"),
        "color": (255, 215, 0)
    }
]

# 3. Función para lanzar el juego secundario de forma blindada
def lanzar_juego(ruta_script):
    if not os.path.exists(ruta_script):
        print(f"\n[ERROR] No se encontró el archivo en:\n{ruta_script}")
        return

    # Ocultamos la ventana del menú principal temporalmente
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    
    try:
        if getattr(sys, 'frozen', False):
            # Si es .exe, no llamamos a 'python.exe' (porque no existe en la PC de tus amigos).
            # Leemos y ejecutamos el script de forma interna usando la función nativa exec()
            with open(ruta_script, "r", encoding="utf-8") as archivo_juego:
                codigo_juego = archivo_juego.read()
                
            # Sobrescribimos temporalmente el entorno para que Pygame inicialice la sub-ventana correctamente
            global pantalla
            pygame.quit() # Apagar el menú transitoriamente
            
            # Crear un entorno limpio para ejecutar el sub-juego
            entorno_local = {"__name__": "__main__"}
            exec(codigo_juego, entorno_local)
            
            # Al terminar el juego, reinicializamos el sistema del menú
            pygame.init()
        else:
            # Si estás probando en VS Code, el comportamiento clásico de Subprocess funciona genial
            subprocess.run([sys.executable, ruta_script])
            
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        
    # Restauramos la ventana del menú principal al finalizar
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Lanzador de Juegos Arcade - Python Pro")

# ---- BUCLE DEL MENÚ ----
while True:
    pantalla.fill(COLOR_FONDO)
    pos_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for btn in botones:
                if btn["rect"].collidepoint(pos_mouse):
                    lanzar_juego(btn["script"])

    # Dibujar elementos visuales
    txt_tit = fuente_tit.render("ARCADE STATION", True, (0, 255, 255))
    pantalla.blit(txt_tit, (ANCHO // 2 - txt_tit.get_width() // 2, 50))
    
    for btn in botones:
        esta_encima = btn["rect"].collidepoint(pos_mouse)
        color_actual = btn["color"] if esta_encima else (40, 40, 60)
        
        pygame.draw.rect(pantalla, color_actual, btn["rect"], border_radius=8)
        pygame.draw.rect(pantalla, btn["color"], btn["rect"], 2, border_radius=8)
        
        color_txt = COLOR_FONDO if esta_encima else COLOR_TEXTO
        txt_btn = fuente_btn.render(btn["texto"], True, color_txt)
        pantalla.blit(txt_btn, (btn["rect"].centerx - txt_btn.get_width() // 2, btn["rect"].centery - txt_btn.get_height() // 2))

    pygame.display.flip()
    reloj.tick(60)
