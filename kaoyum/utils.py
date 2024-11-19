import pygame
from typing import Literal

def tint_inp(surface: pygame.Surface, tint_color, mode: Literal["multiply", "add"] = "multiply") -> pygame.Surface:
    """This WILL mutate the surface passed in.
    """
    if mode == "multiply":
        surface.fill(tint_color[0:3] + (0,), None, pygame.BLEND_MULT)
    else:
        surface.fill(tint_color[0:3] + (0,), None, pygame.BLEND_ADD)
    return surface

# This won't
def tint(surface: pygame.Surface, tint_color, mode: Literal["multiply", "add"] = "multiply") -> pygame.Surface:
    """ adds tint_color onto surface.
    """
    surface = surface.copy()
    return tint_inp(surface, tint_color, mode)

type Number = float | int

def coerce(value: Number, lower: Number, upper: Number) -> Number:
    return max(lower, min(value, upper))

def add(a: tuple[Number, Number], b: tuple[Number, Number]) -> tuple[Number, Number]:
    return a[0] + b[0], a[1] + b[1]

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Timer:
    def __init__(self):
        self.start_time: dict[str, int] = {}
        self._stack: list[str] = []

    def start(self, name: str):
        self.start_time[name] = pygame.time.get_ticks()
        self._stack.append(name)
    
    def stop(self):
        name = self._stack.pop()
        print(f"{name}: {pygame.time.get_ticks() - self.start_time[name]}ms")
        del self.start_time[name]
