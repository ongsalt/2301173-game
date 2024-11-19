from pygame import Surface, SRCALPHA
from ..widget.widget import Widget
from ..widget.text import Text
from kaoyum.assets_manager import AssetsManager
from ..animation import Loop, Spring, Acceleration

class SettingsUI(Widget):
    def __init__(self, size):
        self.size = size
        self.surface = Surface(size, SRCALPHA, 32).convert_alpha()
        self.title_text = Text("Settings", "upheavtt.ttf", 50, (255, 255, 255))

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        self.description_text.color = (255, 255, 255, self.description_text_opacity.value)
        self.surface.fill((0, 0, 0, 0))
        w, h = self.size
        x1 = self.offset_x.value + (w // 2 - self.title_text.size[0] // 2)
        x2 = self.offset_x.value + (w // 2 - self.description_text.size[0] // 2)
        self.title_text.draw(self.surface, (x1, 120))
        self.description_text.draw(self.surface, (x2, 180))
        self.dirty = False
        display.blit(self.surface, offset)
    
    def select(self):
        pass

    def update(self, dt = 1000 / 60, is_game_started = False):
        pass
