from pygame import SRCALPHA
import pygame
from pygame.surface import Surface
from kaoyum.ui.animation import Spring
from ..widget import Widget, Text

class PauseMenu(Widget):
    def __init__(self, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32)
        self.hidden = True
        self.opacity = Spring(0)
        self.size = size
        self.scale = Spring(.85)
        self.text = Text("Mai Tam Tee", "upheavtt.ttf", 60, (255, 255, 255))

    def update(self, dt: float = 1000 / 60):
        self.scale.update(dt)
        self.opacity.update(dt)

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        # if self.hidden:
        #     return

        w, h = self.size
        self.surface.fill((0, 0, 0, 0))
        x = w // 2 - self.text.size[0] // 2
        self.text.draw(self.surface, (x, h // 2 - self.text.size[1] // 2))
        self.surface.set_alpha(self.opacity.value)

        scaled = pygame.transform.scale(self.surface, (int(w * self.scale.value), int(h * self.scale.value)))
        x, y = offset
        x += (w - scaled.get_width()) // 2
        y += (h - scaled.get_height()) // 2
        display.blit(scaled, (x, y))

    def show(self):
        self.hidden = False
        self.scale.animate_to(1)
        self.opacity.animate_to(255)

    def hide(self):
        self.hidden = True
        self.scale.animate_to(.85)
        self.opacity.animate_to(0)
