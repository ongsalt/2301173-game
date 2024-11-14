from dataclasses import dataclass
from .core import WrapperNode
from ..core import Constraints

class Transformation(WrapperNode):
    def __init__(self, child = None, scale = 1.0, scale_x: float | None = None, scale_y: float | None = None, opacity = 1.0, blur_radius = 0.0):
        super().__init__(child)
        scale_x = scale_x or scale
        scale_y = scale_y or scale
        self.effect = TransformationEffect(scale_x, scale_y, opacity, blur_radius)

    def measure(self):
        constraints = super().measure()
        min_width = constraints.min_width * self.effect.scale_x
        min_height = constraints.min_height * self.effect.scale_y
        max_width = constraints.max_width * self.effect.scale_x
        max_height = constraints.max_height * self.effect.scale_y
        return Constraints(min_width, min_height, max_width, max_height)
    
    def layout(self, size):
        rects = super().layout(size)
        rect = rects[0]
        rect.width *= self.effect.scale_x
        rect.height *= self.effect.scale_y
        rect.top *= self.effect.scale_y
        rect.left *= self.effect.scale_x
        return [rect]

    def __hash__(self):
        return hash((self.effect, *self.children))

@dataclass(frozen=True)
class TransformationEffect:
    scale_x: float = 1.0
    scale_y: float = 1.0
    opacity: float = 1.0
    blur_radius: float = 0.0

