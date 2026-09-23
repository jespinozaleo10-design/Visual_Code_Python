import pygame
import sys
import random

# 1. Inicialización y Ventana
pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Pong Pro - Vectores e IA de Seguimiento")
reloj = pygame.time.Clock()

# Fuentes y Colores
fuente_hud = pygame.font.SysFont("Impact", 40)
fuente_sub = pygame.font.SysFont("Arial", 20)

COLOR_J1 = (0, 255, 200)    # Cian Neón
COLOR_IA = (255, 0, 128)    # Fucsia Neón
COLOR_BOLA = (255, 255, 255)

# 2. PROPIEDADES DE LAS ENTIDADES
# Jugador 1 (Izquierda)
j1_x, j1_y = 30, ALTO // 2 - 50
j1_ancho, j1_alto_base = 15, 90
j1_alto = j1_alto_base
j1_vel = 7

# IA Enemiga (Derecha)
ia_x, ia_y = ANCHO - 45, ALTO // 2 - 50
ia_ancho, ia_alto = 15, 90
ia_vel = 4.5  # Velocidad controlada para que sea ganable

# Pelota Física (Vectores de posición y velocidad)
bola_x, bola_y = ANCHO // 2, ALTO // 2
bola_radio = 10
bola_vel_x = random.choice([-5, 5])
bola_vel_y = random.choice([-3, 3])

# Marcador
puntos_j1 = 0
puntos_ia = 0

