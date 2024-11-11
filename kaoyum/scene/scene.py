import pygame
import pygame.freetype
from pygame.locals import *

# Can i just make an interface for this?
class Scene:
    def __init__(self, size: tuple[int, int]):
        pass

    def run(self, display: pygame.Surface, dt: int):
        pass

    def handle_event(self, event: pygame.event.Event) -> None | str:
        pass
