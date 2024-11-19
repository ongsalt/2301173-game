import pygame
from pygame.locals import *

class ColorChange(pygame.sprite.Sprite): 
    def __init__(self,x,color: str):
        super().__init__()
        self.color = color
        self.x = x
        self.y = 0
        self.rect = Rect(x, 0, 50, 600)
        self.rect.y = 0
        self.rect.x = x
    def draw(self, screen: pygame.Surface):
        if self.color == "red":
            draw_color = (255,0,0)
        elif self.color == "green":
            draw_color = (0,255,0)
        elif self.color == "blue":
            draw_color = (0,0,255)
        pygame.draw.rect(screen,draw_color,self.rect)
    def copy(self):
        return ColorChange(self.rect.x,self.color)
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