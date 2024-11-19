from pygame import Surface
from pygame.transform import smoothscale, scale

# Just a repeated box blur
# This is very expensive operation so dont set the step too high
def blur(surface: Surface, radius: int, step: int = 2):
    if radius <= 1:
        return surface
    radius /= step
    cache_surface = surface.copy()
    w, h = cache_surface.get_size()
    size = (w // radius, h // radius)
    cache_surface2 = Surface(size)
    for i in range(step):
        smoothscale(cache_surface, size, cache_surface2)
        smoothscale(cache_surface2, (w, h), cache_surface)

    return cache_surface

def pixelate(surface: Surface, radius: int):
    if radius <= 1:
        return surface
    w, h = surface.get_size()
    surface = scale(surface, (w // radius, h // radius))
    surface = scale(surface, (w, h))
    return surface

def smooth_pixelate(surface: Surface, radius: int, target: Surface):
    if radius <= 1:
        return surface
    w, h = surface.get_size()
    surface = smoothscale(surface, (w // radius, h // radius))
    scale(surface, (w, h), target)
    return target

