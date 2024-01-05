import pygame
from game_constants.AssetConstants import AssetsIMG


class Meteor:
    def __init__(self, posx, posy, speed):
        super().__init__()
        self.image = pygame.image.load(AssetsIMG.METEOR_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.speed = 1
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.rect
        self.sprite.speed = self.speed



