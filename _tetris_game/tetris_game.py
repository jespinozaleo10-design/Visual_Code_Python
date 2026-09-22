import pygame
import random
import sys

# 1. Inicialización y Configuración Gráfica
pygame.init()
LADO_BLOQUE = 30  # Tamaño en píxeles de cada cuadrado del Tetris
FILAS, COLUMNAS = 20, 10
ANCHO_PANEL = 200 # Espacio lateral para la puntuación
ANCHO, ALTO = (COLUMNAS * LADO_BLOQUE) + ANCHO_PANEL, FILAS * LADO_BLOQUE

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Tetris - Dominando Matrices")
reloj = pygame.time.Clock()

fuente = pygame.font.SysFont("Impact", 30)

# Colores Neón para las Piezas (Índice corresponde al tipo de pieza)
COLORES = [
    (15, 12, 28),     # 0: Fondo oscuro de la cuadrícula
    (0, 255, 255),    # 1: Cian (Pieza I)
    (255, 215, 0),    # 2: Amarillo (Pieza O)
    (255, 0, 128),    # 3: Fucsia (Pieza T)
    (0, 255, 100),    # 4: Verde (Pieza S)
    (255, 50, 50),    # 5: Rojo (Pieza Z)
    (0, 100, 255),    # 6: Azul (Pieza J)
    (255, 165, 0)     # 7: Naranja (Pieza L)
]

# 2. DEFINICIÓN DE PIEZAS (Formas en matrices de coordenadas relativas)
FORMAS = [
    [[1, 5, 9, 13], [4, 5, 6, 7]], # I
    [[1, 2, 5, 6]],                # O
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]], # T
    [[1, 2, 4, 5], [1, 5, 6, 10]], # S
    [[0, 1, 5, 6], [2, 5, 6, 9]],  # Z
    [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 8, 9], [0, 4, 5, 6]], # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]] # L
]

class Pieza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(0, len(FORMAS) - 1)
        self.color_idx = self.tipo + 1
        self.rotacion = 0

    def obtener_imagen(self):
        return FORMAS[self.tipo][self.rotacion]

# 3. FUNCIONES DE LÓGICA DE MATRIZ
def crear_matriz_tablero():
    # Crea una cuadrícula vacía de 20x10 llena de ceros
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

