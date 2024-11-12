from pygame import Surface

from kaoyum.assets_manager import AssetsManager
from random import randint
from .core import SizedNode

class StaticSurfaceNode(SizedNode):
    node_type: str = "StaticSurfaceNode"
    _invalidation_flags = 0

    def __init__(self, surface: Surface, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        super().__init__(children=[], width=width, height=height, fill_max_width=fill_max_width, fill_max_height=fill_max_height)
        self.surface = surface
        self._invalidation_flags = randint(0, 10000000)
        w, h = surface.get_size()
        self.width = w
        self.height = h

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

    # im too lazy to do the scaling so please just give the correct size image
    def __init__(self, image: str, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        super().__init__(
            surface=AssetsManager().get(image),
            width=width,
            height=height,
            fill_max_width=fill_max_width,
            fill_max_height=fill_max_height
        )
