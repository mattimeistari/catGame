# Import Libraries
import pygame
import random
from pygame import mixer
import time
import math
import pickle

# Start mixer
mixer.init()
mixer.music.load(f"sound/aquire.mp3")
mixer.music.load(f"sound/gem.mp3")

# Hard set values #
score = 0
level = 1
FPS = 60

# Functions


def play(soundfile):

    mixer.music.load(f"sound/{soundfile}")
    mixer.music.play()


def restart():

    return


# Setja upp playarea #
pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("FLOTTASTI LEIKUR IN THE WORLD")

# Backgrounds #
background = pygame.image.load("images/grass.jpg")
win.blit(background, (0, 0))

# Win background
random_number = random.randint(0, 4)
image_path = (f"images/cheer{random_number}.jpg")

# All text and buttons #

# Create fonts
font = pygame.font.SysFont("Arial", 32)
font1 = pygame.font.SysFont("Arial", 62)

# Retry button
retry_text = font1.render("Next Levle", True, (195, 153, 64))
retry_button_rect = pygame.Rect(300, 300, 205, 80)
retry_button_color = (50, 50, 50)

# Create cats collected constant text
text = font.render(f"Kettir náðir: {score}", True, (255, 255, 255))
text_rect = text.get_rect()
text_rect.center = (640, 600)
win.blit(text, text_rect)

# Create win text
win_text = font1.render("Yuo Win!", True, (255, 255, 255))
win_text_rect = text.get_rect()
win_text_rect.center = (640, 320)

# Leikmaður
player_image = pygame.image.load("images/player.jpg")
player_width = 100
player_height = 100
player_x = win.get_width() / 2 - player_width / 2
player_y = win.get_height() / 2 - player_height / 2

# Load the three images and generate their random positions
images = []
image_rects = []
# for i in range(1, 4+level)
if level > 4:
    level = 4

cats_total = (level + 3)
for i in range(1, cats_total):
    image = pygame.image.load(f"images/image{random.randint(1, 3)}.png")
    image_rect = image.get_rect()
    image_rect.x = random.randint(0, 1180)
    image_rect.y = random.randint(0, 620)
    images.append(image)
    image_rects.append(image_rect)


# Game Loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if score != (cats_total-1):
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

                # Tékka snertingu og hljóð
        for i, image_rect in enumerate(image_rects):
            image_center = (image_rect.x + 45, image_rect.y + 45)
            player_center = (player_x + player_width // 2, player_y + player_height // 2)
            distance = math.sqrt((image_center[0] - player_center[0])**2 + (image_center[1] - player_center[1])**2)
            if distance < 50:  # 90 is half the sum of the width and height of the images
                score += 1
                text = font.render(f"Kettir náðir: {score}", True, (255, 255, 255))
                win.blit(text, text_rect)
                print(f"cat {i+1} collected")
                play('aquire.mp3')
                win.blit(background, image_rect)  # redraw the background over the image
                image_rects.remove(image_rect)  # remove the image from the list

        player_x = int(player_x)
        player_y = int(player_y)

        # Teikna leikinn
        win.blit(background, (0, 0))  # grass

        win.blit(text, text_rect)

        # Define the player sprite position with a margin of 100x100
        player_rect = pygame.Rect(player_x + 50, player_y + 50, player_width - 100, player_height - 100)

        for i, image_rect in enumerate(image_rects):
            # Define the image sprite position with a margin of 90x90
            image_rect_margin = pygame.Rect(image_rect.x + 45, image_rect.y + 45, image_rect.width - 90, image_rect.height - 90)

            win.blit(images[i], image_rect)

        win.blit(player_image, (player_x, player_y))
        pygame.display.flip()  # update the display with the changes made

    else:
        winbackground = pygame.image.load(image_path)
        win.blit(winbackground, (0, 0))
        win.blit(win_text, win_text_rect)
        play("gem.mp3")

    pygame.display.update()

    clock.tick(FPS)  # Hraði

pygame.quit()