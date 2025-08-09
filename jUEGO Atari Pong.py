# Python y Pygame
import pygame

# Inicializar Pygame
pygame.init()

# Colores y constantes
Tamaño_pantalla = (800, 600)
Blanco = (255, 255, 255)
Negro = (0, 0, 0)
Azul_Aqua = (0, 255, 255)
Rojo = (255, 0, 0)
Ancho_jugador = 15
Alto_jugador = 90

# Crear la ventana
ventana = pygame.display.set_mode((Tamaño_pantalla))
pygame.display.set_caption("Atari Pong")
Reloj = pygame. time.Clock()
#Coordenadas y velocidad del jugador 1
Jugador1_x_coor = 50
Jugador1_y_coor = 300 - 45
Jugador1_y_velocidad = 0

#Coordenadas y velocidad del jugador 2
Jugador2_x_coor = 750 - Ancho_jugador
Jugador2_y_coor = 300 - 45
Jugador2_y_velocidad = 0

#Coordenadas de la pelota
pelota_x = 400
pelota_y = 300
pelota_velocidad_x = 3
pelota_velocidad_y = 3

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    
    ventana.fill(Negro)
    #Graficos
    Jugador1 = pygame.draw.rect(ventana, Azul_Aqua, (Jugador1_x_coor, Jugador1_y_coor, Ancho_jugador, Alto_jugador))
    Jugador2 = pygame.draw.rect(ventana, Rojo, (Jugador2_x_coor, Jugador2_y_coor, Ancho_jugador, Alto_jugador))
    pelota = pygame.draw.circle(ventana, Blanco, (pelota_x, pelota_y), 10)
    pygame.display.flip()
    Reloj.tick(60)        

pygame.quit()