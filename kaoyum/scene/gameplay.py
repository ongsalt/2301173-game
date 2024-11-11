from .scene import Scene
from kaoyum.game import Game

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game(size)

    def run(self, display, dt: int):
        self.game.run(display, dt)
    
    def handle_event(self, event):
        self.game.handle_event(event)

    def copy(self):
        return GameplayScene(self.x, self.y) 
