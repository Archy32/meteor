import random
import sys

import pygame

# Initialize pygame
pygame.init()

# Initialize the window and give it a name
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Meteors")

# Define the window icon
icon = pygame.image.load("assets/sprites/meteor.png")
pygame.display.set_icon(icon)

# Load the music
pygame.mixer.music.load("assets/musics/stranger-things-124008.mp3")

# Load the background images
background = pygame.image.load("assets/sprites/fond.png").convert()
background2 = pygame.image.load("assets/sprites/fond.png").convert()
background_y = 0
background2_y = -background.get_height()

# Load the ship image
ship_sprite = pygame.sprite.Sprite()
ship_sprite.image = pygame.image.load("assets/sprites/vaisseau.png").convert_alpha()
ship_sprite.rect = ship_sprite.image.get_rect()
ship = ship_sprite.rect
ship_protected = pygame.image.load("assets/sprites/vaisseauhit.png").convert_alpha()

# Load the meteor image
meteor_image = pygame.image.load("assets/sprites/meteor.png")
meteor_detruit = pygame.image.load("assets/sprites/meteor_explode.png")

# Initialize the position of the ship

ship_x = (width - ship.get_width()) / 2
ship_y = height - ship.get_height() - 10

# Initialize the speed of the ship
ship_speed = 0.2

# Load the missile image
missile = pygame.image.load("assets/sprites/missile.png").convert_alpha()

# Initialize the position and speed of the missile
missile_x = 0
missile_y = height - ship.get_height() - missile.get_height() - 10
missile_speed = 0.5
missile_launched = False

# Initialize the speed of the meteors
meteor_speed = 1

# Initialize the number of meteors
num_meteors = 10

# Initialize the meteor list
meteor_list = pygame.sprite.Group()
for i in range(num_meteors):
    meteor = pygame.sprite.Sprite()
    meteor.image = meteor_image
    meteor.rect = meteor.image.get_rect()
    meteor.rect.x = random.randint(0, width - meteor_image.get_width())
    meteor.rect.y = -meteor_image.get_height()
    meteor.speed_x = random.uniform(-meteor_speed, meteor_speed)
    meteor.speed_y = random.uniform(meteor_speed, 0.2)
    meteor_list.add(meteor)

# Initialize the variables for when a meteor is hit
meteor_hit = False
meteor_hit_timer = 0

# Initialize the direction of the ship
ship_direction = 0

# Play the music
pygame.mixer.music.play(loops=-1)

# Initialize the variable for when the ship is hit
ship_hit = False
ship_hit_timer = 0

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship_direction = -1
            elif event.key == pygame.K_RIGHT:
                ship_direction = 1
            elif event.key == pygame.K_SPACE:
                if not missile_launched:
                    missile_launched = True
                    missile_x = ship_x + (ship.get_width() - missile.get_width()) / 2
                    missile_y = ship_y - missile.get_height()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and ship_direction == -1:
                ship_direction = 0
            elif event.key == pygame.K_RIGHT and ship_direction == 1:
                ship_direction = 0

    # Draw all
    # Draw the background
    screen.blit(background, (0, background_y))
    screen.blit(background2, (0, background2_y))
    if background_y >= background.get_height():
        background_y = -background.get_height()
    if background2_y >= background2.get_height():
        background2_y = -background2.get_height()
    background_y += 0.1
    background2_y += 0.1

    # Draw the meteors
    for meteor in meteor_list:
        meteor.rect.x += meteor.speed_x
        meteor.rect.y += meteor.speed_y
        if meteor.rect.y > height:
            meteor.rect.x = random.randint(0, width - meteor_image.get_width())
            meteor.rect.y = -meteor_image.get_height()
            meteor.speed_x = random.uniform(-meteor_speed, meteor_speed)
            meteor.speed_y = random.uniform(meteor_speed, 0.2)
        if meteor.rect.colliderect(ship.rect):
            # Game over if a meteor collides with the spaceship
            game_over = True
        screen.blit(meteor.image, meteor.rect)

    # Draw the missile if it has been launched
    if missile_launched:
        missile_y -= missile_speed
        if missile_y < -missile.get_height():
            missile_launched = False
        else:
            screen.blit(missile, (missile_x, missile_y))

    # Draw the ship
    if not ship_hit:
        ship_x += ship_direction * ship_speed
        if ship_x < 0:
            ship_x = 0
        elif ship_x > width - ship.get_width():
            ship_x = width - ship.get_width()
        screen.blit(ship, (ship_x, ship_y))
    else:
        if ship_hit_timer == 0:
            ship_hit_timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - ship_hit_timer > 3000:
            ship_hit = False
            ship_hit_timer = 0
        else:
            if pygame.time.get_ticks() % 200 < 100:
                screen.blit(ship_protected, (ship_x, ship_y))

    # Check for collisions between the ship and the meteors
    for meteor in meteor_list:
        if not ship_hit and meteor.rect.colliderect(pygame.Rect(ship_x, ship_y, ship.get_width(), ship.get_height())):
            ship_hit = True
            meteor_hit = True
            meteor_list.remove(meteor)
            break

    # Check for collisions between the missile and the meteors
    for meteor in meteor_list:
        if missile_launched and meteor.rect.colliderect(
                pygame.Rect(missile_x, missile_y, missile.get_width(), missile.get_height())):
            missile_launched = False
            meteor_hit = True
            meteor_list.remove(meteor)
            break

    # Draw the explosion if a meteor has been hit
    if meteor_hit:
        if meteor_hit_timer == 0:
            meteor_hit_timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - meteor_hit_timer > 500:
            meteor_hit = False
            meteor_hit_timer = 0
        else:
            screen.blit(meteor_detruit, (meteor.rect.x, meteor.rect.y))

    # Update the display
    pygame.display.flip()