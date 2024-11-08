import pygame

def tint_inp(surface: pygame.Surface, tint_color) -> pygame.Surface:
    """This WILL mutate the surface passed in.
    """
    surface.fill(tint_color[0:3] + (0,), None, pygame.BLEND_MULT)
    # surface.fill(tint_color[0:3] + (0,), None, pygame.BLEND_ADD)
    return surface

# This won't
def tint(surface: pygame.Surface, tint_color) -> pygame.Surface:
    """ adds tint_color onto surface.
    """
    surface = surface.copy()
    return tint_inp(surface, tint_color)

type Number = float | int

def coerce(value: Number, lower: Number, upper: Number) -> Number:
    return max(lower, min(value, upper))


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
