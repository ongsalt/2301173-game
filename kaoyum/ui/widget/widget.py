from pygame.surface import Surface

# I should make a different class for overlays but they still behave like widgets anyway
class Widget:
    def update(self, dt: float = 1000 / 60):
        pass

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        pass
