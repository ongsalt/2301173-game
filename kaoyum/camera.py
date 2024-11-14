from dataclasses import dataclass
from pygame import Rect

@dataclass
class Camera:
    x: float = 0
    y: float = 0
    size: tuple[int, int] = (800, 600) # screen size

    def move(self, dx: float = 0, dy: float = 0):
        # Top left of the camera
        self.x += dx
        self.y += dy

    def is_visible(self, x: float, y: float, w: float, h: float) -> bool:
        return Rect(self.x, self.y, self.size[0], self.size[1]).colliderect(Rect(x, y, w, h))

    def translate(self, x: float, y: float) -> tuple[float, float]:
        return x - self.x, y - self.y
