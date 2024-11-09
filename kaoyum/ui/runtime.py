import pygame
from pygame import Rect
from .core import UINode, Constraints, Padding, Widget
from typing import Literal, Self
from kaoyum.utils import add

type Change = Literal["add", "remove", "update", "move"]
# If move, we don't need to mark the node as damaged
# Will skip the layout and draw phase

# We will compare 2 tree before measure phase

# Should be UINodeImmediateWhatever
class UINodeTexture:
    def __init__(self, size: tuple[int, int], node: UINode | None = None):
        self.size = size
        self.node = node
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.children: list[UINodeTexture] = []

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def add_child(self, texture: Self):
        self.children.append(texture)

    def __repr__(self):
        return f"Texture(size={self.size}, color={self.color})"

# Also act as a render texture manager
class Compositor:
    def __init__(self, size: tuple[int, int], root: UINode):
        self.size = size
        self.root = root
        self.screen = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.constraints = Constraints(0, 0, size[0], size[1])

        # Should remove the none variant
        self.root_texture: UINodeTexture | None = None

    # we can make this thing smarter by reusing the texture
    # but then we need information about which node to dispose 
    # def find_texture(self, path: str, size: tuple[int, int]) -> UINodeTexture:
    #     if (path not in self.textures) or (self.textures[path].size != size):
    #         self.textures[path] = UINodeTexture(size)
    #     return self.textures[path]

    # FUCK THIS: PREMATURE OPTIMIZATION IS THE ROOT OF ALL EVIL

    def draw_to(self, screen: pygame.Surface, position: tuple[int, int]):
        screen.blit(self.screen, position)

    # Should be call when something change
    def render(self) -> UINodeTexture:
        def traverse(node: UINode, path: str = "") -> UINodeTexture:
            # TODO: cache measure call
            size = node.measure(self.constraints)
            texture = UINodeTexture(size, node)
            texture.clear()
            node.draw(texture.surface)
            for i, child in enumerate(node.children):
                child_texture = traverse(child, f"{path}/{i}")
                texture.add_child(child_texture)
            return texture
        self.root_texture = traverse(self.root)
        return self.root_texture 

    # Only get called when the layout is change
    def composite(self):
        def traverse(texture: UINodeTexture, offset: tuple[int, int]):
            placeables = texture.node.layout()
            self.screen.blit(texture.surface, offset)
            for child, rect in zip(texture.children, placeables):
                traverse(child, add(offset, rect.topleft))

        self.screen.fill((0, 0, 0, 0))
        traverse(self.root_texture, (0, 0))

# TODO make this thing accept a normal node too
class UIRuntime:
    def __init__(self, root: Widget, size: tuple[int, int], draw_bound: bool = False):
        self.root = root.build()
        self.compositor = Compositor(size, self.root)
        self.draw_bound = draw_bound
        self.compositor.render()

    def update(self):
        self.compositor.render()
        self.compositor.composite()

    def draw(self, screen: pygame.Surface, position: tuple[int, int] = (0, 0)):
        # NOW DO THE DIFFING
        self.update()
        screen.blit(self.compositor.screen, position)

    # find which part of tree need to be replaced
    def diff(old: UINode, new: UINode):
        changes = []

        def compare_nodes(old_node, new_node, path=""):
            if old_node != new_node:
                changes.append((path, old_node, new_node))
            
            old_children = old_node.children if old_node else []
            new_children = new_node.children if new_node else []

            max_len = max(len(old_children), len(new_children))
            for i in range(max_len):
                # So we can't track reordering??
                old_child = old_children[i] if i < len(old_children) else None
                new_child = new_children[i] if i < len(new_children) else None
                compare_nodes(old_child, new_child, f"{path}/{i}")

        compare_nodes(old, new)
        return changes


if __name__ == "__main__":
    class ExampleWidget(Widget):
        def build(self):
            return VStack(
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

    from kaoyum.ui.text import UIText
    from kaoyum.ui.stack import VStack, HStack

    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    renderer = UIRuntime(
        size=(400, 300),
        draw_bound=True,
        root=ExampleWidget()
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
        