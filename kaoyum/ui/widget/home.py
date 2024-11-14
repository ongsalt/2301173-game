from pygame import Surface, SRCALPHA
from .widget import Widget
from .text import Text
from kaoyum.assets_manager import AssetsManager
from ..animation import Loop

class HomeUI(Widget):
    def __init__(self, size):
        self.size = size
        self.surface = Surface(size, SRCALPHA, 32)
        self.dirty = True
        self.offset_x = 0
        self.title_text = Text("Game Title", "upheavtt.ttf", 50, (255, 255, 255))
        self.description_text = Text("Press Space to start", "upheavtt.ttf", 20, (255, 255, 255))
        self.description_text_opacity = Loop(160, 235, angular_frequency=.5)


    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        self.description_text.color = (255, 255, 255, self.description_text_opacity.value)
        self.surface.fill((0, 0, 0, 0))
        w, h = self.size
        x1 = self.offset_x + (w // 2 - self.title_text.size[0] // 2)
        x2 = self.offset_x + (w // 2 - self.description_text.size[0] // 2)
        self.title_text.draw(self.surface, (x1, 120))
        self.description_text.draw(self.surface, (x2, 180))
        self.dirty = False
        display.blit(self.surface, offset)
    
    def select(self):
        pass

    def update(self, dt = 1000 / 60, is_game_started = False):
        self.description_text_opacity.update(dt)
        if self.offset_x > -self.size[0] and is_game_started:
            self.offset_x -= 10
            self.dirty = True