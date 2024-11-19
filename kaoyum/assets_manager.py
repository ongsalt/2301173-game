import pygame
import pygame.freetype
from kaoyum.utils import Singleton

class AssetsManager(metaclass=Singleton):
    def __init__(self):
        # key is (path, size)
        self.surfaces: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}

        # key is a tuple of font path and font size
        self.fonts: dict[tuple[str, int], pygame.Surface] = {}

    # DON'T EVER MUTATE THE SURFACE RETURNED BY THIS FUNCTION
    # If you need to mutate it, copy it first
    # If not please use this method
    def get(self, path: str, size: tuple[int, int] | None = None) -> pygame.Surface:
        path = f"Assets/images/{path}"
        sized_key = (path, size)
        defualt_key = (path, None)
        if defualt_key not in self.surfaces:
            self.surfaces[defualt_key] = pygame.image.load(path).convert_alpha()
        
        if sized_key not in self.surfaces:
            if size == self.surfaces[defualt_key].get_size():
                self.surfaces[sized_key] = self.surfaces[defualt_key]
            else:
                self.surfaces[sized_key] = pygame.transform.scale(self.surfaces[defualt_key], size)

        return self.surfaces[sized_key]
    
    def set(self, path: str, surface: pygame.Surface) -> None:
        path = f"Assets/images/{path}"
        key = (path, None)
        self.surfaces[key] = surface
        
    def get_font(self, path: str = "Inter-Regular.ttf", size: int = 18) -> pygame.freetype.Font:
        path = f"Assets/fonts/{path}"
        key = (path, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.freetype.Font(path, size)
        return self.fonts[key]
