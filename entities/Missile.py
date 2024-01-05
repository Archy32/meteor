import pygame

from game_constants.AssetConstants import AssetsIMG


class Missile:
    def __init__(self, posx, posy):
        super().__init__()
        self.image = pygame.image.load(AssetsIMG.MISSILE_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.speed = 5
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.rect
