""" Import Libraries """
import random
from random import choice
import pickle
import math
import os
import pygame
from pygame import mixer

# Total #

if os.path.exists("total.pkl"):
    with open("total.pkl", "rb") as f:
        number = pickle.load(f)

else:
    number = 0


# Start mixer
mixer.init()
acquire = mixer.Sound("sound/acquire.wav")
win_song = mixer.Sound("sound/gem.wav")

# Hard set values #
score = 0
level = 1
FPS = 60

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
cats_total = random.randint(4, 7)

# Functions


def generate_cats():
    """ Generate cats """

    global images
    global image_rects
    global player_x, player_y

    images = []
    image_rects = []

    # get the set of all possible x-coordinates
    all_x = set(range(0, 1180))

    # get the set of x-coordinates that are occupied by the player
    player_x_range = range(player_x, player_x + player_width)
    player_x_set = set(player_x_range)

    # get the set of x-coordinates that are available for the image_rect
    image_x_set = all_x - player_x_set

    # repeat the same process for y-coordinates
    all_y = set(range(0, 620))
    player_y_range = range(player_y, player_y + player_height)
    player_y_set = set(player_y_range)
    image_y_set = all_y - player_y_set

    for i in range(1, cats_total):
        image = pygame.image.load(f"images/image{random.randint(1, 3)}.png")
        image_rect = image.get_rect()

        # choose a random x-coordinate from the image_x_set
        image_rect.x = choice(list(image_x_set))

        # choose a random y-coordinate from the image_y_set
        image_rect.y = choice(list(image_y_set))

        images.append(image)
        image_rects.append(image_rect)


def update_score():
    """ Update the score """
    global number  # Declare number as global
    with open("total.pkl", "wb") as f:
        pickle.dump(number, f)  # Save number to pickle file


def restart():
    """ Restart """

    global score, level, cats_total, background
    global text, player_x, player_y, level_text

    background = pygame.image.load(f"images/bg{random.randint(1, 10)}.jpg")
    cats_total = random.randint(4, 7)
    level += 1

    score = 0
    player_x = win.get_width() // 2 - player_width // 2
    player_y = win.get_height() // 2 - player_height // 2
    # Load the images and generate their random positions
    generate_cats()
    text = font.render(f"Kettir náðir: {score}", True, (255, 255, 255))
    win.blit(text, text_rect)
    level_text = font.render(
        f"Level: {level}", True,
        (255, 255, 255),
    )


# Setja upp playarea #
pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("FLOTTASTI LEIKUR IN THE WORLD")

# Backgrounds #
background = pygame.image.load(f"images/bg0.jpg")
win.blit(background, (0, 0))

# Win background
random_number = random.randint(0, 4)
image_path = (f"images/cheer{random_number}.jpg")

# All text and buttons #

# Create fonts
font = pygame.font.SysFont("Arial", 32)
font1 = pygame.font.SysFont("Arial", 62)

# Create cats collected constant text
text = font.render(f"Kettir náðir: {score}", True, (255, 255, 255))
text_rect = text.get_rect()
text_rect.center = (640, 600)
win.blit(text, text_rect)

# Create level counter
level_text = font.render(
    f"Level: {level}", True,
    (255, 255, 255),
)
level_text_rect = level_text.get_rect()
level_text_rect.center = (100, 680)

# Create total cats collected text
total_text = font.render(
    f"Kettir rescured in total: {number}", True,
    (255, 255, 255),
)
total_text_rect = total_text.get_rect()
total_text_rect.center = (640, 500)

# Create win text
win_text = font1.render("Yuo Win!", True, (255, 255, 255))
win_text_rect = text.get_rect()
win_text_rect.center = (615, 320)

# Create button constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT = "Restart"

# Create button rect and text objects
button_rect = pygame.Rect(
    (win.get_width() - BUTTON_WIDTH) // 2,
    (win.get_height() - BUTTON_HEIGHT) // 2 + 70,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
button_text = font.render(BUTTON_TEXT, True, (255, 255, 255))
button_text_rect = button_text.get_rect(center=button_rect.center)


# Skins

# Diamondsonmydick
PLAYER_SKIN0 = pygame.image.load("images/player.jpg")

# Hello Kitty
PLAYER_SKIN1 = pygame.image.load("images/skin0.png")
PLAYER_SKIN1 = pygame.transform.smoothscale(PLAYER_SKIN1, (100, 100))

# Player
player_image = PLAYER_SKIN0
player_width = 100
player_height = 100
player_x = win.get_width() // 2 - player_width // 2
player_y = win.get_height() // 2 - player_height // 2

# Load the three images and generate their random positions
generate_cats()
collected = []

# Game Loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_score()
            running = False

    if image_rects:

        # Hreyfing
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 5
            if player_x < -player_width:
                player_x = win.get_width()
        elif keys[pygame.K_d]:
            player_x += 5
            if player_x > win.get_width():
                player_x = -player_width
        elif keys[pygame.K_w]:
            player_y -= 5
            if player_y < -player_height:
                player_y = win.get_height()
        elif keys[pygame.K_s]:
            player_y += 5
            if player_y > win.get_height():
                player_y = -player_height

        # Skin Selection temp.
        if keys[pygame.K_1]:
            player_image = PLAYER_SKIN0
        elif keys[pygame.K_2]:
            player_image = PLAYER_SKIN1

        # Tékka snertingu og hljóð
        for i, image_rect in enumerate(image_rects):
            image_center = (image_rect.x + 45, image_rect.y + 45)
            player_center = (
                player_x + player_width // 2,
                player_y + player_height // 2,
            )
            distance = math.hypot(
                image_center[0] - player_center[0],
                image_center[1] - player_center[1],
            )
            if (
                distance < 70
            ):  # 90 is half the sum of the width and height of the images
                score += 1
                text = font.render(
                    f"Kettir náðir: {score}", True,
                    (255, 255, 255),
                )
                win.blit(text, text_rect)
                print(f"cat {i+1} collected")
                collected.append(image_rect)
                acquire.play()
                win.blit(background, image_rect)  # redraw the background
                number += 1

        image_rects = [
            image_rect for image_rect in image_rects if image_rect not in collected
        ]

        # Teikna leikinn
        win.blit(background, (0, 0))  # level background
        win.blit(text, text_rect)
        win.blit(level_text, level_text_rect)

        # Define the player sprite position with a margin of 100x100
        player_rect = pygame.Rect(
            player_x + 50, player_y + 50,
            player_width - 100, player_height - 100,
        )

        for i, image_rect in enumerate(image_rects):
            # Define the image sprite position with a margin of 90x90
            image_rect_margin = pygame.Rect(
                image_rect.x + 45,
                image_rect.y + 45,
                image_rect.width - 90,
                image_rect.height - 90,
            )

            win.blit(images[i], image_rect)

        win.blit(player_image, (player_x, player_y))
        pygame.display.flip()  # update the display with the changes made

    else:
        ran_once = False
        if not ran_once:
            update_score()
        win_song.play(0)
        winbackground = pygame.image.load(image_path)
        win.blit(winbackground, (0, 0))

        win.blit(win_text, win_text_rect)
        pygame.draw.rect(win, BUTTON_COLOR, button_rect)
        win.blit(button_text, button_text_rect)
        total_text = font.render(
            f"Kettir rescured in total: {number}", True,
            (255, 255, 255),
        )
        win.blit(total_text, total_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse_pos):
            restart()

    pygame.display.update()

    clock.tick(FPS)  # Hraði

pygame.quit()
