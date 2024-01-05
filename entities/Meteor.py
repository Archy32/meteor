import pygame
from game_constants.AssetConstants import AssetsIMG


class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load(AssetsIMG.METEOR_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed



