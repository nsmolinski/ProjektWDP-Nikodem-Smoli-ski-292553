import pygame
import sys
import random
import button
import time
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
collision_sound = pygame.mixer.Sound('collectcoin.mp3')
collision_sound.set_volume(0.5)
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulator Grzybiarza")

player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 5

character = pygame.image.load('teem.png')
background = pygame.image.load('grass.png')
font = pygame.font.Font(None, 36)
# Dodaj ścieżki do obrazów punktów
mushroom_images = ['muchomor2.png', 'grzyb11.png', 'grzyb2.png']

# Inicjalizacja listy obiektów punktów
mushrooms = []
images = []

def display_time():
    current_time = pygame.time.get_ticks()
    time_surf = font.render(current_time, False, (64, 64, 64))
    time_rect = time_surf.get_rect(center = (400, 50))
    screen.blit(time_surf, time_rect)
def add_character_at_location(x, y):
    screen.blit(character, (x, y))

def add_mushroom_at_location(mushroom):
    screen.blit(mushroom['image'], (mushroom['x'], mushroom['y']))
def append_mushroom():
    mushroom_x = random.randint(50, width - 50)
    mushroom_y = random.randint(50, height - 50)
    a = random.choice(mushroom_images)
    mushroom_image = pygame.image.load(a)
    mushrooms.append({'x': mushroom_x, 'y': mushroom_y, 'image': mushroom_image, 'type': a})
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def draw_image(image_path, x, y):
    image = pygame.image.load(image_path)
    screen.blit(image, (x, y))
exit_game = False
score = 0
resume_img = pygame.image.load('play.png').convert_alpha()
menu_img = pygame.image.load('bg.png').convert_alpha()
options_img = pygame.image.load('settings.png').convert_alpha()
resume_button = button.Button(240, 190, resume_img, 0.5)
options_button = button.Button(130, 190, options_img, 0.5)
append_mushroom()
game_paused = True
menu_state = "main"
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
while not exit_game:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_size:
        player_y += player_speed

    # Check collision with mushroom objects
    for mushroom in mushrooms:
        if player_x < mushroom['x'] < player_x + player_size and \
            player_y < mushroom['y'] < player_y + player_size:
            if  mushroom['type'] == 'muchomor2.png':
                score -= 1
            else:
                score += 1
                collision_sound.play()

            mushrooms.remove(mushroom)
            append_mushroom()
    # Wypełnij ekran obrazem tła


    # Dodaj postać na ekranie
    add_character_at_location(player_x, player_y)

    # Dodaj obiekty punktów na ekranie
    for mushroom in mushrooms:
        add_mushroom_at_location(mushroom)

    # Wyświetl wynik
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (385, 10))
    if game_paused == True:
        score = 0
        player_size = 50
        player_x = width // 2 - player_size // 2
        player_y = height // 2 - player_size // 2
        player_speed = 5
        elapsed_time2 = pygame.time.get_ticks()
        seconds2 = elapsed_time2 / 1000
        if menu_state == "main":
            screen.blit(menu_img, (0, 0))
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
        if menu_state == "options":
            print("options")
    else:
        elapsed_time = pygame.time.get_ticks()
        seconds = elapsed_time / 1000 - seconds2
        text_surface = font.render("{:.2f}".format(seconds), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(30, 20))
        screen.blit(text_surface, text_rect)
        draw_text("Press ESC - Main Menu", font, (255, 255, 255), 120, 460)
    # Odśwież ekran
    pygame.display.flip()

    # Kontrola liczby klatek na sekundę
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
