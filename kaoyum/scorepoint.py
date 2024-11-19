import pygame
from pygame import *

class Scorepoint:
    def __init__(self,x,y,width,height,score ,image, color: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = score
        self.image = image
        self.color = color
        # self.image = pygame.transform.scale(self.image,(self.width, self.height))
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (self.x,self.y)

    def is_collided(self, player_hitbox: pygame.Rect):
        return player_hitbox.colliderect(self.hitbox)
        
    def update(self):
        self.hitbox.move_ip(-10,0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image,self.hitbox)
    
    def copy(self):
        return Scorepoint(self.x,self.y,self.width,self.height,self.score,self.image, self.color)