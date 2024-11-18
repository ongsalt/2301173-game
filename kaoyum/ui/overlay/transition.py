from math import ceil
from ..animation import Spring
from ..widget import Widget
from pygame import Surface

# i want to do gakumas style transition animation

class Transition(Widget):
    def __init__(self, screen_size: tuple[int, int], square_size: int):
        self.screen_size = screen_size
        self.square_size = square_size
        self.start_progress = Spring(0, natural_freq=12) # First ripple
        self.end_progress = Spring(0, natural_freq=12) # Second ripple
        self.wait_timer = 0
        self.square_surface = Surface((square_size, square_size))
        self.square_surface.fill((0, 0, 0))

    def update(self, dt: int):
        self.start_progress.update(dt) 
        if self.wait_timer <= 0 and not self.start_progress.is_animating:
            self.is_fully_covered = False
            self.end_progress.update(dt)
        if not self.start_progress.is_animating: # I should really make a helper for this
            self.wait_timer -= dt
            self.is_fully_covered = True

    def draw(self, screen: Surface, offset: tuple[int, int]):
        # screen.get_size() must be equal to self.screen_size
        width, height = self.screen_size
        w = ceil(width / self.square_size)
        h = ceil(height / self.square_size)

        length = w + h + 1

        # This must be slow af
        for x in range(w):
            for y in range(h):
                # if self.start_progress.value * length > x + (h - y) and self.end_progress.value * length < x + (h - y):
                opacity1 = max(min(self.start_progress.value * length - (x + (h - y)), 2), 0)
                opacity2 = max(min(self.end_progress.value * length - (x + (h - y)), 2), 0)
                opacity = (opacity1 - opacity2) / 2
                # pygame.draw.rect(screen, (0, 0, 0, opacity * 255), (x * self.square_size, y * self.square_size, self.square_size, self.square_size))
                self.square_surface.set_alpha(opacity * 255)
                screen.blit(self.square_surface, (x * self.square_size, y * self.square_size))

    def start(self, time: int = 0):
        self.wait_timer = time
        self.start_progress.value = 0
        self.end_progress.value = 0
        self.start_progress.animate_to(1)
        self.end_progress.animate_to(1)
        self.is_fully_covered = False

    @property
    def is_finished(self):
        return self.start_progress.value == 1 and self.end_progress.value == 1
    
    @property
    def is_in_progress(self):
        return self.start_progress.value > 0 and self.end_progress.value != 1
    