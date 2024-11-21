import pygame
from pygame.locals import *
from .assets_manager import AssetsManager

class ColorChanger(pygame.sprite.Sprite): 
    def __init__(self,x,color: str):
        super().__init__()
        self.color = color
        self.x = x
        self.y = 0
        self.rect = Rect(x, 0, 12, 600)
        self.rect.y = 0
        self.rect.x = x

        self.surfaces = [AssetsManager().get(f"ColorChanger/{color}-{i}.png") for i in range(1, 10)]

        self._frame_time_counter = 0
        self._animation_frame = 0


    def draw(self, screen: pygame.Surface):
        screen.blit(self.surfaces[self._animation_frame], (self.x, self.y))

    def copy(self):
        return ColorChanger(self.rect.x,self.color)
    def update(self):
        self.cycle_frame(1000//60)
        self.x -= 10
        self.rect.x -= 10
    def is_collided(self, player_hitbox: pygame.Rect) -> bool:
        return self.rect.colliderect(player_hitbox)
    
    def cycle_frame(self, dt: int):
        self._frame_time_counter += dt
        # print(self._frame_time_counter)
        if self._frame_time_counter > 120: # 250ms per frame
            self._frame_time_counter -= 120
            self._animation_frame += 1
            if self._animation_frame == len(self.surfaces):
                self._animation_frame = 0


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