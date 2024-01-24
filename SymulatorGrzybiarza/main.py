import pygame
import sys
import random
import buttona
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
mushroom_lifetime = 2
total_game_time = 60
total_game_time_str = ''
character = pygame.image.load('teem.png')
background = pygame.image.load('grass.png')
font = pygame.font.Font(None, 36)
# Dodaj ścieżki do obrazów punktów
mushroom_images = ['muchomor2.png', 'grzyb11.png', 'grzyb2.png']
temp_score = 0
# Inicjalizacja listy obiektów punktów
mushrooms = []
images = []
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
options_bg = pygame.image.load('bg3.png').convert_alpha()
resume_button = button.Button(240, 190, resume_img, 0.5)
options_button = button.Button(130, 190, options_img, 0.5)
append_mushroom()
game_paused = True
menu_state = "main"
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
start_time2 = None
start_time3 = None
input_rect = pygame.Rect(200, 200, 200, 32)
color = pygame.Color('green')
maxtemp = 0
#pętla gry
while not exit_game:
    screen.blit(background, (0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (385, 10))
    start_time3 = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    game_paused = True
            if event.key == pygame.K_BACKSPACE:
                total_game_time_str = total_game_time_str[:-1]
            elif event.key == pygame.K_RETURN:
                try:
                    total_game_time = int(total_game_time_str)
                except:
                    print("Zły czas")
                game_paused = True
                menu_state = "main"
            else:
                total_game_time_str += event.unicode
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_size:
        player_y += player_speed
    # sprawdzenie czy weszliśmy w grzyba
    for mushroom in mushrooms:
        if player_x < mushroom['x'] < player_x + player_size and \
            player_y < mushroom['y'] < player_y + player_size:
            start_time2 = time.time()
            if  mushroom['type'] == 'muchomor2.png':
                score -= 1
                player_speed = player_speed * 0.5
            elif mushroom['type'] == 'grzyb11.png':
                score +=1
                collision_sound.play()
                player_speed = player_speed * 1.5
            else:
                score += 1
                collision_sound.play()

            mushrooms.remove(mushroom)
            append_mushroom()

    mushrooms_to_remove = []
    for mushroom in mushrooms:
        if 'spawn_time' not in mushroom:
            #czas od wejścia w grzyba
            mushroom['spawn_time'] = time.time()
        elif time.time() - mushroom['spawn_time'] >= mushroom_lifetime:
            mushrooms_to_remove.append(mushroom)

    for mushroom in mushrooms_to_remove:
        mushrooms.remove(mushroom)
        append_mushroom()

    if start_time2 is not None and time.time() - start_time2 >= 1:
        player_speed = 5
        start_time2 = None

    # dodanie postaci na ekran
    add_character_at_location(player_x, player_y)

    # dodanie obiektów punktów na ekranie
    for mushroom in mushrooms:
        add_mushroom_at_location(mushroom)

    # Wyświetl wynik
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))

    screen.blit(score_text, (385, 10))
    if score>= maxtemp:
        maxtemp = score
    if game_paused == True:

        score = 0
        player_size = 50
        player_x = width // 2 - player_size // 2
        player_y = height // 2 - player_size // 2
        player_speed = 5
        elapsed_time2 = pygame.time.get_ticks()
        seconds2 = elapsed_time2 / 1000
        if menu_state == "main":
            #tło menu
            screen.blit(menu_img, (0, 0))

            score_text2 = font.render(f"Best score: {maxtemp}", True, (255, 255, 255))
            screen.blit(score_text2, (178, 75))

            total_game_time_str = ''

            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
        #opcje
        if menu_state == "options":
            screen.blit(menu_img, (0, 0))
            pygame.draw.rect(screen, color, input_rect)
            text_surface2 = font.render(total_game_time_str, False, (255, 255, 255))
            screen.blit(text_surface2, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(100, text_surface2.get_width() + 10)
            draw_text("Time: ", font, (255, 255, 255), 120, 203)

    else:
        elapsed_time = pygame.time.get_ticks()
        seconds = elapsed_time / 1000 - seconds2
        #powrót do menu po upływie czasu podanego przez użytkownika
        if seconds >= total_game_time:
            game_paused = True
            menu_state = "main"


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
