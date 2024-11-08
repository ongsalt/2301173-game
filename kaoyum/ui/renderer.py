import pygame
from kaoyum.ui.core import UINode, Constraints, Padding

class UIRenderer:
    def __init__(self, root: UINode, size: tuple[int, int], draw_bound: bool = False):
        self.screen = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.rect = self.screen.get_rect()
        self.constraints = Constraints(0, 0, size[0], size[1])
        self.root = root
        self.draw_bound = draw_bound

    def render(self):
        self.screen.fill((0, 0, 0, 0))
        self.root.measure(self.constraints)
        self.root.layout(self.rect)
        self.root.draw(self.screen)
        if self.draw_bound:
            self.root.draw_bound(self.screen)
        self.traverse(self.root)

    def traverse(self, node: UINode):
        for child in node.children:
            child.draw(self.screen)
            if self.draw_bound:
                child.draw_bound(self.screen)
            self.traverse(child)

    def draw(self, screen: pygame.Surface, position: tuple[int, int] = (0, 0)):
        if self.root.damaged:
            self.render()
        screen.blit(self.screen, position)

if __name__ == "__main__":
    from kaoyum.ui.text import UIText
    from kaoyum.ui.stack import VStack, HStack

    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    renderer = UIRenderer(
        size=(400, 300),
        draw_bound=True,
        root=VStack(
            gap=10,
            padding=Padding(0, 0, 0, 24),
            children=[
                UIText("Title", size=24),
                UIText("Text 2"),
                HStack(
                    gap=25,
                    children=[
                        UIText("1"),
                        UIText("Hello World"),
                        VStack(
                            children=[
                                UIText("Nested 1"),
                                UIText("Nested 2"),
                            ]
                        ),
                    ]
                ),
                UIText("With padding", padding=Padding.all(20)),
            ]
        )
    )

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        screen.fill((16, 163, 240))
        renderer.draw(screen, (200, 150))

        pygame.display.flip()