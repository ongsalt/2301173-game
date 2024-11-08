import pygame
from pygame import Rect
from kaoyum.assets_manager import AssetsManager
from kaoyum.ui.core import UINode, Constraints, Padding

class UIText(UINode):
    def __init__(self, text: str, font_name: str = "Inter-Regular.ttf", size: int = 18, color: tuple = (255, 255, 255), padding: Padding | None = None):
        super().__init__()
        self.texture: pygame.Surface | None = None
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.damaged = True # Default
        self.padding = padding or Padding.zero()

    def render(self):
        font = AssetsManager().get_font(self.font_name, self.size)
        font.render_to(self.texture, self.padding.topleft, self.text, self.color)
        self.damaged = False

    def draw(self, screen: pygame.Surface) -> bool:
        if self.damaged:
            self.render()
        size = Rect((0, 0), self.rect.size)
        screen.blit(self.texture, self.rect, size)

    def layout(self, area):
        if self.texture is None or self.texture.get_size() != area.size:
            self.texture = pygame.Surface(area.size, pygame.SRCALPHA, 32)
        return super().layout(area)

    def measure(self, constraints: Constraints) -> tuple[int, int]:
        font = AssetsManager().get_font(self.font_name, self.size)
        w, h = font.get_rect(self.text).size
        w += abs(self.padding.width)
        h += abs(self.padding.height)
        return constraints.coerce(w, h)

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    text = UIText("Hello World", position=(100, 100))
    size = text.measure()
    print(size)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        screen.fill((0, 0, 0))
        text.draw(screen, Rect(0, 0, 0, 0))

        pygame.display.flip()