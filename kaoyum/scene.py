import pygame
import pygame.freetype
from pygame.locals import *
from kaoyum.game import Game 
from kaoyum.ui import UIRuntime, VStack, UIText, Spring, Padding, StatefulWidget, Stack, Image, Box, HStack

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

class HomeUI(StatefulWidget):
    def __init__(self):
        super().__init__()

    def build(self):
        return Stack(
            alignment="center",
            arrangement="center",
            children=[
                Image("bg.800x600.jpg"),
                Stack(
                    alignment="center",
                    arrangement="end",
                    fill_max_width=True,
                    fill_max_height=True,
                    gap=30,
                    padding=Padding(bottom=24),
                    children=[
                        UIText("Press space to begin", size=18),
                    ]
                ),
                VStack(
                    gap=10,
                    alignment="center",
                    children=[
                        UIText("Game Title", size=40),
                        Box(
                            height=1,
                            width=200,
                            background_color=(255, 255, 255, 100),
                        ),
                        UIText("Some random text", size=18)
                    ]
                ),
                VStack(
                    alignment="end",
                    arrangement="end",
                    fill_max_width=True,
                    fill_max_height=True,
                    gap=6,
                    padding=Padding(right=24, bottom=24),
                    children=[
                        UIText("Settings", size=18),
                        UIText("Exit", size=18)
                    ]
                )    
            ]
        )

class HomeScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.ui = HomeUI()
        self.ui_runtime = UIRuntime(
            size=size, 
            # draw_bound=True,
            root=self.ui
        )

    def run(self, display, dt: int):
        display.fill((0, 0, 0))
        self.ui_runtime.run(display, dt=dt)
    
    def handle_event(self, event) -> str | None:
        if event.type == KEYDOWN:
            key = event.dict["key"]
            if key == K_SPACE:
                return "to:game"
        #     if key == K_s or key == K_DOWN:
        #         self.ui.selected_index = (self.ui.selected_index + 1) % 3
        #     elif key == K_w or key == K_UP:
        #         self.ui.selected_index = (self.ui.selected_index - 1) % 3
        #     elif key == K_RETURN or key == K_SPACE:
        #         if self.ui.selected_index == 0:
        #             return "to:game"
        #         elif self.ui.selected_index == 1:
        #             return "to:settings"
        #         elif self.ui.selected_index == 2:
        #             return "exit"
