import pygame
import pygame.freetype
from kaoyum.utils import Singleton

class AssetsManager(metaclass=Singleton):
    def __init__(self):
        self.surfaces: dict[str, pygame.Surface] = {}

        # key is a tuple of font path and font size
        self.fonts: dict[tuple[str, int], pygame.Surface] = {}

    # DON'T EVER MUTATE THE SURFACE RETURNED BY THIS FUNCTION
    # If you need to mutate it, copy it first
    # If not please use this method
    def get(self, path: str) -> pygame.Surface:
        path = f"Assets/images/{path}"
        if path not in self.surfaces:
            self.surfaces[path] = pygame.image.load(path)
        return self.surfaces[path]
    
    def set(self, path: str, surface: pygame.Surface) -> None:
        self.surfaces[path] = surface
        
    def get_font(self, path: str = "Inter-Regular.ttf", size: int = 18) -> pygame.freetype.Font:
        path = f"Assets/fonts/{path}"
        key = (path, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.freetype.Font(path, size)
        return self.fonts[key]