# 3. CONFIGURACIÓN DE BLOQUES DE SUPERPODER
# Ponemos 3 bloques brillantes en el centro del campo
bloques_poder = [
    {"rect": pygame.Rect(ANCHO // 2 - 10, 100, 20, 40), "activo": True},
    {"rect": pygame.Rect(ANCHO // 2 - 10, 230, 20, 40), "activo": True},
    {"rect": pygame.Rect(ANCHO // 2 - 10, 360, 20, 40), "activo": True}
]
superpoder_activo = False
timer_superpoder = 0

# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((12, 10, 22)) # Fondo oscuro espacial

    # === CAPTURA DE EVENTOS (Controles del Jugador) ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if (puntos_j1 >= 5 or puntos_ia >= 5) and evento.key == pygame.K_RETURN:
                puntos_j1, puntos_ia = 0, 0
                bola_x, bola_y = ANCHO // 2, ALTO // 2
                bola_vel_x, bola_vel_y = random.choice([-5, 5]), random.choice([-3, 3])

    # === LÓGICA DEL JUEGO (Solo si nadie ha llegado a 5 puntos) ===
    if puntos_j1 < 5 and puntos_ia < 5:
        
        # --- MOVIMIENTO DEL JUGADOR 1 (W / S) ---
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and j1_y > 10:
            j1_y -= j1_vel
        if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and j1_y < ALTO - j1_alto - 10:
            j1_y += j1_vel

        # --- INTELIGENCIA ARTIFICIAL (IA de Seguimiento Suave) ---
        # La paleta de la IA calcula el centro de la bola y se mueve suavemente hacia él
        centro_ia = ia_y + ia_alto // 2
        if bola_vel_x > 0: # La IA solo reacciona cuando la bola va hacia su lado
            if centro_ia < bola_y and ia_y < ALTO - ia_alto - 10:
                ia_y += ia_vel
            elif centro_ia > bola_y and ia_y > 10:
                ia_y -= ia_vel

        # --- MOVIMIENTO DE LA PELOTA (Aplicando Vectores) ---
        bola_x += bola_vel_x
        bola_y += bola_vel_y

        # Rebotes contra Techo y Suelo
        if bola_y - bola_radio <= 0 or bola_y + bola_radio >= ALTO:
            bola_vel_y *= -1

        # --- LÓGICA DE SUPERPODERES (Temporizador) ---
        if superpoder_activo:
            timer_superpoder -= 1
            if timer_superpoder <= 0:
                j1_alto = j1_alto_base # El poder expira, la paleta vuelve al tamaño normal
                superpoder_activo = False

        # --- DETECCIÓN DE REBOTES EN LAS PALETAS (Físicas Angulares) ---
        rect_bola = pygame.Rect(bola_x - bola_radio, bola_y - bola_radio, bola_radio * 2, bola_radio * 2)
        rect_j1 = pygame.Rect(j1_x, j1_y, j1_ancho, j1_alto)
        rect_ia = pygame.Rect(ia_x, ia_y, ia_ancho, ia_alto)

        # Rebote en Jugador 1
        if rect_bola.colliderect(rect_j1) and bola_vel_x < 0:
            bola_vel_x *= -1.05  # Aumenta un 5% la velocidad con cada golpe para dar emoción
            # Calcular en qué parte de la paleta pegó para cambiar el ángulo vertical
            impacto_relativo = (bola_y - (j1_y + j1_alto // 2)) / (j1_alto // 2)
            bola_vel_y = impacto_relativo * 5

        # Rebote en la IA
        if rect_bola.colliderect(rect_ia) and bola_vel_x > 0:
            bola_vel_x *= -1.05
            impacto_relativo = (bola_y - (ia_y + ia_alto // 2)) / (ia_alto // 2)
            bola_vel_y = impacto_relativo * 5

        # --- COLISIÓN CON BLOQUES DE PODER ---
        for bloque in bloques_poder:
            if bloque["activo"] and rect_bola.colliderect(bloque["rect"]):
                bloque["activo"] = False # Destruir bloque
                bola_vel_x *= -1         # Rebotar la bola
                
                # Activar Súper Escudo / Paleta Gigante para J1 si él golpeó último
                if bola_vel_x > 0:
                    superpoder_activo = True
                    j1_alto = j1_alto_base * 1.6 # Agrandar la paleta un 60%
                    timer_superpoder = 350       # Duración del poder

        # --- ANOTACIÓN DE PUNTOS (Límites Laterales) ---
        if bola_x < 0:
            puntos_ia += 1
            # Resetear bola
            bola_x, bola_y = ANCHO // 2, ALTO // 2
            bola_vel_x = 5
            bola_vel_y = random.choice([-3, 3])
        elif bola_x > ANCHO:
            puntos_j1 += 1
            bola_x, bola_y = ANCHO // 2, ALTO // 2
            bola_vel_x = -5
            bola_vel_y = random.choice([-3, 3])

    # === RENDERIZADO VISUAL ===
    # 1. Dibujar línea central divisoria estética
    pygame.draw.line(pantalla, (25, 25, 40), (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

    # 2. Dibujar Bloques de Poder (Si están activos)
    for bloque in bloques_poder:
        if bloque["activo"]:
            pygame.draw.rect(pantalla, (255, 215, 0), bloque["rect"], border_radius=4)
            pygame.draw.rect(pantalla, (255, 255, 255), bloque["rect"], 1, border_radius=4)

    # 3. Dibujar Paletas Neón
    pygame.draw.rect(pantalla, COLOR_J1, (j1_x, j1_y, j1_ancho, j1_alto), border_radius=4) # J1
    pygame.draw.rect(pantalla, COLOR_IA, (ia_x, ia_y, ia_ancho, ia_alto), border_radius=4) # IA

    # Aura brillante si tienes el superpoder activo
    if superpoder_activo:
        pygame.draw.rect(pantalla, (255, 255, 255), (j1_x, j1_y, j1_ancho, j1_alto), 2, border_radius=4)

    # 4. Dibujar Pelota
    pygame.draw.circle(pantalla, COLOR_BOLA, (int(bola_x), int(bola_y)), bola_radio)

    # 5. Marcador Superior fijo (HUD)
    txt_j1 = fuente_hud.render(str(puntos_j1), True, COLOR_J1)
    txt_ia = fuente_hud.render(str(puntos_ia), True, COLOR_IA)
    pantalla.blit(txt_j1, (ANCHO // 2 - 80, 20))
    pantalla.blit(txt_ia, (ANCHO // 2 + 50, 20))

    # Pantalla de Fin de Juego
    if puntos_j1 >= 5 or puntos_ia >= 5:
        ganador = "¡Felicidades, ganaste!" if puntos_j1 >= 5 else "La Inteligencia Artificial gana"
        color_win = COLOR_J1 if puntos_j1 >= 5 else COLOR_IA
        
        txt_win = fuente_hud.render(ganador, True, color_win)
        txt_rst = fuente_sub.render("Presiona [ ENTER ] para una revancha", True, (255, 255, 255))
        
        pantalla.blit(txt_win, (ANCHO // 2 - txt_win.get_width() // 2, ALTO // 2 - 40))
        pantalla.blit(txt_rst, (ANCHO // 2 - txt_rst.get_width() // 2, ALTO // 2 + 30))

    pygame.display.flip()
    reloj.tick(60)
