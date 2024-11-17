from pygame import SRCALPHA
import pygame
from pygame.surface import Surface
from kaoyum.game import Game
from kaoyum.assets_manager import AssetsManager
from ..widget.widget import Widget
from kaoyum.ui.animation import Spring
from ..widget.text import Text

class GameOverlay(Widget):
    def __init__(self, game: Game, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32)
        self.size = size
        self._score = 0
        self.hp = 100
        self.max_hp = 100
        self.opacity = Spring(0, natural_freq=6)
        self.offset_x = Spring(40, natural_freq=6)
        self.score_text = Text("0", "upheavtt.ttf", 30, (255, 255, 255))

    def update(self, dt: float = 1000 / 60):
        self.opacity.update(dt)
        self.offset_x.update(dt)
        self.score_text.text = str(self.score)

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        self.surface.fill((0, 0, 0, 0))
        self.surface.set_alpha(self.opacity.value)
        x = self.size[0] - self.score_text.size[0] - 24 
        self.score_text.draw(self.surface, (x, 24))

        # Hp bar
        hp_bar_width = 400
        hp_bar_height = 4
        pygame.draw.rect(self.surface, (80, 80, 80, 80), (24, 24, hp_bar_width, hp_bar_height))
        pygame.draw.rect(self.surface, (255, 255, 255), (24, 24, self.hp / self.max_hp * hp_bar_width, hp_bar_height))

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
