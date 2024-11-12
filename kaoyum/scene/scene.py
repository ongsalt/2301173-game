from pygame import Surface
from pygame.locals import *
from pygame.event import Event
from kaoyum.ui import UIRuntime, UINode

# TODO: cache rendered surface
class Scene:
    def __init__(self, size: tuple[int, int]):
        pass

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        return []

class UIScene(Scene):
    def __init__(self, size: tuple[int, int], ui: UINode, draw_bound: bool = False):
        super().__init__(size)
        self.ui = ui
        self.ui_runtime = UIRuntime(
            draw_bound=draw_bound,
            root=self.ui,
            size=size
        )

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        display.fill((0, 0, 0))
        self.ui_runtime.run(display, dt=dt)
        return []
    