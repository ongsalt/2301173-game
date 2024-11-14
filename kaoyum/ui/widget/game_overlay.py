from pygame import SRCALPHA
from pygame.surface import Surface
from kaoyum.game import Game
from kaoyum.assets_manager import AssetsManager
from .widget import Widget
from kaoyum.ui.animation import Spring
from .text import Text

class GameOverlay(Widget):
    def __init__(self, game: Game, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32)
        self.size = size
        self._score = 0
        self.opacity = Spring(0, natural_freq=6)
        self.offset_x = Spring(40, natural_freq=6)
        self.score_text = Text("0", "upheavtt.ttf", 30, (255, 255, 255))

    def update(self, dt: float = 1000 / 60):
        self.opacity.update(dt)
        self.offset_x.update(dt)
        self.score_text.text = str(self.score)

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        self.surface.fill((0, 0, 0, 0))
        x = self.size[0] - self.score_text.size[0] - 24 
        self.score_text.draw(self.surface, (x, 24))
        self.surface.set_alpha(self.opacity.value)
        display.blit(self.surface, (offset[0] + self.offset_x.value, offset[1]))

    def show(self):
        self.opacity.animate_to(255)
        self.offset_x.animate_to(0)

    def hide(self):
        self.opacity.animate_to(0)
        self.offset_x.animate_to(40)

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, score: int):
        # if self._score != score:
            # self.notify("score", score)
        self._score = score
