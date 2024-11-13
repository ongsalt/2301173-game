import pygame
from pygame import Surface
from pygame import Rect
from kaoyum.assets_manager import AssetsManager
from ..core import UINode, Constraints, Size

class UIText(UINode):
    node_type: str = "UIText"

    def __init__(self, text: str, font_name: str = "Rowdies-Light.ttf", size: int = 18, color: tuple = (255, 255, 255)):
        super().__init__()
        self.texture: pygame.Surface | None = None
        self.text = text
        self.font_name = font_name
        self.font_size = size
        self.color = color

    def draw(self, target: Surface, size: Size):
        font = AssetsManager().get_font(self.font_name, self.font_size)
        font.render_to(target, (0, 0), self.text, self.color)

    # TODO: handle baseline becuase currently it's look like shit
    def measure(self) -> Constraints:
        font = AssetsManager().get_font(self.font_name, self.font_size)
        w, h = font.get_rect(self.text).size
        return Constraints(w, h, w, h)

    def __hash__(self):
        return hash((self.node_type, self.text, self.font_name, self.font_size, self.color))

    def __repr__(self):
        return f"{self.node_type}(text={self.text}, font_name={self.font_name}, size={self.font_size}, color={self.color})"

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    text = UIText("Hello World")
    constraints = text.measure()
    size = (constraints.max_width, constraints.max_height)
    children_bound = text.layout(size)
    print(f"{size=} {children_bound=}")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        screen.fill((0, 0, 0))
        text.draw(screen, size)

        pygame.display.flip()