from pygame.surface import Surface

class Widget:
    def update(self, dt: float = 1000 / 60):
        pass

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        pass

