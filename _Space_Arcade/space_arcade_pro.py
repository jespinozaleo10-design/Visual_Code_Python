import pygame
import random
import sys
import math
import os

# 1. Inicialización y Ventana
pygame.init()
pygame.mixer.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mega Space Shooter 2026 - Edición Premium")
reloj = pygame.time.Clock()

# 2. ESTADOS DEL JUEGO
estado_juego = "MENU"
fuente_titulo = pygame.font.SysFont("Impact", 50)
fuente_normal = pygame.font.SysFont("Arial", 25)

# Archivo Local para el High Score
ARCHIVO_RECORD = "high_score.txt"

# Función para cargar el récord desde el archivo local
def cargar_high_score():
    if os.path.exists(ARCHIVO_RECORD):
        try:
            with open(ARCHIVO_RECORD, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

# Función para guardar el récord en el archivo local
def guardar_high_score(nuevo_record):
    try:
        with open(ARCHIVO_RECORD, "w") as f:
            f.write(str(nuevo_record))
    except:
        pass

# Cargar récord inicial
high_score = cargar_high_score()

# 3. Propiedades del Jugador
jugador_x = ANCHO // 2
jugador_y = ALTO - 80
jugador_vel = 7
arma_nivel = 1
temporizador_poder = 0
# Variables para el Jefe Final
jefe_activo = False
jefe_x = ANCHO // 2 - 60
jefe_y = -100  # Inicia arriba, fuera de pantalla para hacer una entrada épica
jefe_vel_x = 3
jefe_vida_max = 50
jefe_vida = jefe_vida_max
temporizador_disparo_jefe = 0

jugador_escudo_max = 3
jugador_escudo = jugador_escudo_max  # Inicia con vida completa

# Estructuras de Datos
balas = []
enemigos = []
poderes = []
puntuacion = 0
temporizador_enemigo = 0

# 4. FUNCIONES DE AUDIO (Generador de tonos retro de 8-bits)
def reproducir_sonido_retro(tipo):
    try:
        sample_rate = 22050
        duracion = 0.1 if tipo == "disparo" else 0.3
        num_samples = int(sample_rate * duracion)
        buf = bytearray(num_samples)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            frecuencia = (800 - i * 2) if tipo == "disparo" else (200 + random.randint(-50, 50))
            val = int(127.0 * math.sin(2.0 * math.pi * frecuencia * t))
            buf[i] = max(0, min(255, val + 128))
            
        sound = pygame.mixer.Sound(buffer=buf)
        sound.set_volume(0.05)
        sound.play()
    except:
        pass

# 5. DIBUJAR ALIENS CON CÓDIGO
def dibujar_alien(superficie, x, y, tipo, vida_actual, vida_max):
    if tipo == 1:
        color = (100, 255, 100)
        puntos_dibujo = [(x+15, y), (x, y+30), (x+30, y+30)]
    elif tipo == 2:
        color = (255, 165, 0)
        puntos_dibujo = [(x, y), (x+30, y), (x+30, y+30), (x, y+30)]
    else:
        color = (255, 0, 100)
        puntos_dibujo = [(x+15, y), (x+30, y+15), (x+15, y+30), (x, y+15)]

    pygame.draw.polygon(superficie, color, puntos_dibujo)
    
    # Barra de vida del Alien
    ancho_barra = 30
    ancho_vida = int(ancho_barra * (vida_actual / vida_max))
    pygame.draw.rect(superficie, (50, 50, 50), (x, y - 8, ancho_barra, 4))
    pygame.draw.rect(superficie, (0, 255, 0), (x, y - 8, ancho_vida, 4))

# 6. FUNCIÓN DE REINICIO
def reiniciar_juego():
    global jugador_x, jugador_y, arma_nivel, balas, enemigos, poderes, puntuacion, estado_juego, jugador_escudo
    global jefe_activo, jefe_x, jefe_y, jefe_vida
    jugador_x = ANCHO // 2
    jugador_y = ALTO - 80
    arma_nivel = 1
    jugador_escudo = jugador_escudo_max
    balas.clear()
    enemigos.clear()
    poderes.clear()
    puntuacion = 0
    # Reiniciar Jefe
    jefe_activo = False
    jefe_x = ANCHO // 2 - 60
    jefe_y = -100
    jefe_vida = jefe_vida_max
    estado_juego = "JUGANDO"


# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((10, 10, 25))
    
    # === ESTADO: MENÚ DE INICIO ===
    if estado_juego == "MENU":
        texto_tit = fuente_titulo.render("SPACE ARCADE PRO", True, (0, 255, 200))
        texto_inst = fuente_normal.render("Presiona ENTER para comenzar a Jugar", True, (255, 255, 255))
        texto_rec = fuente_normal.render(f"RÉCORD MÁXIMO: {high_score} PTS", True, (255, 215, 0))
        
        pantalla.blit(texto_tit, (ANCHO//2 - texto_tit.get_width()//2, 150))
        pantalla.blit(texto_inst, (ANCHO//2 - texto_inst.get_width()//2, 280))
        pantalla.blit(texto_rec, (ANCHO//2 - texto_rec.get_width()//2, 350))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                estado_juego = "JUGANDO"

    # === ESTADO: GAME OVER ===
    elif estado_juego == "GAME_OVER":
        texto_go = fuente_titulo.render("¡GAME OVER!", True, (255, 50, 50))
        texto_sc = fuente_normal.render(f"Puntuación Lograda: {puntuacion}", True, (255, 255, 255))
        texto_hi = fuente_normal.render(f"Récord Máximo Actual: {high_score}", True, (255, 215, 0))
        texto_re = fuente_normal.render("Presiona R para VOLVER A INTENTARLO", True, (0, 255, 200))
        
        pantalla.blit(texto_go, (ANCHO//2 - texto_go.get_width()//2, 150))
        pantalla.blit(texto_sc, (ANCHO//2 - texto_sc.get_width()//2, 250))
        pantalla.blit(texto_hi, (ANCHO//2 - texto_hi.get_width()//2, 310))
        pantalla.blit(texto_re, (ANCHO//2 - texto_re.get_width()//2, 390))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                reiniciar_juego()

    # === ESTADO: JUGANDO ===
    elif estado_juego == "JUGANDO":
        temporizador_enemigo += 1
        if arma_nivel > 1:
            temporizador_poder -= 1
            if temporizador_poder <= 0: arma_nivel = 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                reproducir_sonido_retro("disparo")
                if arma_nivel == 1:
                    balas.append(pygame.Rect(jugador_x + 22, jugador_y, 6, 15))
                elif arma_nivel == 2:
                    balas.append(pygame.Rect(jugador_x + 5, jugador_y, 6, 15))
                    balas.append(pygame.Rect(jugador_x + 40, jugador_y, 6, 15))
                elif arma_nivel >= 3:
                    balas.append(pygame.Rect(jugador_x + 5, jugador_y, 6, 15))
                    balas.append(pygame.Rect(jugador_x + 22, jugador_y - 5, 6, 15))
                    balas.append(pygame.Rect(jugador_x + 40, jugador_y, 6, 15))

        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jugador_x > 0: jugador_x -= jugador_vel
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jugador_x < ANCHO - 50: jugador_x += jugador_vel

        for b in balas[:]:
            b.y -= 9
            if b.y < 0: balas.remove(b)

        # --- ACTIVACIÓN DEL JEFE FINAL ---
        if puntuacion >= 500 and not jefe_activo and jefe_vida > 0:
            jefe_activo = True
            enemigos.clear() # Limpiar la pantalla de aliens normales para el jefe

        # --- GENERACIÓN DE ENEMIGOS NORMALES (Solo si el jefe no está activo) ---
        if not jefe_activo and jefe_vida > 0:
            if temporizador_enemigo >= 35:
                x_ali = random.randint(0, ANCHO - 40)
                tipo_random = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
                if tipo_random == 1:   datos = [pygame.Rect(x_ali, -40, 30, 30), 1, 1, 1, 4]
                elif tipo_random == 2: datos = [pygame.Rect(x_ali, -40, 30, 30), 2, 3, 3, 2.5]
                else:                  datos = [pygame.Rect(x_ali, -40, 30, 30), 3, 6, 6, 1.5]
                enemigos.append(datos)
                temporizador_enemigo = 0

        # --- LÓGICA EXCLUSIVA DEL JEFE FINAL ---
        if jefe_activo:
            # 1. Entrada épica (baja lentamente hasta y=60)
            if jefe_y < 60:
                jefe_y += 2
            else:
                # 2. Movimiento lateral oscilatorio
                jefe_x += jefe_vel_x
                if jefe_x <= 20 or jefe_x >= ANCHO - 140:
                    jefe_vel_x *= -1
                
                # 3. Ataque del Jefe: Dispara asteroides hacia abajo
                temporizador_disparo_jefe += 1
                if temporizador_disparo_jefe >= 25: # Dispara rápido
                    # Crea un asteroide que cae desde la posición del jefe
                    enemigos.append([pygame.Rect(jefe_x + 50, jefe_y + 40, 25, 25), 1, 1, 1, 5])
                    reproducir_sonido_retro("explosion") # Sonido de alerta de disparo
                    temporizador_disparo_jefe = 0

        # Mover Aliens y Asteroides normales
        rect_jugador = pygame.Rect(jugador_x, jugador_y, 50, 50)
        for ali in enemigos[:]:
            rect_ali, tipo, vida, vida_max, vel = ali
            rect_ali.y += vel
            if rect_ali.y > ALTO: enemigos.remove(ali)
            elif rect_ali.colliderect(rect_jugador):
                reproducir_sonido_retro("explosion")
                enemigos.remove(ali)
                jugador_escudo -= 1
                if jugador_escudo <= 0:
                    if puntuacion > high_score: high_score = puntuacion; guardar_high_score(high_score)
                    estado_juego = "GAME_OVER"

        # --- IMPACTO DE TUS BALAS CONTRA EL JEFE ---
        rect_jefe = pygame.Rect(jefe_x, jefe_y, 120, 50)
        for b in balas[:]:
            if jefe_activo and b.colliderect(rect_jefe):
                balas.remove(b)
                jefe_vida -= 1
                reproducir_sonido_retro("disparo") # Feedback de golpe
                
                if jefe_vida <= 0:
                    jefe_activo = False
                    puntuacion += 500 # Súper bonificación por ganar
                    if puntuacion > high_score: high_score = puntuacion; guardar_high_score(high_score)
                    # Aquí podrías poner un estado de "VICTORIA", por ahora sigue el juego infinito

            

        
        # Lógica de Impacto / Colisión de Enemigos contra la Nave
        rect_jugador = pygame.Rect(jugador_x, jugador_y, 50, 50)
        for ali in enemigos[:]:
            rect_ali, tipo, vida, vida_max, vel = ali
            rect_ali.y += vel
            
            if rect_ali.y > ALTO: 
                enemigos.remove(ali)
            elif rect_ali.colliderect(rect_jugador):
                reproducir_sonido_retro("explosion")
                enemigos.remove(ali)
                jugador_escudo -= 1  # Reducir vida/escudo de la nave (Mejora 1)
                
                if jugador_escudo <= 0:
                    # Verificar si superó el High Score antes de perder
                    if puntuacion > high_score:
                        high_score = puntuacion
                        guardar_high_score(high_score)
                    estado_juego = "GAME_OVER"

        # Lógica de Superpoderes flotantes (Drops)
        for pod in poderes[:]:
            rect_pod, tipo_p = pod
            rect_pod.y += 3
            if rect_pod.y > ALTO:
                poderes.remove(pod)
            elif rect_pod.colliderect(rect_jugador):
                arma_nivel = min(3, arma_nivel + 1)
                temporizador_poder = 400
                poderes.remove(pod)

        # Impactos de Balas contra Enemigos
        for b in balas[:]:
            for ali in enemigos[:]:
                rect_ali, tipo, vida, vida_max, vel = ali
                if b.colliderect(rect_ali):
                    if b in balas: balas.remove(b)
                    ali[2] -= 1  # Restar vida interna del Alien
                    
                    if ali[2] <= 0:
                        reproducir_sonido_retro("explosion")
                        if random.random() < 0.25:
                            poderes.append([pygame.Rect(rect_ali.x, rect_ali.y, 20, 20), "PowerUp"])
                        
                        puntuacion += tipo * 10
                        enemigos.remove(ali)
                    break

        # ---- DIBUJAR ELEMENTOS ----
        color_b = (0, 255, 255) if arma_nivel == 1 else (255, 215, 0)
        for b in balas: pygame.draw.rect(pantalla, color_b, b)

        for pod in poderes:
            pygame.draw.circle(pantalla, (255, 0, 255), (pod[0].x+10, pod[0].y+10), 10)

        for ali in enemigos:
            # 3. Dibujar al Jefe Final si está activo
            if jefe_activo:
                # Cuerpo de la Nave Nodriza Gigante (Polígono de 5 lados)
                puntos_jefe = [
                    (jefe_x + 60, jefe_y + 50),  # Punta inferior
                    (jefe_x, jefe_y + 20),       # Ala izquierda
                    (jefe_x + 20, jefe_y),       # Esquina superior izq
                    (jefe_x + 100, jefe_y),      # Esquina superior der
                    (jefe_x + 120, jefe_y + 20)  # Ala derecha
                ]
                pygame.draw.polygon(pantalla, (255, 0, 128), puntos_jefe) # Fucsia neón imponente
                pygame.draw.polygon(pantalla, (255, 255, 255), puntos_jefe, 2) # Borde blanco de escudo
                
                # BARRA DE VIDA GIGANTE DEL JEFE (En el centro superior de la pantalla)
                pygame.draw.rect(pantalla, (60, 20, 20), (ANCHO // 2 - 200, 20, 400, 15), border_radius=5)
                ancho_vida_jefe = int(400 * (jefe_vida / jefe_vida_max))
                pygame.draw.rect(pantalla, (255, 0, 50), (ANCHO // 2 - 200, 20, ancho_vida_jefe, 15), border_radius=5)
                
                txt_jefe = fuente_normal.render("BOSS: NAVE NODRIZA DESTROYER", True, (255, 255, 255))
                pantalla.blit(txt_jefe, (ANCHO // 2 - txt_jefe.get_width() // 2, 40))

            dibujar_alien(pantalla, ali[0].x, ali[0].y, ali[1], ali[2], ali[3])

        # Nave del Jugador
        puntos_nave = [(jugador_x + 25, jugador_y), (jugador_x, jugador_y + 40), (jugador_x + 50, jugador_y + 40)]
        pygame.draw.polygon(pantalla, (0, 255, 200), puntos_nave)
        if arma_nivel > 1:
            pygame.draw.polygon(pantalla, (255, 0, 255), puntos_nave, 3)

        # INTERFAZ DE USUARIO (HUD)
        # Barra de Escudo del Jugador (Mejora 1)
        pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO - 160, 15, 140, 20), border_radius=3)
        ancho_escudo_actual = int(140 * (jugador_escudo / jugador_escudo_max))
        color_escudo = (0, 255, 150) if jugador_escudo > 1 else (255, 50, 50)
        pygame.draw.rect(pantalla, color_escudo, (ANCHO - 160, 15, ancho_escudo_actual, 20), border_radius=3)
        
        txt_esc = fuente_normal.render("ESCUDO", True, (255, 255, 255))
        pantalla.blit(txt_esc, (ANCHO - 260, 12))

        # Puntuaciones en vivo
        txt_pts = fuente_normal.render(f"Puntos: {puntuacion}", True, (255, 255, 255))
        txt_hsc = fuente_normal.render(f"Récord: {high_score}", True, (255, 215, 0))
        pantalla.blit(txt_pts, (10, 10))
        pantalla.blit(txt_hsc, (10, 40))
        
        if arma_nivel > 1:
            txt_pdr = fuente_normal.render(f"¡SUPERPODER ACTIVO! NIVEL {arma_nivel}", True, (255, 0, 255))
            pantalla.blit(txt_pdr, (10, 70))

    # === Cierre correcto del bucle principal (Fuera del IF de juego, alineado al inicio) ===
    pygame.display.flip()
    reloj.tick(60)
