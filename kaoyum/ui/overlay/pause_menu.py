from pygame import SRCALPHA, Rect
import pygame
from pygame.surface import Surface
from kaoyum.ui.animation import Spring
from ..widget import Widget, Text
from ..animation import SpringRect

class PauseMenu(Widget):
    def __init__(self, size: tuple[int, int]):
        self.surface = Surface(size, SRCALPHA, 32)
        self.hidden = True
        self.opacity = Spring(0, natural_freq=15)
        self.size = size
        self.scale = Spring(.85, natural_freq=15)
        self.text = Text("Pause Menu", "upheavtt.ttf", 36, (255, 255, 255))
        self.menu_texts = [
            Text("Resume", "upheavtt.ttf", 24, (255, 255, 255)),
            Text("Restart", "upheavtt.ttf", 24, (255, 255, 255)),
            Text("Quit", "upheavtt.ttf", 24, (255, 255, 255))
        ]
        self._selected = 0
        self._selected_indicator = SpringRect(0, 0, 0, 0, natural_freq=20)
        self.background = Surface(size, SRCALPHA, 32)
        self.background.fill((120, 120, 120, 150))

        self.select(0)
        self.hide()


    def update(self, dt: float = 1000 / 60):
        self.scale.update(dt)
        self.opacity.update(dt)
        self._selected_indicator.update(dt)

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        self.surface.fill((0, 0, 0, 0))
        self.surface.set_alpha(self.opacity.value)
        self.background.set_alpha(self.opacity.value)

        w, h = self.size
        x = w // 2 - self.text.size[0] // 2
        self.text.draw(self.surface, (x, 120))

        pygame.draw.rect(self.surface, (0, 0, 0, 80), self._selected_indicator.rect_value)

        for i, text in enumerate(self.menu_texts):
            x = w // 2 - text.size[0] // 2
            y = 240 + 60 * i
            text.draw(self.surface, (x, y))

        scaled = pygame.transform.scale(self.surface, (int(w * self.scale.value), int(h * self.scale.value)))
        x, y = offset
        x += (w - scaled.get_width()) // 2
        y += (h - scaled.get_height()) // 2
        display.blit(self.background, offset)
        display.blit(scaled, (x, y))

    def select(self, index: int):
        self._selected = index
        self._selected_indicator.animate_to(0, 225 + 60 * index, self.size[0], 40)

    def select_next(self):
        self.select((self._selected + 1) % 3)
    
    def select_previous(self):
        self.select((self._selected - 1) % 3)
    
    def activate_selected(self) -> str:
        if self._selected == 0:
            return "resume"
        elif self._selected == 1:
            return "restart"
        elif self._selected == 2:
            return "quit"
        
    def show(self):
        self.hidden = False
        self.scale.animate_to(1)
        self.opacity.animate_to(255)

    def hide(self):
        self.hidden = True
        self.scale.animate_to(1.1)
        self.opacity.animate_to(0)

