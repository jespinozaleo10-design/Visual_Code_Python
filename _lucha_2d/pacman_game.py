import pygame
import sys
import math
import random

# 1. Inicialización y Configuración Gráfica
pygame.init()
LADO_CELDA = 30  # Tamaño de cada bloque del laberinto
FILAS, COLUMNAS = 15, 20  # Dimensiones de la cuadrícula
ANCHO, ALTO = COLUMNAS * LADO_CELDA, (FILAS * LADO_CELDA) + 50
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Pac-Man - Generador Automático e IA")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Impact", 24)

# 2. GENERADOR AUTOMÁTICO DE LABERINTO (Evita errores de sintaxis)
# Creamos un tablero inicial con bordes rígidos y pasillos internos libres
MAPA = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
for f in range(FILAS):
    for c in range(COLUMNAS):
        # Crear los muros exteriores del mapa
        if f == 0 or f == FILAS - 1 or c == 0 or c == COLUMNAS - 1:
            MAPA[f][c] = 1
        # Añadir algunos bloques de obstáculos simétricos en el centro
        elif f % 2 == 0 and c % 3 == 0:
            MAPA[f][c] = 1
        elif f in [4, 10] and 5 <= c <= 14:
            MAPA[f][c] = 1

# 3. Copiar píldoras del mapa para poder consumirlas
pildoras = [[True if MAPA[f][c] == 0 else False for c in range(COLUMNAS)] for f in range(FILAS)]

# 4. PROPIEDADES DE LAS ENTIDADES (Posiciones seguras iniciales)
pacman = {"x": 1, "y": 1, "dir_x": 0, "dir_y": 0, "prox_dir_x": 0, "prox_dir_y": 0}
fantasma = {"x": 18, "y": 13, "dir_x": -1, "dir_y": 0, "color": (255, 0, 128)} # Fucsia

puntuacion = 0
juego_terminado = False

# 5. INTELIGENCIA ARTIFICIAL DE PERSECUCIÓN
def mover_fantasma_ia(f_data, p_data, mapa):
    direcciones_posibles = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    movimientos_validos = []

    for dx, dy in direcciones_posibles:
        if dx == -f_data["dir_x"] and dy == f_data["dir_y"]:
            continue
        if mapa[f_data["y"] + dy][f_data["x"] + dx] != 1:
            movimientos_validos.append((dx, dy))

    if not movimientos_validos:
        movimientos_validos.append((-f_data["dir_x"], -f_data["dir_y"]))

    mejor_dir = movimientos_validos[0]
    distancia_minima = float("inf")

    for dx, dy in movimientos_validos:
        sig_x = f_data["x"] + dx
        sig_y = f_data["y"] + dy
        dist = math.sqrt((sig_x - p_data["x"])**2 + (sig_y - p_data["y"])**2)
        
        if dist < distancia_minima:
            distancia_minima = dist
            mejor_dir = (dx, dy)

    f_data["dir_x"], f_data["dir_y"] = mejor_dir
    f_data["x"] += f_data["dir_x"]
    f_data["y"] += f_data["dir_y"]

# ---- BUCLE PRINCIPAL ----
timer_movimiento = 0
while True:
    pantalla.fill((10, 8, 20))
    
    # === CAPTURA DE EVENTOS ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if evento.type == pygame.KEYDOWN:
            if juego_terminado and evento.key == pygame.K_RETURN:
                pacman = {"x": 1, "y": 1, "dir_x": 0, "dir_y": 0, "prox_dir_x": 0, "prox_dir_y": 0}
                fantasma = {"x": 18, "y": 13, "dir_x": -1, "dir_y": 0, "color": (255, 0, 128)}
                pildoras = [[True if MAPA[f][c] == 0 else False for c in range(COLUMNAS)] for f in range(FILAS)]
                puntuacion = 0
                juego_terminado = False
            
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a: pacman["prox_dir_x"], pacman["prox_dir_y"] = -1, 0
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d: pacman["prox_dir_x"], pacman["prox_dir_y"] = 1, 0
            if evento.key == pygame.K_UP or evento.key == pygame.K_w: pacman["prox_dir_x"], pacman["prox_dir_y"] = 0, -1
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s: pacman["prox_dir_x"], pacman["prox_dir_y"] = 0, 1

    # === LÓGICA DE JUEGO ===
    if not juego_terminado:
        timer_movimiento += 1
        if timer_movimiento >= 9:  # Mover entidades (ajusta para variar velocidad)
            
            # Intentar aplicar el giro deseado por el jugador
            if MAPA[pacman["y"] + pacman["prox_dir_y"]][pacman["x"] + pacman["prox_dir_x"]] != 1:
                pacman["dir_x"], pacman["dir_y"] = pacman["prox_dir_x"], pacman["prox_dir_y"]
            
            # Mover a Pac-Man si no hay pared por delante
            if MAPA[pacman["y"] + pacman["dir_y"]][pacman["x"] + pacman["dir_x"]] != 1:
                pacman["x"] += pacman["dir_x"]
                pacman["y"] += pacman["dir_y"]

            # Consumir píldoras
            if pildoras[pacman["y"]][pacman["x"]]:
                pildoras[pacman["y"]][pacman["x"]] = False
                puntuacion += 10

            # Mover al Fantasma con IA
            mover_fantasma_ia(fantasma, pacman, MAPA)
            timer_movimiento = 0

        # Detectar colisión
        if pacman["x"] == fantasma["x"] and pacman["y"] == fantasma["y"]:
            juego_terminado = True

    # === RENDERIZADO VISUAL ===
    # 1. Dibujar el Laberinto generado por código
    for y in range(FILAS):
        for x in range(COLUMNAS):
            rect_celda = pygame.Rect(x * LADO_CELDA, y * LADO_CELDA, LADO_CELDA, LADO_CELDA)
            if MAPA[y][x] == 1:
                pygame.draw.rect(pantalla, (15, 25, 50), rect_celda)
                pygame.draw.rect(pantalla, (0, 120, 255), rect_celda, 2, border_radius=4)
            elif pildoras[y][x]:
                pygame.draw.circle(pantalla, (255, 185, 0), rect_celda.center, 4)

    # 2. Dibujar a Pac-Man
    centro_p = (pacman["x"] * LADO_CELDA + LADO_CELDA//2, pacman["y"] * LADO_CELDA + LADO_CELDA//2)
    pygame.draw.circle(pantalla, (255, 230, 0), centro_p, LADO_CELDA//2 - 2)

    # 3. Dibujar al Fantasma
    rect_f = pygame.Rect(fantasma["x"] * LADO_CELDA + 4, fantasma["y"] * LADO_CELDA + 4, LADO_CELDA - 8, LADO_CELDA - 8)
    pygame.draw.rect(pantalla, fantasma["color"], rect_f, border_radius=4)
    pygame.draw.circle(pantalla, (255, 255, 255), (rect_f.x + 6, rect_f.y + 8), 3)
    pygame.draw.circle(pantalla, (255, 255, 255), (rect_f.x + 16, rect_f.y + 8), 3)

    # 4. HUD inferior
    txt_pts = fuente.render(f"PUNTOS: {puntuacion}", True, (0, 255, 200))
    pantalla.blit(txt_pts, (20, FILAS * LADO_CELDA + 12))

    if juego_terminado:
        txt_go = fuente.render("¡ATRAPADO! Presiona ENTER para reiniciar", True, (255, 50, 50))
        pantalla.blit(txt_go, (ANCHO // 2 - 160, FILAS * LADO_CELDA + 12))

    pygame.display.flip()
    reloj.tick(60)
