from pygame import SRCALPHA
from pygame.surface import Surface
from kaoyum.ui.animation import Spring
from ..widget import Widget

class GameOverUI(Widget):
    def __init__(self, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32)
        self.hidden = True
        self.scale = Spring(1, natural_freq=5)

    def update(self, dt: float = 1000 / 60):
        pass

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        pass

    def show(self):
        self.hidden = False
        self.scale.animate_to(1)

    def hide(self):
        self.hidden = True
        self.scale.animate_to(0)