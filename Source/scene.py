import pygame
import pygame.freetype
from pygame.locals import *
from game import Game 
from dataclasses import dataclass

# Can i just make an interface for this?
class Scene:
    def __init__(self, size: tuple[int, int]):
        pass

    def run(self, display: pygame.Surface):
        pass

    def handle_event(self, event: pygame.event.Event) -> None | str:
        pass


class GameScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game()

    def run(self, display):
        self.game.run(display)
    
    def handle_event(self, event):
        self.game.handle_event(event)

    def copy(self):
        return GameScene(self.x, self.y) 


class HomeScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.selected_index = 0
        self.font = pygame.freetype.Font("Assets/fonts/Inter-Regular.ttf", 18)

    def run(self, display):
        display.fill((0, 0, 0))
        self.font.render_to(display, (10, 10), "Game title", (255, 255, 255))
        self.font.render_to(display, (10, 60),"Start", (255, 255, 255))
        self.font.render_to(display, (10, 90),"Settings (not implemented yet)", (255, 255, 255))
        self.font.render_to(display, (10, 120),"Exit", (255, 255, 255))
        pygame.draw.rect(display, (255, 255, 255), (2, 52 + self.selected_index * 30, 3, 30))
    
    def handle_event(self, event) -> str | None:
        if event.type == KEYDOWN:
            key = event.dict["key"]
            if key == K_s or key == K_DOWN:
                self.selected_index = (self.selected_index + 1) % 3
            elif key == K_w or key == K_UP:
                self.selected_index = (self.selected_index - 1) % 3
            elif key == K_RETURN or key == K_SPACE:
                if self.selected_index == 0:
                    return "to:game"
                elif self.selected_index == 1:
                    return "to:settings"
                elif self.selected_index == 2:
                    return "exit"
