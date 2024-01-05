import random

import pygame

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialisation de la clock
clock = pygame.time.Clock()

# Define the window icon
icon = pygame.image.load("assets/sprites/meteor.png")
pygame.display.set_icon(icon)

# Set the caption
pygame.display.set_caption("Météors")


# objet meteors
class Meteor(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def explode(self):
        # Afficher une explosion à l'emplacement du météore
        explosion_image = pygame.image.load("assets/sprites/Explosion.png").convert_alpha()
        screen.blit(explosion_image, self.rect.center)


def create_meteors(num_meteor, meteor_image, width, height):
    meteors = pygame.sprite.Group()
    for i in range(num_meteor):
        x = random.randrange(width)
        y = random.randrange(-height, -100)
        speed = random.uniform(0.1, 0.5)
        meteor = Meteor(meteor_image, x, y, speed)
        meteors.add(meteor)
    return meteors


# Load the images
ship_image = pygame.image.load("assets/sprites/vaisseau.png").convert_alpha()
missile_image = pygame.image.load("assets/sprites/missile.png").convert_alpha()
meteor_image = pygame.image.load("assets/sprites/meteor.png").convert_alpha()

# Create the player sprite
player_sprite = pygame.sprite.Sprite()
player_sprite.image = ship_image
player_sprite.rect = player_sprite.image.get_rect()

# Set the player's starting position
player_sprite.rect.centerx = WIDTH / 2
player_sprite.rect.bottom = HEIGHT - 10

# Set the speeds
player_speed = 5
missile_speed = 5

# Create the missile sprite group
missile_group = pygame.sprite.Group()

# Initialize the clock
clock = pygame.time.Clock()

# Load the background images
background = pygame.image.load("assets/sprites/fond.png").convert()
background2 = pygame.image.load("assets/sprites/fond.png").convert()
background_y = 0
background2_y = -background.get_height()

# Load the music
pygame.mixer.music.load("assets/musics/stranger-things-124008.mp3")

# Play the music
pygame.mixer.music.play(loops=-1)

# Initialize variables
move_left = False
move_right = False
move_timer = 0
move_delay = 5  # Delay in milliseconds between movements

num_meteor = 3
meteor_group = create_meteors(num_meteor, meteor_image, WIDTH, HEIGHT)

# Game loop

running = True
while running:
    # Limitation de FPS
    clock.tick(FPS)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Create a new missile sprite
                missile_sprite = pygame.sprite.Sprite()
                missile_sprite.image = missile_image
                missile_sprite.rect = missile_sprite.image.get_rect()

                # Set the missile's starting position
                missile_sprite.rect.centerx = player_sprite.rect.centerx
                missile_sprite.rect.bottom = player_sprite.rect.top
                # Add the missile to the group
                missile_group.add(missile_sprite)
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
    elif player_sprite.rect.right > WIDTH:
        player_sprite.rect.right = WIDTH

    # Move the missiles
    for missile_sprite in missile_group:
        missile_sprite.rect.y -= missile_speed
        if missile_sprite.rect.colliderect(pygame.Rect(0, 0, WIDTH, 0)):
            # Le missile a touché le bord supérieur de l'écran
            # Remove the missile when it goes off screen
            missile_group.remove(missile_sprite)

    # Handle missile-meteor collision
    collisions = pygame.sprite.groupcollide(missile_group, meteor_group, True, True)
    for meteor in collisions.values():
        for m in meteor:
            m.explode()

    # Move the meteors
    for meteor in meteor_group:
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
    meteor_group.draw(screen)

    # Draw the missiles
    missile_group.draw(screen)

    # Draw the player
    screen.blit(player_sprite.image, player_sprite.rect)

    # Update the screen
    pygame.display.flip()

pygame.quit()
