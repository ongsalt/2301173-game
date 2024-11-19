import pygame
from pygame import *

class Obstacle:
    def __init__(self,x,y,width,height,damage: float,image: Surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = damage
        self.image = image
        # self.image = pygame.transform.scale(self.image,(self.width, self.height))
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (self.x,self.y)

    def is_collided(self, player_hitbox: pygame.Rect):
        return player_hitbox.colliderect(self.hitbox)

    def update(self):
        self.hitbox.move_ip(-10,0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image,self.hitbox)
        # pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
    
    def copy(self):
        return Obstacle(self.x,self.y,self.width,self.height,self.damage,self.image)