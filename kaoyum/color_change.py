import pygame
from pygame.locals import *

class ColorChange(pygame.sprite.Sprite): 
    def __init__(self,x,y,color):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.rect = Rect(x, y, 50, 600)
        self.rect.y = y
        self.rect.x = x
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen,self.color,self.rect)
    def copy(self):
        return ColorChange(self.rect.x,self.rect.y,self.color)
    def update(self):
        self.rect.x -= 10
    def is_collided(self, player_hitbox: pygame.Rect) -> bool:
        return self.rect.colliderect(player_hitbox)

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ

        pygame.display.flip()