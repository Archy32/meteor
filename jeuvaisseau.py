import random

import pygame


from entities.Meteor import Meteor
from entities.Missile import Missile
from game_constants.ScreenConstant import ScreenConstant
from game_constants.AssetConstants import AssetsIMG, AssetsMUSIC

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen = pygame.display.set_mode((ScreenConstant.SCREEN_WIDTH.__float__(), ScreenConstant.SCREEN_HEIGHT.__float__()))

# Initialisation de la clock
clock = pygame.time.Clock()

# Define the window icon
icon = pygame.image.load(AssetsIMG.METEOR_IMG)
pygame.display.set_icon(icon)
# Set the caption
pygame.display.set_caption("Météors")


def explode(meteor):
    # Afficher une explosion à l'emplacement du météore
    explosion_image = pygame.image.load(AssetsIMG.EXPLOSION_IMG).convert_alpha()
    screen.blit(explosion_image, meteor.rect)





# Load the images
ship_image = pygame.image.load(AssetsIMG.SHIP_IMG).convert_alpha()
missile_image = pygame.image.load(AssetsIMG.MISSILE_IMG).convert_alpha()

# Create the player sprite
player_sprite = pygame.sprite.Sprite()
player_sprite.image = ship_image
player_sprite.rect = player_sprite.image.get_rect()

# Set the player's starting position
player_sprite.rect.centerx = ScreenConstant.SCREEN_WIDTH / 2
player_sprite.rect.bottom = ScreenConstant.SCREEN_HEIGHT - 10

# Set the speeds
player_speed = 5
missile_speed = 5

# Create the missile sprite group
missile_group = pygame.sprite.Group()

# Initialize the clock
clock = pygame.time.Clock()

# Load the background images
background = pygame.image.load(AssetsIMG.BACKGROUND_IMG).convert()
background2 = pygame.image.load(AssetsIMG.BACKGROUND_IMG).convert()
background_y = 0
background2_y = -background.get_height()

# Load the music
pygame.mixer.music.load(AssetsMUSIC.MUSIC)

# Play the music
pygame.mixer.music.play(loops=-1)

# Initialize variables
move_left = False
move_right = False
move_timer = 0
move_delay = 5 # Delay in milliseconds between movements
num_meteor = 3


met_group = pygame.sprite.Group()
def create_meteors(count, width, height):
    for i in range(count):
        start_x = random.randrange(0,width - 50)
        start_y = random.randrange(0, height - 50)
        speed  = random.uniform(0.1, 0.5)
        met = Meteor(start_x,start_y, speed).sprite
        met_group.add(met)

create_meteors(num_meteor, ScreenConstant.SCREEN_WIDTH,ScreenConstant.SCREEN_HEIGHT)

# Game loop

running = True
while running:
    # Limitation de FPS
    clock.tick(ScreenConstant.FPS.__float__())

    if len(met_group) < num_meteor:
        create_meteors(num_meteor - len(met_group), ScreenConstant.SCREEN_WIDTH, ScreenConstant.SCREEN_HEIGHT)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Create a new missile
                missile = Missile(player_sprite.rect.centerx, player_sprite.rect.top)
                # Add the missile to the group
                missile_group.add(missile.sprite)
            if event.key == pygame.K_LEFT:
                move_left = True
                move_timer = pygame.time.get_ticks()
            elif event.key == pygame.K_RIGHT:
                move_right = True
                move_timer = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # Move the player
    now = pygame.time.get_ticks()
    if move_left and now - move_timer > move_delay:
        player_sprite.rect.x -= player_speed
        move_timer = now
    elif move_right and now - move_timer > move_delay:
        player_sprite.rect.x += player_speed
        move_timer = now

    # Keep the player on screen
    if player_sprite.rect.left < 0:
        player_sprite.rect.left = 0
    elif player_sprite.rect.right > ScreenConstant.SCREEN_WIDTH:
        player_sprite.rect.right = ScreenConstant.SCREEN_WIDTH

    # Move the missiles
    for missile_sprite in missile_group:
        missile_sprite.rect.y -= missile_speed
        if missile_sprite.rect.colliderect(pygame.Rect(0, 0, ScreenConstant.SCREEN_WIDTH.__float__(), 0)):
            # Le missile a touché le bord supérieur de l'écran
            # Remove the missile when it goes off screen
            missile_group.remove(missile_sprite)

    # Handle missile-meteor collision
    collisions = pygame.sprite.groupcollide(missile_group, met_group, True, True)
    for meto in collisions.values():
        for m in meto:
            explode(m)

    # Move the meteors
    for meteor in met_group:
         meteor.rect.y += meteor.speed

    # Draw the background
    screen.blit(background, (0, background_y))
    screen.blit(background2, (0, background2_y))
    if background_y >= background.get_height():
        background_y = -background.get_height()
    if background2_y >= background2.get_height():
        background2_y = -background2.get_height()
    background_y += 1
    background2_y += 1

    # Draw the meteors
    met_group.draw(screen)

    # Draw the missiles
    missile_group.draw(screen)

    # Draw the player
    screen.blit(player_sprite.image, player_sprite.rect)

    # Update the screen
    pygame.display.flip()

pygame.quit()
