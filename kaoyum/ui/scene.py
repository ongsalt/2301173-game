from typing import Literal
from pygame import Surface
from pygame.locals import *
from pygame.event import Event

from kaoyum.game import Game
from .effect import blur, pixelate, smooth_pixelate
from .overlay.game_over import GameOverUI
from .overlay.pause_menu import PauseMenu
from .overlay.home import HomeUI
from .overlay.game_overlay import GameOverlay
from .animation import Spring

class Scene:
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        pass
        # for event in reversed(events or []):
        #     if self.handle_event(event):
        #         events.remove(event)

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        self.game = Game(size)
        self.home_ui = HomeUI(size)
        self.game_overlay = GameOverlay(self.game, size)
        self.pause_menu = PauseMenu(size)
        self.game_over_ui = GameOverUI(size)
        self.lower_layer = Surface(size)
        self.pixelate_radius = Spring(0, natural_freq=12)
        
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):      
        for event in reversed(events or []):
            if self.handle_event(event):
                events.remove(event)

        self.update(dt)
        self.draw(display)

    def update(self, dt: int):
        self.update_animation(dt)

        if self.game.state == "waiting":
            self.game_overlay.hide()
            self.pixelate_radius.animate_to(0)

        elif self.game.state == "running":
            self.game_overlay.show()
            self.pause_menu.hide()
            self.pixelate_radius.animate_to(0)
        
        elif self.game.state == "paused":
            self.game_overlay.show()
            self.pause_menu.show()
            self.pixelate_radius.animate_to(24)

        elif self.game.state == "finished":
            self.game_overlay.hide()
            self.game_over_ui.show()
            self.pixelate_radius.animate_to(24)


        self.game.run(self.lower_layer, dt)
        self.game_overlay.score = self.game.score
        self.game_overlay.hp = self.game.player.hp

        if self.game.state != "paused":
            self.home_ui.update(dt=dt, is_game_started=self.game.is_started)
        self.game_overlay.update(dt)
        self.pause_menu.update(dt)
        self.game_over_ui.update(dt)

    def update_animation(self, dt: int):
        self.pixelate_radius.update(dt)
    
    def draw(self, display: Surface):
        self.home_ui.draw(self.lower_layer)
        self.game_overlay.draw(self.lower_layer)
        # blurred_lower_layer = blur(self.lower_layer, 2 * self.pixelate_radius.value, step=4)
        # blurred_lower_layer = pixelate(self.lower_layer, self.pixelate_radius.value)
        blurred_lower_layer = smooth_pixelate(self.lower_layer, self.pixelate_radius.value)
        # blurred_lower_layer = smooth_pixelate(self.lower_layer, 4)
        display.blit(blurred_lower_layer, (0, 0))
        self.game_over_ui.draw(display)
        self.pause_menu.draw(display)


    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            # print(event)
            if event.key == 32:
                self.game.start()
                self.game_overlay.show()
                return True
            
            if event.key == 27:
                if self.game.state == "running":
                    self.game.pause()
                elif self.game.state == "paused":
                    self.game.resume()
                return True
            
        return False
