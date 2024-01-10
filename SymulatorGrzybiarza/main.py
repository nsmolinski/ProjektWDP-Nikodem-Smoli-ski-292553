import pygame
import sys
import random

pygame.init()

width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulator Grzybiarza")

player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 5

character = pygame.image.load('teem.png')
background = pygame.image.load('grass.png')

# Dodaj ścieżki do obrazów punktów
mushroom_images = ['muchomor.png', 'muchomor.png', 'muchomor.png']

# Inicjalizacja listy obiektów punktów
mushrooms = []

for _ in range(5):  # Ilość obiektów punktów na ekranie
    mushroom_x = random.randint(50, width - 50)
    mushroom_y = random.randint(50, height - 50)
    mushroom_image = pygame.image.load(random.choice(mushroom_images))
    mushrooms.append({'x': mushroom_x, 'y': mushroom_y, 'image': mushroom_image})

def add_character_at_location(x, y):
    screen.blit(character, (x, y))

def add_mushroom_at_location(mushroom):
    screen.blit(mushroom['image'], (mushroom['x'], mushroom['y']))

exit_game = False
score = 0

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_size:
        player_y += player_speed

    # Sprawdź kolizję z obiektami punktów
    for mushroom in mushrooms:
        if player_x < mushroom['x'] < player_x + player_size and \
           player_y < mushroom['y'] < player_y + player_size:
            score += 1
            mushrooms.remove(mushroom)

    # Wypełnij ekran obrazem tła
    screen.blit(background, (0, 0))

    # Dodaj postać na ekranie
    add_character_at_location(player_x, player_y)

    # Dodaj obiekty punktów na ekranie
    for mushroom in mushrooms:
        add_mushroom_at_location(mushroom)

    # Wyświetl wynik
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Odśwież ekran
    pygame.display.flip()

    # Kontrola liczby klatek na sekundę
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
