from pygame import SRCALPHA
from pygame.surface import Surface
from kaoyum.ui.animation import Spring, Loop
from kaoyum.assets_manager import AssetsManager
from ..widget import Widget, Text

class GameOverUI(Widget):
    def __init__(self, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32).convert_alpha()
        self.hidden = True
        self.opacity = Spring(0, natural_freq=2)
        self.y_offset = Spring(24, natural_freq=3)
        self.size = size
        self.score = 0
        self._score = Spring(0, natural_freq=4)
        self.timer = Spring(0, natural_freq=10)
        self.restart_text_opacity = Loop(160, 225, angular_frequency=.4)

        self.title = Text("Game Over", font_name="upheavtt.ttf", font_size=100, color=(255, 255, 255))
        self.score_text = Text("Your score: 0", font_name="upheavtt.ttf", font_size=42, color=(255, 255, 255))
        self.restart_text = Text("Press space to restart", font_name="upheavtt.ttf", font_size=24, color=(255, 255, 255))

    def update(self, dt: float = 1000 / 60):
        self.timer.update(dt)
        self.restart_text_opacity.update(dt)

        if not self.hidden and self.timer.value > 0.8: # I should make a step helper
            self.opacity.animate_to(255)
            self._score.animate_to(self.score)
            self.y_offset.animate_to(0)

        self.opacity.update(dt)
        self._score.update(dt)
        self.y_offset.update(dt)

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        if self.hidden and not self.opacity.is_animating:
            return
        self.surface.fill((120, 120, 120, 120))
        self.surface.set_alpha(self.opacity.value)

        self.score_text.text = f"Your score: {self._score.value:.0f}"
        self.restart_text.color = (255, 255, 255, self.restart_text_opacity.value)

        x = (self.size[0] - self.title.size[0]) // 2
        self.title.draw(self.surface, (x, 100 + self.y_offset.value))
        x = (self.size[0] - self.score_text.size[0]) // 2
        self.score_text.draw(self.surface, (x, 200 + self.y_offset.value))
        x = (self.size[0] - self.restart_text.size[0]) // 2
        self.restart_text.draw(self.surface, (x, 300 + self.y_offset.value))
        display.blit(self.surface, offset)

    def show(self):
        self.hidden = False
        self.timer.animate_to(1)

    def hide(self):
        self.hidden = True
        self.timer.animate_to(0)