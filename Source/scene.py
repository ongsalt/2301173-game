import pygame

class Scene:
    def __init__(self):
        self.surface = pygame.Surface()

    def draw(self, display: pygame.Surface):
        display.blit(self.surface)

    def update(self, dt: float):
        pass