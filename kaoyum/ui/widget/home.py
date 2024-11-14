from pygame import Surface, SRCALPHA
from .widget import Widget
from kaoyum.assets_manager import AssetsManager

class HomeUI(Widget):
    def __init__(self, size):
        self.title_font = AssetsManager().get_font("upheavtt.ttf", 50)
        self.ui_font = AssetsManager().get_font("upheavtt.ttf", 30)
        self.size = size
        self.surface = Surface(size, SRCALPHA, 32)
        self.dirty = True
        self.offset_x = 0

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        w, h = self.size
        title_size = self.title_font.get_rect("Game Title").size
        description_size = self.ui_font.get_rect("Press Space to start").size
        self.title_font.render_to(self.surface, (w//2 - title_size[0]//2 + self.offset_x, 50), "Game Title", (255, 255, 255))
        self.ui_font.render_to(self.surface, (w//2 - description_size[0]//2 + self.offset_x, 120), "Press Space to start", (255, 255, 255))

    def draw(self, display):
        if self.dirty:
            self.render()
            self.dirty = False
        display.blit(self.surface, (0, 0))
    
    def select(self):
        pass

    def update(self, dt = 1000 / 60, is_game_started = False):
        if self.offset_x > -self.size[0] and is_game_started:
            self.offset_x -= 10
            self.dirty = True