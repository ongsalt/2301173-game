import pygame
import pygame.freetype
from pygame.locals import *
from kaoyum.game import Game 
from kaoyum.ui import UIRuntime, VStack, UIText, Spring, Padding, Widget

# Can i just make an interface for this?
class Scene:
    def __init__(self, size: tuple[int, int]):
        pass

    def run(self, display: pygame.Surface, dt: int):
        pass

    def handle_event(self, event: pygame.event.Event) -> None | str:
        pass

class GameScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game(size)

    def run(self, display, dt: int):
        self.game.run(display, dt)
    
    def handle_event(self, event):
        self.game.handle_event(event)

    def copy(self):
        return GameScene(self.x, self.y) 



class HomeUI(Widget):
    def __init__(self):
        self.selected_index = 0
        self.indicator_y = Spring(42)
        super().__init__()

    def build(self):
        return VStack(
            gap=10,
            padding=Padding(left=20),
            children=[
                UIText("Kaoyum", size=32),
                UIText("Play", size=24),
                UIText("Settings", size=24),
                UIText("Exit", size=24)
            ]
        )

class HomeScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.selected_index = 0
        self.indicator_y = Spring(42)
        self.ui = UIRuntime(
            size=size, 
            root=HomeUI()
        )

    def run(self, display, dt: int):
        display.fill((0, 0, 0))
        self.ui.run(display)
        self.indicator_y.update(dt)
        pygame.draw.rect(display, (255, 255, 255), (2, self.indicator_y.value, 3, 30))
    
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
            self.indicator_y.animate_to(42 + self.selected_index * 30)
