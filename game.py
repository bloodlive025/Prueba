import pygame
from background import Background
from MeteoriteManager import MeteoriteManager
from players import Player
from coin import Coin

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player1 = Player()
        self.player2 = Player()
        self.meteorite_manager = MeteoriteManager(10)
        self.collision_count_p1 = 0  # Contador de colisiones para el jugador 1
        self.collision_count_p2 = 0  # Contador de colisiones para el jugador 2
        self.coins = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 36)  # Fuente por defecto, tamaño 36
        self.start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio del juego


        for _ in range(3):
            coin = Coin()
            self.coins.add(coin)

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.handle_input()
            self.update()
            self.draw()

            self.clock.tick(60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player1.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.player1.move(5, 0)
        if keys[pygame.K_a]:
            self.player2.move(-5, 0)
        if keys[pygame.K_d]:
            self.player2.move(5, 0)

    def update(self):
        self.meteorite_manager.update()
        self.coins.update()

        self.player1.update()
        self.player2.update()
        # Verificar colisiones para ambos jugadores
        collisions_p1 = self.meteorite_manager.check_collisions(self.player1)
        collisions_p2 = self.meteorite_manager.check_collisions(self.player2)

        # Contar colisiones para el jugador 1
        if collisions_p1:
            for meteorite in collisions_p1:
                meteorite.reset_position()  # Reinicia la posición del meteorito
                self.collision_count_p1 += 1  # Incrementa el contador de colisiones
                print(f"Colisiones Jugador 1: {self.collision_count_p1}")  # Imprimir contador

        # Contar colisiones para el jugador 2
        if collisions_p2:
            for meteorite in collisions_p2:
                meteorite.reset_position()  # Reinicia la posición del meteorito
                self.collision_count_p2 += 1  # Incrementa el contador de colisiones
                print(f"Colisiones Jugador 2: {self.collision_count_p2}")  # Imprimir contador


    

    def draw(self):
        self.player1.image = pygame.image.load('sprites/cohete1.png')
        self.player2.image = pygame.image.load('sprites/cohete2.png')
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.player1.image, self.player1.rect)
        self.screen.blit(self.player2.image, self.player2.rect)

        self.meteorite_manager.draw(self.screen)
        
        # Mostrar contadores de colisiones
        font = pygame.font.Font(None, 36)
        text_p1 = font.render(f"Colisiones P1: {self.collision_count_p1}", True, (255, 255, 255))
        text_p2 = font.render(f"Colisiones P2: {self.collision_count_p2}", True, (255, 255, 255))
        
        self.screen.blit(text_p1, (10, 10))  # Dibuja el texto para el jugador 1
        self.screen.blit(text_p2, (10, 40))  # Dibuja el texto para el jugador 2


        self.coins.draw(self.screen)
        self.display_time()
        pygame.display.flip()
    
    
    def display_time(self):
        # Calcular el tiempo en segundos desde que comenzó el juego
        current_time = pygame.time.get_ticks() - self.start_time
        seconds = current_time // 1000  # Convertir a segundos

        # Renderizar el texto con la fuente
        time_text = self.font.render(f"Tiempo: {seconds} s", True, (255, 255, 255))  # Texto en blanco

        # Dibujar el texto en la esquina superior izquierda
        self.screen.blit(time_text, (10, 10))


    # Creacion del menu

    def main_menu(self):
        runing = True
        while runing:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 1 es el botón izquierdo del ratón
                        # Obtener la posición del clic
                        mouse_pos = pygame.mouse.get_pos()
                        # Verificar si el clic ocurrió dentro del área del botón
                        if self.buttom_rect_start.collidepoint(mouse_pos):
                            # entra al juego directamente
                            self.loop()
                            # cerramos si cierras la ventana en loop
                            runing = False
                            print("¡Botón de inicio clicado!")
                        if self.buttom_rect_off.collidepoint(mouse_pos):
                            # cerramos la ventana
                            runing = False
                            print("¡Botón de salida clicado!")

    def draw_menu(self): 
        pygame.display.set_caption("Menú de Juego")
        # Colores
        BLACK = (0, 0, 0)
        # Fuentes
        font = pygame.font.Font(None, 74)
        font_small = pygame.font.Font(None, 36)

        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Cargando las imágenes
        title_menu = pygame.image.load("sprites/boton_menu.png")
        buttom_start = pygame.image.load("sprites/boton_start.png")
        buttom_off = pygame.image.load("sprites/boton_off.png")

        # Crear un rectángulo a partir de la imagen del botón
        self.buttom_rect_start = buttom_start.get_rect()  # Hacemos self para acceder a este rectángulo desde main_menu
        self.buttom_rect_start.topleft = (330, 270)  # Posición del botón en la pantalla
        self.buttom_rect_off = buttom_off.get_rect()  # Igual para este botón
        self.buttom_rect_off.topleft = (380, 350)

        # Dibujar el texto menú y botones en la pantalla
        self.screen.blit(title_menu, (280, 100))
        self.screen.blit(buttom_start, self.buttom_rect_start.topleft)
        self.screen.blit(buttom_off, self.buttom_rect_off.topleft)

        pygame.display.flip()

