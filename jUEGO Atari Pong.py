import pygame
import sys
import random

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Colores y constantes
Tamaño_pantalla = (800, 600)
Blanco = (255, 255, 255)
Negro = (0, 0, 0)
Azul_Aqua = (0, 255, 255)
Rojo = (255, 0, 0)
Ancho_jugador = 15
Alto_jugador = 90
Velocidad_maxima = 15
PUNTUACION_MAXIMA = 3

# Cargar sonidos de forma segura
try:
    sonido_rebote = pygame.mixer.Sound("PONG.wav")
except pygame.error as e:
    print(f"Error: No se pudo cargar el archivo de sonido 'PONG.wav'. Asegúrate de que está en la misma carpeta que el script.")
    print(e)
    sonido_rebote = None

# Puntuaciones
puntuacion_jugador1 = 0
puntuacion_jugador2 = 0
ganador = ""

# Fuente para el puntaje y menús
fuente_puntaje = pygame.font.Font(None, 74)
fuente_menu = pygame.font.Font(None, 100)
fuente_botones = pygame.font.Font(None, 45)

# Crear la ventana
ventana = pygame.display.set_mode((Tamaño_pantalla))
pygame.display.set_caption("Atari Pong")
Reloj = pygame.time.Clock()

# Coordenadas y velocidad del jugador 1
Jugador1_x_coor = 50
Jugador1_y_coor = 300 - 45
Jugador1_y_velocidad = 0

# Coordenadas y velocidad del jugador 2
Jugador2_x_coor = 750 - Ancho_jugador
Jugador2_y_coor = 300 - 45
Jugador2_y_velocidad = 0

# Coordenadas y velocidad de la pelota
pelota_x = 400
pelota_y = 300
pelota_velocidad_x = 3
pelota_velocidad_y = 3

# Variables de estado del juego
MENU = 0
JUGANDO = 1
FIN_DE_JUEGO = 2
estado_juego = MENU
vs_cpu = False

def reiniciar_juego():
    global puntuacion_jugador1, puntuacion_jugador2, pelota_x, pelota_y, pelota_velocidad_x, pelota_velocidad_y
    puntuacion_jugador1 = 0
    puntuacion_jugador2 = 0
    pelota_x = 400
    pelota_y = 300
    pelota_velocidad_x = random.choice([-3, 3])
    pelota_velocidad_y = random.choice([-3, 3])

