from .scene import Scene
from kaoyum.game import Game
from pygame.surface import Surface
from pygame.event import Event

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game(size)

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        self.game.run(display, dt)
    
    def copy(self):
        return GameplayScene(self.x, self.y) 
