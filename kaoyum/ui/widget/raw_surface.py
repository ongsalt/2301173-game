from pygame import Surface
from .core import Constraints
from kaoyum.assets_manager import AssetsManager
from random import randint
from .layout import SizedNode

class StaticSurfaceNode(SizedNode):
    node_type: str = "StaticSurfaceNode"
    _invalidation_flags = 0

    def __init__(self, surface: Surface, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        width = width or surface.get_width()
        height = height or surface.get_height()
        super().__init__(children=[], width=width, height=height, fill_max_width=fill_max_width, fill_max_height=fill_max_height)
        self.surface = surface
        self._invalidation_flags = randint(0, 10000000)

    def draw(self, target: Surface, size: tuple[int, int]):
        # print(f"Drawing {self.node_type} with size {size}")
        target.blit(self.surface, (0, 0))

    def invalidate(self):
        self._invalidation_flags = randint(0, 10000000)

    def __hash__(self):
        return hash((self.surface.get_size(), self._invalidation_flags, self.node_type))

    def __repr__(self):
        return f"{self.node_type}(surface={self.surface})"

class Image(StaticSurfaceNode):
    node_type: str = "Image"

    # im too lazy to do the scaling so please just give the correct size image
    def __init__(self, image: str, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        self.image_name = image
        super().__init__(
            surface=AssetsManager().get(image),
            width=width,
            height=height,
            fill_max_width=fill_max_width,
            fill_max_height=fill_max_height
        )

    def __hash__(self):
        return hash((self.surface.get_size(), self.image_name, self.node_type))
