import pygame
import random

# Inicijaliziraj pygame
pygame.init()

# Postavi dimenzije prozora
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Postavi naslov prozora
pygame.display.set_caption("Flappy Beer")

# Definiraj boje
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# Postavi fontove
font = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 25)

# Učitaj sliku ptice
bird_image = pygame.image.load('bird.jpg')
bird_image = pygame.transform.scale(bird_image, (50, 35))

# Učitaj sliku pozadine
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Funkcija za prikaz poruke
def message(msg, color, y_displace=0):
    text = font.render(msg, True, color)
    screen.blit(text, [screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 + y_displace])

# Funkcija za prikaz informacija o igri
def game_info():
    info = True
    while info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    info = False

        screen.blit(background_image, (0, 0))
        message("Poštovani, cilj ove igre", white, -100)
        message("je što duže izbjegavati", white, -50)
        message("plaćanje računa u birtiji.", white, 0)
        message("Press Enter to go back", white, 100)
        pygame.display.update()

# Funkcija za prikaz glavnog menija
def main_menu(highscore):
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                if event.key == pygame.K_i:
                    game_info()

        screen.blit(background_image, (0, 0))
        message("Flappy Beer", white, -100)
        message(f"Highscore: {highscore}", white, -50)
        message("Press Space to Play", white, 50)
        message("Press I for Info", white, 100)
        pygame.display.update()

# Definiraj klasu za igru
class FlappyBird:
    def __init__(self):
        self.bird_x = 50
        self.bird_y = screen_height // 2
        self.bird_width = 50  # Adjusted to match the scaled image
        self.bird_height = 35 # Adjusted to match the scaled image
        self.bird_vel_y = 0
        self.gravity = 0.5
        self.flap_strength = -10
        self.pipes = []
        self.pipe_width = 70
        self.pipe_gap = 200
        self.pipe_speed = 5
        self.spawn_pipe()
        self.score = 0

    def spawn_pipe(self):
        pipe_height = random.randint(100, 400)
        self.pipes.append({'x': screen_width, 'height': pipe_height})

    def move_bird(self):
        self.bird_vel_y += self.gravity
        self.bird_y += self.bird_vel_y

    def flap(self):
        self.bird_vel_y = self.flap_strength

    def move_pipes(self):
        for pipe in self.pipes:
            pipe['x'] -= self.pipe_speed

    def draw_bird(self):
        screen.blit(bird_image, (self.bird_x, self.bird_y))

    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(screen, green, [pipe['x'], 0, self.pipe_width, pipe['height']])
            pygame.draw.rect(screen, green, [pipe['x'], pipe['height'] + self.pipe_gap, self.pipe_width, screen_height - pipe['height'] - self.pipe_gap])
            text = small_font.render("Računi", True, black)
            screen.blit(text, (pipe['x'] + (self.pipe_width - text.get_width()) // 2, pipe['height'] - text.get_height()))
            text = small_font.render("- $", True, black)
            screen.blit(text, (pipe['x'] + (self.pipe_width - text.get_width()) // 2, pipe['height'] + self.pipe_gap))

    def check_collision(self):
        if self.bird_y < 0 or self.bird_y + self.bird_height > screen_height:
            return True

        for pipe in self.pipes:
            if pipe['x'] < self.bird_x + self.bird_width and pipe['x'] + self.pipe_width > self.bird_x:
                if self.bird_y < pipe['height'] or self.bird_y + self.bird_height > pipe['height'] + self.pipe_gap:
                    return True
        return False

    def remove_offscreen_pipes(self):
        self.pipes = [pipe for pipe in self.pipes if pipe['x'] + self.pipe_width > 0]

    def update_score(self):
        for pipe in self.pipes:
            if pipe['x'] + self.pipe_width < self.bird_x and not pipe.get('scored'):
                self.score += 1
                pipe['scored'] = True

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, white)
        screen.blit(score_text, [10, 10])

    def restart(self):
        self.__init__()

# Inicijaliziraj igru
game = FlappyBird()

# Postavi frame rate
clock = pygame.time.Clock()
FPS = 60

# Početni highscore
highscore = 0

# Prikazi glavni meni prije pocetka igre
main_menu(highscore)

# Glavna petlja igre
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    game.restart()
                    game_over = False
                else:
                    game.flap()
            if event.key == pygame.K_m and game_over:
                main_menu(highscore)
                game.restart()
                game_over = False

    if not game_over:
        game.move_bird()
        game.move_pipes()
        game.remove_offscreen_pipes()
        game.update_score()

        if len(game.pipes) == 0 or game.pipes[-1]['x'] < screen_width - 300:
            game.spawn_pipe()

        if game.check_collision():
            game_over = True
            if game.score > highscore:
                highscore = game.score

    # Boji ekran sa slikom pozadine
    screen.blit(background_image, (0, 0))

    # Crta pticu i cijevi
    game.draw_bird()
    game.draw_pipes()
    game.draw_score()

    if game_over:
        message("Game Over!", white, -50)
        message("Press Space to Restart", white, 50)
        message("Press M for Main Menu", white, 100)

    # Osvježi ekran
    pygame.display.flip()

    # Ograniči frame rate
    clock.tick(FPS)

# Zatvori pygame
pygame.quit()
