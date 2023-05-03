import pygame
import random
import os

# Define game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
CAT_WIDTH = 50
CAT_HEIGHT = 50
CAT_SPEED = 5
FONT_SIZE = 32
MAX_CATS = 10
SCORE_INCREMENT = 1

# Initialize Pygame
pygame.init()

# Set up the game window
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cat Collector")

# Load game images
bg_img = pygame.image.load(os.path.join("images", "grass.jpg"))
player_img = pygame.image.load(os.path.join("images", "player.jpg"))
cat_imgs = [
    pygame.image.load(os.path.join("images", "image1.png")),
    pygame.image.load(os.path.join("images", "image2.png")),
    pygame.image.load(os.path.join("images", "image3.png"))
]
victory_img = pygame.image.load(os.path.join("images", "cheer4.jpg"))

# Load game sounds
acquire_sound = pygame.mixer.Sound(os.path.join("sound", "acquire.wav"))
win_sound = pygame.mixer.Sound(os.path.join("sound", "gem.wav"))

# Set up the font for displaying text
font = pygame.font.SysFont(None, FONT_SIZE)

# Define game variables
player_x = WINDOW_WIDTH / 2 - PLAYER_WIDTH / 2
player_y = WINDOW_HEIGHT / 2 - PLAYER_HEIGHT / 2
player_speed = 5
score = 0
cats = []
for i in range(MAX_CATS):
    cat_x = random.randint(0, WINDOW_WIDTH - CAT_WIDTH)
    cat_y = random.randint(0, WINDOW_HEIGHT - CAT_HEIGHT)
    cat_dx = random.randint(-CAT_SPEED, CAT_SPEED)
    cat_dy = random.randint(-CAT_SPEED, CAT_SPEED)
    cat_img = random.choice(cat_imgs)
    cats.append((cat_x, cat_y, cat_dx, cat_dy, cat_img))

# Define game functions
def move_player(keys):
    global player_x, player_y
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - PLAYER_WIDTH:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - PLAYER_HEIGHT:
        player_y += player_speed

def move_cats():
    global cats
    for i in range(len(cats)):
        cat_x, cat_y, cat_dx, cat_dy, cat_img = cats[i]
        cat_x += cat_dx
        cat_y += cat_dy
        if cat_x < 0 or cat_x > WINDOW_WIDTH - CAT_WIDTH:
            cat_dx = -cat_dx
        if cat_y < 0 or cat_y > WINDOW_HEIGHT - CAT_HEIGHT:
            cat_dy = -cat_dy
        cats[i] = (cat_x, cat_y, cat_dx, cat_dy, cat_img)

def check_collisions():
    global score
    for i in range(len(cats)):
        cat_x, cat_y, cat_dx, cat_dy, cat_img = cats[i]
        if (player_x < cat_x + CAT_WIDTH and
            player_x + PLAYER_WIDTH > cat_x and
            player_y < cat_y + CAT_HEIGHT and
            player_y + PLAYER_HEIGHT > cat_y):
            acquire_sound.play()
            score += SCORE_INCREMENT
            cat_x = random.randint(0, WINDOW_WIDTH - CAT_WIDTH)
            cat_y = random.randint(0, WINDOW_HEIGHT - CAT_HEIGHT)
            cat_dx = random.randint(-CAT_SPEED, CAT_SPEED)
            cat_dy = random.randint(-CAT_SPEED, CAT_SPEED)
            cat_img = random.choice(cat_imgs)
            cats[i] = (cat_x, cat_y, cat_dx, cat_dy, cat_img)

def draw_game():
    win.blit(bg_img, (0, 0))
    win.blit(player_img, (player_x, player_y))
    for cat_x, cat_y, _, _, cat_img in cats:
        win.blit(cat_img, (cat_x, cat_y))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

def draw_victory():
    win.blit(victory_img, (0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (WINDOW_WIDTH / 2 - score_text.get_width() / 2, WINDOW_HEIGHT / 2 - score_text.get_height() / 2))

def restart():
    global score, player_x, player_y, cats
    score = 0
    player_x = WINDOW_WIDTH / 2 - PLAYER_WIDTH / 2
    player_y = WINDOW_HEIGHT / 2 - PLAYER_HEIGHT / 2
    cats = []
    for i in range(MAX_CATS):
        cat_x = random.randint(0, WINDOW_WIDTH - CAT_WIDTH)
        cat_y = random.randint(0, WINDOW_HEIGHT - CAT_HEIGHT)
        cat_dx = random.randint(-CAT_SPEED, CAT_SPEED)
        cat_dy = random.randint(-CAT_SPEED, CAT_SPEED)
        cat_img = random.choice(cat_imgs)
        cats.append((cat_x, cat_y, cat_dx, cat_dy, cat_img))

# Start the game loop
running = True
victory = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                victory = False

    # Move the player
    keys = pygame.key.get_pressed()
    move_player(keys)

    # Move the cats
    move_cats()

    # Check for collisions
    check_collisions()

    # Draw the game
    if not victory:
        draw_game()
        if score == 9999:
            victory = True
            win_sound.play()
    else:
        draw_victory()

    # Update the display
    pygame.display.update()

# Clean up
pygame.quit()