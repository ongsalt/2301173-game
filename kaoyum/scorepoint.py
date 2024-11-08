import pygame
from pygame import *

class Scorepoint:
    def __init__(self,x,y,width,height,score ,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = score
        self.image = image
        self.image = pygame.transform.scale(self.image,(self.width, self.height))
        self.hitbox = self.image.get_rect()
        self.hitbox.topleft = (self.x,self.y)

    def is_collided(self, player_hitbox: pygame.Rect):
        if player_hitbox.colliderect(self.hitbox):
            return self.score
        
    def update(self):
        self.hitbox.move_ip(-10,0)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image,self.hitbox)
    
    def copy(self):
        copy_image = self.image.copy() #ก็อบ Surface image
        return Scorepoint(self.x,self.y,self.width,self.height,self.score,copy_image)