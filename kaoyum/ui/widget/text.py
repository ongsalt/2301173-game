from pygame import SRCALPHA
from pygame.font import Font
from pygame.surface import Surface
from typing import Literal
from kaoyum.assets_manager import AssetsManager
from .widget import Widget
from ..animation import Spring

type Color = tuple[int, int, int] | tuple[int, int, int, int]
class Text(Widget):
    def __init__(self, text: str, font_name: str, font_size: int = 18, color: Color = (0, 0, 0)):
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.color = color
        self.dirty = True
        self.surface: Surface | None = None

    def render(self):
        if self.dirty:
            font = AssetsManager().get_font(self.font_name, self.font_size)
            w, h = font.get_rect(self.text).size
            if self.surface is None or self.size[0] < w or self.size[1] < h:
                self.surface = Surface((w, h), SRCALPHA, 32)
            self.surface.fill((0, 0, 0, 0))
            font.render_to(self.surface, (0, 0), self.text, self.color_without_alpha)
            self.surface.set_alpha(self.opacity)
            self.dirty = False

    def draw(self, surface: Surface, offset: tuple[int, int] = (0, 0)):
        self.render()
        surface.blit(self.surface, offset)

    def __setattr__(self, name, value):
        if name in ["text", "font_size", "font_name", "color"]:
            if hasattr(self, name) and getattr(self, name) != value:
                self.dirty = True
        return super().__setattr__(name, value)
    
    @property
    def size(self) -> tuple[int, int]:
        if self.surface is None:
            self.render()
        return self.surface.get_size()

    @property
    def color_without_alpha(self) -> Color:
        return self.color[:3]

    @color_without_alpha.setter
    def color_without_alpha(self, value: Color):
        self.color = (*value, self.opacity)

    @property
    def opacity(self) -> int:
        return self.color[3] if len(self.color) == 4 else 255
    
    @opacity.setter
    def opacity(self, value: int):
        if len(self.color) == 4:
            self.color = (*self.color_without_alpha, value)
        else:
            self.color = (*self.color, value)


class FlyoutText(Widget):
    def __init__(self, text: str, font_name: str, font_size: int = 18, color: Color = (0, 0, 0), duration: float = 3):
        self.y = Spring(-15)
        self.opacity = Spring(0)
        self.timer = duration
        self.text = Text(text, font_name, font_size, color)
        self.state: Literal["showing", "idle", "hiding"] = "showing"

    def update(self, dt: float = 1000 / 60):
        if self.state == "showing":
            self.y.animate_to(0)
            self.opacity.animate_to(255)
            if not self.y.is_animating and not self.opacity.is_animating:
                self.state = "idle"
        elif self.state == "idle":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "hiding"
        elif self.state == "hiding":
            self.y.animate_to(-15)
            self.opacity.animate_to(0)
            if not self.y.is_animating and not self.opacity.is_animating:
                self.notify("hide")
            
    def draw(self, surface: Surface, offset: tuple[int, int] = (0, 0)):
        self.text.opacity = self.opacity
        x, y = offset
        y += self.y.value
        self.text.draw(surface, (x, y))
