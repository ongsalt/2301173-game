import pygame
from pygame.locals import *

class ColorChange(pygame.sprite.Sprite): 
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.image = pygame.Surface((30, 600))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def update(self):
        self.rect.x -= 10
    def is_collided(self, player_hitbox: pygame.Rect) -> bool:
        return self.rect.colliderect(player_hitbox)