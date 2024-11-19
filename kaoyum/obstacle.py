import pygame
from pygame import *

class Obstacle:
    def __init__(self,x,y,damage: float,image: Surface, hitbox: Rect | None = None):
        self.x = x
        self.y = y
        self.damage = damage
        self.image = image
        # self.image = pygame.transform.scale(self.image,(self.width, self.height))
        self.relative_hitbox = hitbox or self.image.get_rect()
        self.hitbox = self.relative_hitbox.move(x,y)

    def is_collided(self, player_hitbox: pygame.Rect):
        return player_hitbox.colliderect(self.hitbox)

    def update(self):
        self.x -= 10
        self.hitbox.move_ip(-10,0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image,(self.x,self.y))
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
    
    def copy(self):
        return Obstacle(self.x,self.y,self.damage,self.image, self.relative_hitbox)