def validar_colision(tablero, pieza):
    for pos in pieza.obtener_imagen():
        # Calcular posición absoluta en el tablero
        pos_x = (pos % 4) + pieza.x
        pos_y = (pos // 4) + pieza.y
        
        # Verificar límites laterales e inferior
        if pos_x < 0 or pos_x >= COLUMNAS or pos_y >= FILAS:
            return True
        # Verificar colisión con bloques ya fijados en la matriz (valores mayores a 0)
        if pos_y >= 0 and tablero[pos_y][pos_x] > 0:
            return True
    return False

def fijar_pieza_en_matriz(tablero, pieza):
    for pos in pieza.obtener_imagen():
        pos_x = (pos % 4) + pieza.x
        pos_y = (pos // 4) + pieza.y
        if pos_y >= 0:
            tablero[pos_y][pos_x] = pieza.color_idx

def eliminar_filas_llenas(tablero):
    filas_eliminadas = 0
    for y in range(FILAS - 1, -1, -1):
        # Si la fila no contiene ningún cero, significa que está completamente llena
        if 0 not in tablero[y]:
            del tablero[y] # Borrar la lista de esa fila de la matriz
            # Insertar una nueva fila vacía (llena de ceros) arriba del todo
            tablero.insert(0, [0 for _ in range(COLUMNAS)])
            filas_eliminadas += 1
    return filas_eliminadas

# 4. CONFIGURACIÓN INICIAL DEL JUEGO
tablero = crear_matriz_tablero()
pieza_actual = Pieza(COLUMNAS // 2 - 2, 0)
puntuacion = 0
temporizador_caida = 0
velocidad_caida = 30 # Cuantos fotogramas tarda en bajar una casilla

# ---- BUCLE PRINCIPAL ----
while True:
    pantalla.fill((10, 8, 20))
    temporizador_caida += 1

    # === CAPTURA DE EVENTOS (Controles) ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                pieza_actual.x -= 1
                if validar_colision(tablero, pieza_actual): pieza_actual.x += 1
            if evento.key == pygame.K_RIGHT:
                pieza_actual.x += 1
                if validar_colision(tablero, pieza_actual): pieza_actual.x -= 1
            if evento.key == pygame.K_DOWN:
                pieza_actual.y += 1
                if validar_colision(tablero, pieza_actual): pieza_actual.y -= 1
            if evento.key == pygame.K_UP:
                # Rotar la pieza cambiando el índice de su matriz interna
                antigua_rotacion = pieza_actual.rotacion
                pieza_actual.rotacion = (pieza_actual.rotacion + 1) % len(FORMAS[pieza_actual.tipo])
                if validar_colision(tablero, pieza_actual):
                    pieza_actual.rotacion = antigua_rotacion # Deshacer si choca

    # === GRAVEDAD DE LA PIEZA (Caida automática) ===
    if temporizador_caida >= velocidad_caida:
        pieza_actual.y += 1
        if validar_colision(tablero, pieza_actual):
            pieza_actual.y -= 1
            fijar_pieza_en_matriz(tablero, pieza_actual)
            
            # Procesar si se completaron líneas y sumar puntos
            lineas = eliminar_filas_llenas(tablero)
            puntuacion += lineas * 100
            
            # Generar una nueva pieza arriba
            pieza_actual = Pieza(COLUMNAS // 2 - 2, 0)
            
            # Si la nueva pieza aparece colisionando, es Game Over
            if validar_colision(tablero, pieza_actual):
                tablero = crear_matriz_tablero() # Reiniciar tablero
                puntuacion = 0
        temporizador_caida = 0

    # === RENDERIZADO VISUAL ===
    # 1. Dibujar el tablero fijo (Leyendo los números de la matriz)
    for y in range(FILAS):
        for x in range(COLUMNAS):
            valor_casilla = tablero[y][x]
            rect_bloque = pygame.Rect(x * LADO_BLOQUE, y * LADO_BLOQUE, LADO_BLOQUE, LADO_BLOQUE)
            pygame.draw.rect(pantalla, COLORES[valor_casilla], rect_bloque)
            # Dibujar cuadrícula fina de fondo
            pygame.draw.rect(pantalla, (25, 20, 45), rect_bloque, 1)

    # 2. Dibujar la pieza activa que va cayendo
    for pos in pieza_actual.obtener_imagen():
        pos_x = (pos % 4) + pieza_actual.x
        pos_y = (pos // 4) + pieza_actual.y
        if pos_y >= 0:
            rect_bloque_act = pygame.Rect(pos_x * LADO_BLOQUE, pos_y * LADO_BLOQUE, LADO_BLOQUE, LADO_BLOQUE)
            pygame.draw.rect(pantalla, COLORES[pieza_actual.color_idx], rect_bloque_act)
            pygame.draw.rect(pantalla, (255, 255, 255), rect_bloque_act, 1) # Borde de brillo

    # 3. Panel de Información Lateral (HUD)
    pygame.draw.line(pantalla, (0, 255, 255), (COLUMNAS * LADO_BLOQUE, 0), (COLUMNAS * LADO_BLOQUE, ALTO), 3)
    txt_score_tit = fuente.render("PUNTOS", True, (0, 255, 255))
    txt_score_val = fuente.render(str(puntuacion), True, (255, 255, 255))
    pantalla.blit(txt_score_tit, (COLUMNAS * LADO_BLOQUE + 40, 50))
    pantalla.blit(txt_score_val, (COLUMNAS * LADO_BLOQUE + 40, 100))

    pygame.display.flip()
    reloj.tick(60)
