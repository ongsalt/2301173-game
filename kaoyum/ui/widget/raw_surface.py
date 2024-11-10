from pygame import Surface
from ..core import UINode, Constraints, Size
from random import randint

class StaticSurfaceNode(UINode):
    node_type: str = "StaticSurfaceNode"
    _invalidation_flags = 0

    def __init__(self, surface: Surface):
        self.surface = surface
        self._invalidation_flags = randint(0, 10000000)
        super().__init__()

    def measure(self, constraints: Constraints) -> Size:
        w, h = self.surface.get_size()
        return constraints.coerce_and_round(w, h)

    def draw(self, target: Surface):
        target.blit(self.surface, (0, 0))

    def invalidate(self):
        pass

    def __hash__(self):
        return hash((self.surface.get_size(), self._invalidation_flags, self.node_type))

    def __repr__(self):
        return f"{self.node_type}(surface={self.surface})"
    

class Image(StaticSurfaceNode):
    node_type: str = "Image"

    def __init__(self, surface: Surface):
        super().__init__(surface)
