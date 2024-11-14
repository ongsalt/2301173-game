import pygame
from assets_manager import AssetsManager
from ui.node import UINode
from utils import add

class UIText(UINode):
    def __init__(self, text: str, font_name: str = "Inter-Regular.ttf", size: int = 18, color: tuple = (255, 255, 255), position: tuple[int, int] = (0, 0)):
        super().__init__()
        self.texture: pygame.Surface | None = None
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.damage = True

    def render(self):
        font = AssetsManager().get_font(self.font_name, self.size)
        self.texture = font.render(self.text, self.color)

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> bool:
        if self.damage:
            self.render()
        screen.blit(self.texture, add(self.position, offset))

    def __setattr__(self, name, value):
        # Well you should not update the surface directly anyway
        if name != "damage":
            self.damage = True
        return super().__setattr__(name, value)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode((800, 600))
    text = UIText("Hello World", position=(100, 100))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        text.draw(screen)

        pygame.display.flip()