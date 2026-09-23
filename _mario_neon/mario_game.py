import pygame
import sys

# 1. Inicialización y Ventana
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Plumber - Edición Arcade Completa")
reloj = pygame.time.Clock()

# Fuentes
fuente_hud = pygame.font.SysFont("Impact", 30)
fuente_menu = pygame.font.SysFont("Impact", 60)
fuente_sub = pygame.font.SysFont("Arial", 25)

# 2. ESTADOS DEL JUEGO
# Puede ser "JUGANDO" o "GAME_OVER"
estado_juego = "JUGANDO"

# 3. Propiedades del Personaje (Mario)
mario_ancho, mario_alto = 30, 40
mario_x, mario_y = 100, ALTO - 150
mario_vel_x = 5

mario_vel_y = 0
gravedad = 0.6
fuerza_salto = -14
en_el_suelo = False

# Sistema de Vidas y Puntos
vidas_maximas = 3
vidas = vidas_maximas
puntuacion = 0
camara_x = 0

# 4. Diseño del Nivel Fijo
bloques = [
    pygame.Rect(0, ALTO - 50, 2000, 50),          # El Suelo principal
    pygame.Rect(300, ALTO - 200, 40, 40),          # Bloque flotante 1
    pygame.Rect(340, ALTO - 200, 40, 40),          # Bloque flotante 2
    pygame.Rect(380, ALTO - 200, 40, 40),          # Bloque flotante 3
    pygame.Rect(550, ALTO - 130, 60, 80),          # Tubería verde
    pygame.Rect(800, ALTO - 90, 40, 40),           # Escalera
    pygame.Rect(840, ALTO - 130, 40, 80),
    pygame.Rect(880, ALTO - 170, 40, 120),
    pygame.Rect(1000, ALTO - 280, 240, 20),        # Plataforma del Goomba
]

# Monedas coleccionables [Rectángulo, recolectada(True/False)]
monedas_originales = [
    [pygame.Rect(345, ALTO - 240, 15, 15), False],
    [pygame.Rect(572, ALTO - 170, 15, 15), False],
    [pygame.Rect(1050, ALTO - 320, 15, 15), False],
    [pygame.Rect(1100, ALTO - 320, 15, 15), False]
]
monedas = [item[:] for item in monedas_originales]

# Configuración del Enemigo [Rectángulo, Velocidad_X, Límite_Izq, Límite_Der, Vivo]
goomba_original = [pygame.Rect(1050, ALTO - 310, 30, 30), 2, 1000, 1210, True]
goomba = goomba_original[:]

# 5. FUNCIÓN DE REINICIO TOTAL
def reiniciar_partida():
    global mario_x, mario_y, mario_vel_y, vidas, puntuacion, camara_x, goomba, monedas, estado_juego
    mario_x, mario_y = 100, ALTO - 150
    mario_vel_y = 0
    vidas = vidas_maximas
    puntuacion = 0
    camara_x = 0
    goomba = [pygame.Rect(1050, ALTO - 310, 30, 30), 2, 1000, 1210, True]
    monedas = [item[:] for item in monedas_originales]
    estado_juego = "JUGANDO"

# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((14, 10, 24))
    
    # === MANEJO DE EVENTOS GENERALES ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            # Controles en estado JUGANDO
            if estado_juego == "JUGANDO":
                if (evento.key == pygame.K_SPACE or evento.key == pygame.K_UP or evento.key == pygame.K_w) and en_el_suelo:
                    mario_vel_y = fuerza_salto
                    en_el_suelo = False
            # Controles en estado GAME OVER
            elif estado_juego == "GAME_OVER":
                if evento.key == pygame.K_r:
                    reiniciar_partida()

    # ==========================================
    # === LÓGICA DEL ESTADO: GAME OVER ===
    # ==========================================
    if estado_juego == "GAME_OVER":
        # Dibujamos una cortina oscura semitransparente sobre el nivel
        superficie_oscura = pygame.Surface((ANCHO, ALTO))
        superficie_oscura.fill((5, 2, 10))
        pantalla.blit(superficie_oscura, (0, 0))
        
        # Textos del Menú de Derrota
        txt_go = fuente_menu.render("¡GAME OVER!", True, (255, 50, 50))
        txt_sub = fuente_sub.render(f"Puntuación alcanzada: {puntuacion} puntos", True, (255, 255, 255))
        txt_inst = fuente_sub.render("Presiona la tecla [ R ] para volver a intentar", True, (0, 255, 200))
        
        pantalla.blit(txt_go, (ANCHO//2 - txt_go.get_width()//2, 180))
        pantalla.blit(txt_sub, (ANCHO//2 - txt_sub.get_width()//2, 280))
        pantalla.blit(txt_inst, (ANCHO//2 - txt_inst.get_width()//2, 360))

    # ==========================================
    # === LÓGICA DEL ESTADO: JUGANDO ===
    # ==========================================
    elif estado_juego == "JUGANDO":
        # Controles
        teclas = pygame.key.get_pressed()
        movimiento_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: movimiento_x = -mario_vel_x
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: movimiento_x = mario_vel_x

        # Físicas y Caída
        mario_vel_y += gravedad
        if mario_vel_y > 15: mario_vel_y = 15 

        # Inteligencia Artificial del Goomba
        if goomba and goomba[4]:
            goomba[0].x += goomba[1]
            if goomba[0].x <= goomba[2] or goomba[0].x >= goomba[3]:
                goomba[1] *= -1

        # Colisiones en Eje X
        mario_x += movimiento_x
        rect_mario = pygame.Rect(mario_x, mario_y, mario_ancho, mario_alto)
        for bloque in bloques:
            if rect_mario.colliderect(bloque):
                if movimiento_x > 0: mario_x = bloque.left - mario_ancho
                if movimiento_x < 0: mario_x = bloque.right

        # Colisiones en Eje Y
        mario_y += mario_vel_y
        rect_mario = pygame.Rect(mario_x, mario_y, mario_ancho, mario_alto)
        en_el_suelo = False
        for bloque in bloques:
            if rect_mario.colliderect(bloque):
                if mario_vel_y > 0:
                    mario_y = bloque.top - mario_alto
                    mario_vel_y = 0
                    en_el_suelo = True
                elif mario_vel_y < 0:
                    mario_y = bloque.bottom
                    mario_vel_y = 0

        # Si caes por un abismo fuera de la pantalla (Lógica de seguridad)
        if mario_y > ALTO:
            vidas -= 1
            mario_x, mario_y = 100, ALTO - 150
            mario_vel_y = 0
            if vidas <= 0: estado_juego = "GAME_OVER"

        # Interacción y Combate con el Goomba
        rect_mario = pygame.Rect(mario_x, mario_y, mario_ancho, mario_alto)
        if goomba and goomba[4] and rect_mario.colliderect(goomba[0]):
            # Detectar si Mario cae encima de su cabeza
            if mario_vel_y > 0 and (mario_y + mario_alto - mario_vel_y) <= goomba[0].top + 10:
                goomba[4] = False     # ¡Matar Goomba!
                mario_vel_y = -10     # Rebote
                puntuacion += 50
            else:
                # Daño colateral: Perder una vida (Mejora)
                vidas -= 1
                if vidas <= 0:
                    estado_juego = "GAME_OVER"
                else:
                    # Si le quedan vidas, reaparece al inicio de la fase
                    mario_x, mario_y = 100, ALTO - 150
                    mario_vel_y = 0

        # Control de la Cámara Móvil
        if mario_x - camara_x > ANCHO // 2: camara_x = mario_x - ANCHO // 2
        if mario_x - camara_x < ANCHO // 4: camara_x = max(0, mario_x - ANCHO // 4)
        if mario_x < 0: mario_x = 0

        # Recolección de Monedas
        for moneda in monedas:
            if not moneda[1] and rect_mario.colliderect(moneda[0]):
                moneda[1] = True
                puntuacion += 10

        # === DIBUJAR ELEMENTOS ACTIVOS DEL JUEGO ===
        # 1. Dibujar escenario
        for bloque in bloques:
            rect_render = pygame.Rect(bloque.x - camara_x, bloque.y, bloque.width, bloque.height)
            pygame.draw.rect(pantalla, (25, 35, 55), rect_render)
            pygame.draw.rect(pantalla, (0, 255, 200), rect_render, 2, border_radius=3)

        # 2. Dibujar Monedas
        for moneda in monedas:
            if not moneda[1]:
                pygame.draw.circle(pantalla, (255, 215, 0), (moneda[0].centerx - int(camara_x), moneda[0].centery), 8)
                pygame.draw.circle(pantalla, (255, 255, 200), (moneda[0].centerx - int(camara_x), moneda[0].centery), 4)

        # 3. Dibujar Goomba
        if goomba and goomba[4]:
            rect_g_render = pygame.Rect(goomba[0].x - camara_x, goomba[0].y, goomba[0].width, goomba[0].height)
            pygame.draw.rect(pantalla, (80, 20, 50), rect_g_render, border_radius=5)
            pygame.draw.rect(pantalla, (255, 0, 150), rect_g_render, 2, border_radius=5)
            pygame.draw.line(pantalla, (255, 255, 255), (rect_g_render.x + 5, rect_g_render.y + 10), (rect_g_render.x + 12, rect_g_render.y + 15), 2)
            pygame.draw.line(pantalla, (255, 255, 255), (rect_g_render.x + 25, rect_g_render.y + 10), (rect_g_render.x + 18, rect_g_render.y + 15), 2)

        # 4. Dibujar a Mario
        pygame.draw.rect(pantalla, (255, 50, 50), (mario_x - camara_x, mario_y, mario_ancho, mario_alto), border_radius=4)
        pygame.draw.rect(pantalla, (255, 255, 255), (mario_x - camara_x, mario_y, mario_ancho, mario_alto), 2, border_radius=4)

        # 5. Dibujar Interfaz de Usuario (HUD)
        txt_score = fuente_hud.render(f"PUNTOS: {puntuacion}", True, (255, 255, 255))
        pantalla.blit(txt_score, (20, 20))
        
        # Dibujar iconos de corazones/vidas en la esquina superior derecha
        for i in range(vidas):
            pygame.draw.circle(pantalla, (255, 0, 80), (ANCHO - 40 - (i * 30), 35), 10)
            pygame.draw.circle(pantalla, (255, 100, 150), (ANCHO - 40 - (i * 30), 35), 5)

    # Actualización Global de pantalla
    pygame.display.flip()
    reloj.tick(60)

