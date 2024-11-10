import pygame
from pygame import Rect
from ...assets_manager import AssetsManager
from ..core import UINode, Constraints, Padding

class UIText(UINode):
    node_type: str = "UIText"

    def __init__(self, text: str, font_name: str = "Inter-Regular.ttf", size: int = 18, color: tuple = (255, 255, 255), padding: Padding | None = None):
        super().__init__()
        self.texture: pygame.Surface | None = None
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.padding = padding or Padding.zero()

    def draw(self, target: pygame.Surface) -> bool:
        font = AssetsManager().get_font(self.font_name, self.size)
        font.render_to(target, self.padding.topleft, self.text, self.color)

    def measure(self, constraints: Constraints) -> tuple[int, int]:
        font = AssetsManager().get_font(self.font_name, self.size)
        w, h = font.get_rect(self.text).size
        w += abs(self.padding.width)
        h += abs(self.padding.height)
        return constraints.coerce(w, h)

    def __hash__(self):
        return hash((self.node_type, self.text, self.font_name, self.size, self.color, self.padding))

    def __repr__(self):
        return f"{self.node_type}(text={self.text}, font_name={self.font_name}, size={self.size}, color={self.color}, padding={self.padding})"

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    text = UIText("Hello World", padding=Padding(left=50, top=50))
    size = text.measure(Constraints(0, 0, 800, 600))
    text.layout(Rect((0, 0), size))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        screen.fill((0, 0, 0))
        text.draw(screen)

        pygame.display.flip()