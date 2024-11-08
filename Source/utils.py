import pygame

def tint(surf, tint_color):
    """ adds tint_color onto surf.
    """
    surf = surf.copy()
    surf.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # surf.fill(tint_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return surf

type Number = float | int

def coerce(value: Number, lower: Number, upper: Number) -> Number:
    return max(lower, min(value, upper))