def dibujar_menu():
    ventana.fill(Negro)
    titulo_juego = fuente_menu.render("Pong", True, Blanco)
    ventana.blit(titulo_juego, (Tamaño_pantalla[0] // 2 - titulo_juego.get_width() // 2, 100))
    
    # Botón Jugar 2 Jugadores
    texto_2_jugadores = fuente_botones.render("2 Jugadores", True, Blanco)
    rect_2_jugadores = pygame.Rect(Tamaño_pantalla[0] // 2 - 150, 300, 300, 75)
    pygame.draw.rect(ventana, Rojo, rect_2_jugadores)
    texto_pos_x = rect_2_jugadores.x + (rect_2_jugadores.width - texto_2_jugadores.get_width()) // 2
    ventana.blit(texto_2_jugadores, (texto_pos_x, rect_2_jugadores.y + 20))

    # Botón Jugar vs. CPU
    texto_vs_cpu = fuente_botones.render("Jugar vs CPU", True, Blanco)
    rect_vs_cpu = pygame.Rect(Tamaño_pantalla[0] // 2 - 150, 400, 300, 75)
    pygame.draw.rect(ventana, Azul_Aqua, rect_vs_cpu)
    texto_pos_x = rect_vs_cpu.x + (rect_vs_cpu.width - texto_vs_cpu.get_width()) // 2
    ventana.blit(texto_vs_cpu, (texto_pos_x, rect_vs_cpu.y + 20))
    
    return rect_2_jugadores, rect_vs_cpu

def dibujar_fin_de_juego():
    ventana.fill(Negro)
    
    # Elige el color del texto según el ganador
    if ganador == "Jugador 1":
        color_ganador = Azul_Aqua
    else:
        color_ganador = Rojo

    texto_ganador = fuente_menu.render(f"¡{ganador} gana!", True, color_ganador)
    ventana.blit(texto_ganador, (Tamaño_pantalla[0] // 2 - texto_ganador.get_width() // 2, 150))
    
    texto_puntaje_final = fuente_botones.render(f"Puntuación final: {puntuacion_jugador1} - {puntuacion_jugador2}", True, Blanco)
    ventana.blit(texto_puntaje_final, (Tamaño_pantalla[0] // 2 - texto_puntaje_final.get_width() // 2, 250))
    
    # Botones de opción
    ancho_boton = 300
    
    texto_nuevo_juego = fuente_botones.render("Jugar de nuevo", True, Negro)
    rect_nuevo_juego = pygame.Rect(Tamaño_pantalla[0] // 2 - ancho_boton // 2, 350, ancho_boton, 75)
    pygame.draw.rect(ventana, Blanco, rect_nuevo_juego)
    texto_pos_x = rect_nuevo_juego.x + (rect_nuevo_juego.width - texto_nuevo_juego.get_width()) // 2
    ventana.blit(texto_nuevo_juego, (texto_pos_x, rect_nuevo_juego.y + 20))

    texto_menu = fuente_botones.render("Menú principal", True, Negro)
    rect_menu = pygame.Rect(Tamaño_pantalla[0] // 2 - ancho_boton // 2, 450, ancho_boton, 75)
    pygame.draw.rect(ventana, Blanco, rect_menu)
    texto_pos_x = rect_menu.x + (rect_menu.width - texto_menu.get_width()) // 2
    ventana.blit(texto_menu, (texto_pos_x, rect_menu.y + 20))

    return rect_nuevo_juego, rect_menu

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # Manejar eventos según el estado del juego
        if estado_juego == MENU:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rect_2_jugadores, rect_vs_cpu = dibujar_menu()
                if rect_2_jugadores.collidepoint(pos):
                    vs_cpu = False
                    estado_juego = JUGANDO
                    reiniciar_juego()
                elif rect_vs_cpu.collidepoint(pos):
                    vs_cpu = True
                    estado_juego = JUGANDO
                    reiniciar_juego()
        
        elif estado_juego == JUGANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    Jugador1_y_velocidad = -3 
                if evento.key == pygame.K_s:
                    Jugador1_y_velocidad = 3
                # Solo el jugador 2 puede moverse si no estamos en modo CPU
                if not vs_cpu:
                    if evento.key == pygame.K_UP:
                        Jugador2_y_velocidad = -3 
                    if evento.key == pygame.K_DOWN:
                        Jugador2_y_velocidad = 3
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w or evento.key == pygame.K_s:
                    Jugador1_y_velocidad = 0
                if not vs_cpu:
                    if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        Jugador2_y_velocidad = 0
        
        elif estado_juego == FIN_DE_JUEGO:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rect_nuevo_juego, rect_menu = dibujar_fin_de_juego()
                if rect_nuevo_juego.collidepoint(pos):
                    estado_juego = JUGANDO
                    reiniciar_juego()
                elif rect_menu.collidepoint(pos):
                    estado_juego = MENU
                    reiniciar_juego()

    # Lógica del juego principal, solo se ejecuta si estamos jugando
    if estado_juego == JUGANDO:
        # Lógica de la CPU
        if vs_cpu:
            if pelota_y > Jugador2_y_coor + Alto_jugador / 2:
                Jugador2_y_velocidad = 3
            elif pelota_y < Jugador2_y_coor + Alto_jugador / 2:
                Jugador2_y_velocidad = -3
            else:
                Jugador2_y_velocidad = 0

        # Mover paletas y pelota
        Jugador1_y_coor += Jugador1_y_velocidad
        Jugador2_y_coor += Jugador2_y_velocidad

        # Limitar movimiento de paletas
        Jugador1_y_coor = max(0, min(Jugador1_y_coor, Tamaño_pantalla[1] - Alto_jugador))
        Jugador2_y_coor = max(0, min(Jugador2_y_coor, Tamaño_pantalla[1] - Alto_jugador))

        # Movimiento de la pelota
        pelota_x += pelota_velocidad_x
        pelota_y += pelota_velocidad_y
        
        # Colisión con las paredes superior e inferior
        if pelota_y > 590 or pelota_y < 10:
            pelota_velocidad_y *= -1 
        
        # Gráficos
        ventana.fill(Negro)
        
        # Dibujar las líneas del campo
        pygame.draw.rect(ventana, Blanco, (0, 0, 800, 600), 5) # Bordes del campo
        pygame.draw.aaline(ventana, Blanco, (400, 0), (400, 600)) # Línea central

        Jugador1_rect = pygame.draw.rect(ventana, Azul_Aqua, (Jugador1_x_coor, Jugador1_y_coor, Ancho_jugador, Alto_jugador))
        Jugador2_rect = pygame.draw.rect(ventana, Rojo, (Jugador2_x_coor, Jugador2_y_coor, Ancho_jugador, Alto_jugador))
        pelota_rect = pygame.draw.circle(ventana, Blanco, (pelota_x, pelota_y), 10)
        
        # Lógica de colisión con las paletas
        if pelota_rect.colliderect(Jugador1_rect) or pelota_rect.colliderect(Jugador2_rect):
            pelota_velocidad_x *= -1
            if sonido_rebote:
                sonido_rebote.play()

            # Aceleración después de la colisión
            if pelota_velocidad_x > 0:
                pelota_velocidad_x += 0.5
            else:
                pelota_velocidad_x -= 0.5
            if pelota_velocidad_y > 0:
                pelota_velocidad_y += 0.5
            else:
                pelota_velocidad_y -= 0.5

            # Límite de velocidad
            if abs(pelota_velocidad_x) > Velocidad_maxima:
                pelota_velocidad_x = Velocidad_maxima if pelota_velocidad_x > 0 else -Velocidad_maxima
            if abs(pelota_velocidad_y) > Velocidad_maxima:
                pelota_velocidad_y = Velocidad_maxima if pelota_velocidad_y > 0 else -Velocidad_maxima

        # Lógica de puntuación
        if pelota_x > 800:
            puntuacion_jugador1 += 1
            pelota_x = 400
            pelota_y = 300
            pelota_velocidad_x = -3
            pelota_velocidad_y = 3

        if pelota_x < 0:
            puntuacion_jugador2 += 1
            pelota_x = 400
            pelota_y = 300
            pelota_velocidad_x = 3
            pelota_velocidad_y = 3
        
        # Puntuación en pantalla
        texto_puntuacion = fuente_puntaje.render(f"{puntuacion_jugador1} | {puntuacion_jugador2}", True, Blanco)
        texto_rect = texto_puntuacion.get_rect(center=(Tamaño_pantalla[0] // 2, 50))
        ventana.blit(texto_puntuacion, texto_rect)
        
        # Condición de victoria
        if puntuacion_jugador1 >= PUNTUACION_MAXIMA or puntuacion_jugador2 >= PUNTUACION_MAXIMA:
            estado_juego = FIN_DE_JUEGO
            if puntuacion_jugador1 > puntuacion_jugador2:
                ganador = "Jugador 1"
            else:
                ganador = "Jugador 2"

    elif estado_juego == MENU:
        dibujar_menu()
    
    elif estado_juego == FIN_DE_JUEGO:
        dibujar_fin_de_juego()

    pygame.display.flip()
    Reloj.tick(60)

pygame.quit()
sys.exit()
