<<<<<<< HEAD
# 🎮 Colección de Videojuegos 2D en Python (Pygame)

¡Bienvenido a mi repositorio de desarrollo de videojuegos! Este espacio reúne mis primeros proyectos prácticos creados en **Python** utilizando la librería avanzada **Pygame CE (Community Edition)**. El objetivo principal de este repositorio es consolidar conceptos clave de programación como el manejo del tiempo, físicas aplicadas, colisiones avanzadas y persistencia de datos local.

---

## 🚀 Proyectos Incluidos

### 1. Space Shooter 2D: Edición Premium
Un shooter de estilo arcade retro con colores neón que implementa un sistema dinámico de oleadas, superpoderes incrementales y un combate contra un jefe final.

*   **Mecánicas Avanzadas:** 
    *   **Sistema de Vidas y Escudos:** El jugador cuenta con una barra de escudo interactiva que le permite tolerar hasta 3 colisiones directas.
    *   **Armamento Evolutivo (Power-ups):** Los enemigos derrotados tienen probabilidad de soltar cápsulas que transforman el disparo simple en ráfagas dobles y triples.
    *   **IA de Enemigos Dinámica:** 3 tipos de aliens con diferentes dimensiones, velocidades de descenso y puntos de salud ponderados.
    *   **Boss Fight:** Al superar los 500 puntos, se activa el Jefe Final (Nave Nodriza) con su propia barra de vida masiva de 50 impactos.

### 2. Neon Flappy Bird: Simulación Física
Un clon del mítico Flappy Bird diseñado con una estética limpia cyberpunk, enfocado en el aprendizaje de fuerzas físicas gravitatorias y escenarios en movimiento.

*   **Mecánicas Avanzadas:**
    *   **Gravedad Artificial Realista:** El personaje experimenta una aceleración constante en el eje Y que simula el peso del mundo real, contrarrestado por impulsos de vectores negativos al saltar.
    *   **Inclinación Basada en Velocidad:** El sprite del personaje rota dinámicamente en base a su velocidad física actual (apunta hacia el cielo al saltar y cae en picada al descender).
    *   **Fondo Dinámico con Efecto Parallax:** Multi-capas de estrellas que viajan a diferentes velocidades independientes para dar una ilusión de profundidad tridimensional.

---

## 💾 Características Técnicas Globales

*   **Persistencia Local (High Scores):** Ambos juegos incluyen un sistema automatizado de persistencia de datos que lee y escribe archivos planos localmente (`high_score.txt` y `flappy_high_score.txt`) para mantener guardado tu récord histórico, incluso al cerrar el juego.
*   **Audio Sintético de 8-Bits:** Los efectos de sonido láser y explosiones son generados en tiempo real mediante algoritmos matemáticos senoidales que interactúan directamente con el canal de audio del sistema de forma asíncrona.
*   **Optimización del Game Loop:** Estructurados firmemente para procesar eventos, actualizar posiciones y renderizar texturas de forma controlada a 60 FPS estables.

---

## 🛠️ Instalación y Configuración Local

Para ejecutar estos juegos en tu computadora, asegúrate de tener instalado Python y sigue estos pasos desde tu terminal:

1. Clonar este repositorio:
   ```bash
   git clone https://github.com
   ```
2. Acceder al directorio del proyecto:
   ```bash
   cd mis-primeros-juegos-python
   ```
3. Instalar la dependencia del motor gráfico:
   ```bash
   pip install pygame-ce
   ```
4. Ejecutar el juego de tu preferencia:
   ```bash
   # Para jugar el Shooter Espacial:
   python 🚀_Space_Arcade/space_arcade_pro.py

   # Para jugar Flappy Bird:
   python 🐦_Flappy_Neon/flappy_bird_neon.py
   ```

---

## 🧠 Aprendizajes Clave obtenidos
*   Control estricto de estructuras de datos (listas internas y diccionarios para la gestión de proyectiles y enemigos).
*   Lógica asíncrona para la simulación del tiempo en ciclos repetitivos.
*   Manejo y depuración del sistema de control de versiones con **Git y GitHub**.

Desarrollado con ❤️ por **José Espinoza** como parte de mi ruta de aprendizaje en Python.
=======
# Visual_Code_Python
PythonCode
>>>>>>> 36c488a15c14922533d39b24abe3c66e5edb6af8
