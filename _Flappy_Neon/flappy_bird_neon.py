import pygame
import random
import sys
import os
import asyncio

# 1. Inicialización y Ventana
pygame.init()
ANCHO, ALTO = 500, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Flappy Bird - Edición Premium")
reloj = pygame.time.Clock()

# Fuentes
fuente_hud = pygame.font.SysFont("Impact", 35)
fuente_menu = pygame.font.SysFont("Arial", 22)

# Archivo Local para el High Score (Mejora 3)
ARCHIVO_RECORD_FLAPPY = "flappy_high_score.txt"

def cargar_high_score():
    if os.path.exists(ARCHIVO_RECORD_FLAPPY):
        try:
            with open(ARCHIVO_RECORD_FLAPPY, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def guardar_high_score(nuevo_record):
    try:
        with open(ARCHIVO_RECORD_FLAPPY, "w") as f:
            f.write(str(nuevo_record))
    except:
        pass

high_score = cargar_high_score()

# 2. VARIABLES FÍSICAS DE GRAVEDAD Y PERSONAJE
pajaro_x = 100
pajaro_y = ALTO // 2
pajaro_ancho, pajaro_alto = 35, 30

gravedad = 0.45
impulso_salto = -8
velocidad_y = 0
angulo_rotacion = 0 # Ángulo de inclinación (Mejora 1)

# CREAR SPRITE VECTORIAL DEL PERSONAJE (Mejora 1)
# Creamos una superficie transparente para dibujar nuestra nave/pájaro de neón
superficie_pajaro = pygame.Surface((pajaro_ancho, pajaro_alto), pygame.SRCALPHA)
puntos_triangulo = [(pajaro_ancho, pajaro_alto // 2), (0, 0), (5, pajaro_alto // 2), (0, pajaro_alto)]
pygame.draw.polygon(superficie_pajaro, (255, 215, 0), puntos_triangulo) # Cuerpo dorado
pygame.draw.polygon(superficie_pajaro, (255, 255, 255), puntos_triangulo, 2) # Borde blanco brillante

# 3. VARIABLES DEL ESCENARIO EN MOVIMIENTO (Scroll Infinito)
tuberias = []
velocidad_escenario = 3.5
temporizador_tuberia = 0
ANCHO_TUBERIA = 65
ESPACIO_LIBRE = 150

# EFECTO PARALLAX: Fondo con estrellas a distinta velocidad (Mejora 2)
# Cada estrella es una lista: [x, y, velocidad, tamaño]
estrellas_lejanas = [[random.randint(0, ANCHO), random.randint(0, ALTO), random.uniform(0.2, 0.6), 1] for _ in range(30)]
estrellas_cercanas = [[random.randint(0, ANCHO), random.randint(0, ALTO), random.uniform(0.8, 1.5), 2] for _ in range(15)]

puntuacion = 0
juego_activo = False

# 4. FUNCIÓN PARA GENERAR NUEVAS TUBERÍAS
def crear_tuberia():
    altura_centro = random.randint(150, ALTO - 150)
    tuberia_superior = pygame.Rect(ANCHO, 0, ANCHO_TUBERIA, altura_centro - (ESPACIO_LIBRE // 2))
    tuberia_inferior = pygame.Rect(ANCHO, altura_centro + (ESPACIO_LIBRE // 2), ANCHO_TUBERIA, ALTO)
    return {"sup": tuberia_superior, "inf": tuberia_inferior, "pasada": False}

# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((12, 10, 22))  # Fondo cyberpunk oscuro espacial
    temporizador_tuberia += 1

    # === CAPTURA DE EVENTOS (Controles) ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                if not juego_activo:
                    tuberias.clear()
                    pajaro_y = ALTO // 2
                    velocidad_y = 0
                    puntuacion = 0
                    juego_activo = True
                else:
                    velocidad_y = impulso_salto

    # === LÓGICA DE MOVIMIENTO FONDO PARALLAX (Mejora 2) ===
    # Las estrellas se mueven de forma constante independientemente del estado del juego
    for e in estrellas_lejanas:
        e[0] -= e[2]
        if e[0] < 0: e[0] = ANCHO; e[1] = random.randint(0, ALTO)
        pygame.draw.circle(pantalla, (100, 100, 150), (int(e[0]), int(e[1])), e[3])

    for e in estrellas_cercanas:
        e[0] -= e[2]
        if e[0] < 0: e[0] = ANCHO; e[1] = random.randint(0, ALTO)
        pygame.draw.circle(pantalla, (0, 255, 255), (int(e[0]), int(e[1])), e[3])

    # === LÓGICA CON EL JUEGO EN MARCHA ===
    if juego_activo:
        # 1. Aplicar Gravedad Artificial
        velocidad_y += gravedad
        pajaro_y += velocidad_y

        # CALCULAR ROTACIÓN EN BASE A VELOCIDAD (Mejora 1)
        # Si sube, inclina la punta hacia arriba; si cae, rota fuertemente hacia abajo.
        angulo_rotacion = -velocidad_y * 4
        angulo_rotacion = max(-75, min(35, angulo_rotacion)) # Límites de rotación estéticos

        # 2. Generar tuberías
        if temporizador_tuberia >= 90:
            tuberias.append(crear_tuberia())
            temporizador_tuberia = 0

        # 3. Mover las tuberías (Escenario en movimiento)
        for tub in tuberias[:]:
            tub["sup"].x -= velocidad_escenario
            tub["inf"].x -= velocidad_escenario
            
            if tub["sup"].right < 0:
                tuberias.remove(tub)
                
            if not tub["pasada"] and tub["sup"].centerx < pajaro_x:
                puntuacion += 1
                tub["pasada"] = True

        # 4. DETECCIÓN DE COLISIONES
        rect_pajaro_col = pygame.Rect(pajaro_x - 12, pajaro_y - 12, 24, 24)
        
        if pajaro_y < 0 or pajaro_y > ALTO:
            juego_activo = False
            if puntuacion > high_score: high_score = puntuacion; guardar_high_score(high_score)

        for tub in tuberias:
            if rect_pajaro_col.colliderect(tub["sup"]) or rect_pajaro_col.colliderect(tub["inf"]):
                juego_activo = False
                if puntuacion > high_score: high_score = puntuacion; guardar_high_score(high_score)

    else:
        # Si no se está jugando, la nave se mantiene nivelada flotando suavemente
        angulo_rotacion = 0

    # === RENDERIZADO / DIBUJO VISUAL ===
    # 1. Dibujar tuberías de neón
    for tub in tuberias:
        pygame.draw.rect(pantalla, (20, 35, 45), tub["sup"])
        pygame.draw.rect(pantalla, (0, 255, 200), tub["sup"], 3)
        pygame.draw.rect(pantalla, (20, 35, 45), tub["inf"])
        pygame.draw.rect(pantalla, (0, 255, 200), tub["inf"], 3)

    # 2. RENDERIZAR ROTACIÓN DEL PERSONAJE (Mejora 1)
    # Rotamos la superficie vectorial creada originalmente
    pajaro_rotado = pygame.transform.rotate(superficie_pajaro, angulo_rotacion)
    nuevo_rect = pajaro_rotado.get_rect(center=(int(pajaro_x), int(pajaro_y)))
    pantalla.blit(pajaro_rotado, nuevo_rect.topleft)

    # 3. Mostrar Interfaz Gráfica (HUD) (Mejora 3)
    if juego_activo:
        txt_pts = fuente_hud.render(str(puntuacion), True, (255, 255, 255))
        txt_record_vivo = fuente_menu.render(f"Récord: {high_score}", True, (255, 215, 0))
        pantalla.blit(txt_pts, (ANCHO // 2 - txt_pts.get_width() // 2, 20))
        pantalla.blit(txt_record_vivo, (15, 15))
    else:
        # Menú de reposo que lee el High Score de la computadora
        pygame.draw.rect(pantalla, (10, 8, 20), (50, ALTO//2 - 90, ANCHO - 100, 160), border_radius=8)
        pygame.draw.rect(pantalla, (255, 215, 0), (50, ALTO//2 - 90, ANCHO - 100, 160), 2, border_radius=8)
        
        txt_tit = fuente_hud.render("NEON FLAPPY BIRD", True, (0, 255, 200))
        txt_rec = fuente_menu.render(f"MÁXIMO RÉCORD: {high_score} PTS", True, (255, 215, 0))
        txt_sub = fuente_menu.render("Presiona ESPACIO para Volar", True, (255, 255, 255))
        
        pantalla.blit(txt_tit, (ANCHO//2 - txt_tit.get_width()//2, ALTO//2 - 70))
        pantalla.blit(txt_rec, (ANCHO//2 - txt_rec.get_width()//2, ALTO//2 - 15))
        pantalla.blit(txt_sub, (ANCHO//2 - txt_sub.get_width()//2, ALTO//2 + 25))

    # Control global a 60 FPS
    pygame.display.flip()
    reloj.tick(60)

