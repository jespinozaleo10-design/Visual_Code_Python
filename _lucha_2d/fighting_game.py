import pygame
import sys
import random

# 1. Inicialización y Ventana
pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Fighter 2D - Puño (J) y Patada Baja (K)")
reloj = pygame.time.Clock()

# Fuentes
fuente_hud = pygame.font.SysFont("Impact", 25)
fuente_menu = pygame.font.SysFont("Impact", 60)

# 2. CONFIGURACIÓN DE LOS LUCHADORES
j1 = {
    "x": 150, "y": ALTO - 150, "ancho": 40, "alto": 90,
    "vel_x": 6, "vida": 100, "vida_max": 100,
    "estado": "QUIETO", # QUIETO, CAMINANDO, PUÑO, PATADA, HIT
    "timer_ataque": 0, "timer_hit": 0, "direccion": 1
}

j2 = {
    "x": 600, "y": ALTO - 150, "ancho": 40, "alto": 90,
    "vel_x": 4, "vida": 100, "vida_max": 100,
    "estado": "QUIETO",
    "timer_ataque": 0, "timer_hit": 0, "direccion": -1
}

COLOR_J1 = (0, 255, 200)   # Cian Neón
COLOR_J2 = (255, 0, 128)   # Fucsia Neón
SUELO_Y = ALTO - 60

# 3. LÓGICA DE CONTROL DE LA IA (Rival dinámico)
def actualizar_ia(rival, objetivo):
    if rival["estado"] in ["QUIETO", "CAMINANDO"]:
        distancia = objetivo["x"] - rival["x"]
        rival["direccion"] = 1 if distancia > 0 else -1
        
        # Persecución básica
        if abs(distancia) > 85:
            rival["estado"] = "CAMINANDO"
            rival["x"] += rival["vel_x"] * rival["direccion"]
        else:
            # La IA elige aleatoriamente entre lanzar un puño o una patada de largo alcance
            if random.random() < 0.06:
                eleccion = random.choice(["PUÑO", "PATADA"])
                rival["estado"] = eleccion
                rival["timer_ataque"] = 15 if eleccion == "PUÑO" else 20

# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((12, 10, 22))

    # === CAPTURA DE EVENTOS (Controles J1) ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if (j1["vida"] <= 0 or j2["vida"] <= 0) and evento.key == pygame.K_RETURN:
                j1["vida"], j2["vida"] = 100, 100
                j1["x"], j2["x"] = 150, 600
                j1["estado"], j2["estado"] = "QUIETO", "QUIETO"

            # TECLA J: Puñetazo Rápido
            if evento.key == pygame.K_j and j1["estado"] in ["QUIETO", "CAMINANDO"]:
                j1["estado"] = "PUÑO"
                j1["timer_ataque"] = 15 

            # TECLA K: Patada Baja Avanzada (Mejora)
            if evento.key == pygame.K_k and j1["estado"] in ["QUIETO", "CAMINANDO"]:
                j1["estado"] = "PATADA"
                j1["timer_ataque"] = 20 # Más lento y pesado

    # === LÓGICA DE JUEGO ===
    if j1["vida"] > 0 and j2["vida"] > 0:
        
        # Movimiento J1
        teclas = pygame.key.get_pressed()
        if j1["estado"] in ["QUIETO", "CAMINANDO"]:
            moviendo = False
            if teclas[pygame.K_a]:
                j1["x"] -= j1["vel_x"]
                j1["direccion"] = -1
                moviendo = True
            if teclas[pygame.K_d]:
                j1["x"] += j1["vel_x"]
                j1["direccion"] = 1
                moviendo = True
            j1["estado"] = "CAMINANDO" if moviendo else "QUIETO"

        # IA Rival
        actualizar_ia(j2, j1)

        # --- TIMERS Y MAQUINA DE ESTADOS ---
        # Jugador 1
        if j1["estado"] in ["PUÑO", "PATADA"]:
            j1["timer_ataque"] -= 1
            if j1["timer_ataque"] <= 0: j1["estado"] = "QUIETO"
        elif j1["estado"] == "HIT":
            j1["timer_hit"] -= 1
            if j1["timer_hit"] <= 0: j1["estado"] = "QUIETO"

        # Jugador 2
        if j2["estado"] in ["PUÑO", "PATADA"]:
            j2["timer_ataque"] -= 1
            if j2["timer_ataque"] <= 0: j2["estado"] = "QUIETO"
        elif j2["estado"] == "HIT":
            j2["timer_hit"] -= 1
            if j2["timer_hit"] <= 0: j2["estado"] = "QUIETO"

        # --- DETECCIÓN DE GOLPES (HITBOXES ADAPTATIVAS) ---
        
        # ¿J1 impacta a J2?
        if j1["estado"] == "PUÑO" and j1["timer_ataque"] == 8:
            hitbox = pygame.Rect(j1["x"] + (j1["ancho"] if j1["direccion"] == 1 else -40), j1["y"] + 20, 40, 20)
            if hitbox.colliderect(pygame.Rect(j2["x"], j2["y"], j2["ancho"], j2["alto"])):
                j2["vida"] = max(0, j2["vida"] - 12); j2["estado"] = "HIT"; j2["timer_hit"] = 12; j2["x"] += 15 * j1["direccion"]
                
        elif j1["estado"] == "PATADA" and j1["timer_ataque"] == 10: # Conecta en el cuadro medio de 20
            # Hitbox más larga (65px de alcance) posicionada a nivel del suelo (y + 65)
            hitbox = pygame.Rect(j1["x"] + (j1["ancho"] if j1["direccion"] == 1 else -65), j1["y"] + 65, 65, 20)
            if hitbox.colliderect(pygame.Rect(j2["x"], j2["y"], j2["ancho"], j2["alto"])):
                j2["vida"] = max(0, j2["vida"] - 18); j2["estado"] = "HIT"; j2["timer_hit"] = 15; j2["x"] += 35 * j1["direccion"] # Más empuje

        # ¿J2 impacta a J1?
        if j2["estado"] == "PUÑO" and j2["timer_ataque"] == 8:
            hitbox = pygame.Rect(j2["x"] + (j2["ancho"] if j2["direccion"] == 1 else -40), j2["y"] + 20, 40, 20)
            if hitbox.colliderect(pygame.Rect(j1["x"], j1["y"], j1["ancho"], j1["alto"])):
                j1["vida"] = max(0, j1["vida"] - 10); j1["estado"] = "HIT"; j1["timer_hit"] = 12; j1["x"] += 15 * j2["direccion"]
                
        elif j2["estado"] == "PATADA" and j2["timer_ataque"] == 10:
            hitbox = pygame.Rect(j2["x"] + (j2["ancho"] if j2["direccion"] == 1 else -65), j2["y"] + 65, 65, 20)
            if hitbox.colliderect(pygame.Rect(j1["x"], j1["y"], j1["ancho"], j1["alto"])):
                j1["vida"] = max(0, j1["vida"] - 15); j1["estado"] = "HIT"; j1["timer_hit"] = 15; j1["x"] += 30 * j2["direccion"]

        # Límites
        j1["x"] = max(0, min(ANCHO - j1["ancho"], j1["x"]))
        j2["x"] = max(0, min(ANCHO - j2["ancho"], j2["x"]))

    # === RENDERIZADO VISUAL ===
    pygame.draw.line(pantalla, (40, 40, 60), (0, SUELO_Y), (ANCHO, SUELO_Y), 4)

    # HUD Barras de Vida
    pygame.draw.rect(pantalla, (60, 20, 20), (40, 30, 300, 20), border_radius=3)
    pygame.draw.rect(pantalla, COLOR_J1, (40, 30, int(300 * (j1["vida"] / j1["vida_max"])), 20), border_radius=3)
    pygame.draw.rect(pantalla, (60, 20, 20), (ANCHO - 340, 30, 300, 20), border_radius=3)
    pygame.draw.rect(pantalla, COLOR_J2, (ANCHO - 40 - int(300 * (j2["vida"] / j2["vida_max"])), 30, int(300 * (j2["vida"] / j2["vida_max"])), 20), border_radius=3)
    pantalla.blit(fuente_hud.render("VS", True, (255, 255, 255)), (ANCHO//2 - 15, 25))

    # Renderizar J1
    color_actual_j1 = (255, 50, 50) if j1["estado"] == "HIT" else COLOR_J1
    pygame.draw.rect(pantalla, color_actual_j1, (j1["x"], j1["y"], j1["ancho"], j1["alto"]), border_radius=4)
    if j1["estado"] == "PUÑO":
        pygame.draw.rect(pantalla, color_actual_j1, (j1["x"] + (j1["ancho"] if j1["direccion"] == 1 else -30), j1["y"] + 20, 30, 15))
    elif j1["estado"] == "PATADA":
        # Dibujar pierna extendida abajo
        pygame.draw.rect(pantalla, color_actual_j1, (j1["x"] + (j1["ancho"] if j1["direccion"] == 1 else -50), j1["y"] + 65, 50, 15))

    # Renderizar J2 (IA)
    color_actual_j2 = (255, 50, 50) if j2["estado"] == "HIT" else COLOR_J2
    pygame.draw.rect(pantalla, color_actual_j2, (j2["x"], j2["y"], j2["ancho"], j2["alto"]), border_radius=4)
    if j2["estado"] == "PUÑO":
        pygame.draw.rect(pantalla, color_actual_j2, (j2["x"] + (j2["ancho"] if j2["direccion"] == 1 else -30), j2["y"] + 20, 30, 15))
    elif j2["estado"] == "PATADA":
        pygame.draw.rect(pantalla, color_actual_j2, (j2["x"] + (j2["ancho"] if j2["direccion"] == 1 else -50), j2["y"] + 65, 50, 15))

    # Pantalla de Fin de Combate
    if j1["vida"] <= 0 or j2["vida"] <= 0:
        texto = "¡VICTORIA JUGADOR 1!" if j2["vida"] <= 0 else "¡VICTORIA COMPUTADORA!"
        pantalla.blit(fuente_menu.render(texto, True, COLOR_J1 if j2["vida"] <= 0 else COLOR_J2), (ANCHO//2 - 260, ALTO//2 - 50))
        pantalla.blit(fuente_hud.render("Presiona ENTER para revancha", True, (255, 255, 255)), (ANCHO//2 - 140, ALTO//2 + 30))

    pygame.display.flip()
    reloj.tick(60)
