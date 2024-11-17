from pygame import Surface
from .widget import Widget
from kaoyum.assets_manager import AssetsManager

class Image(Widget):
    def __init__(self, image: str, size: tuple[int, int] | None = None):
        super().__init__()
        if size is not None:
            self.size = size
            self.image = AssetsManager().get(image, size)
        else:
            self.image = AssetsManager().get(image)
            self.size = self.image.get_size()

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        display.blit(self.image, offset)
