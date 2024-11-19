import sys
from typing import Literal
from pygame import Surface
import pygame
from pygame.locals import *
from pygame.event import Event

from kaoyum.game import Game
from kaoyum.utils import Timer
from .effect import blur, pixelate, smooth_pixelate
from .overlay.game_over import GameOverUI
from .overlay.pause_menu import PauseMenu
from .overlay.home import HomeUI
from .overlay.game_overlay import GameOverlay
from .overlay.transition import Transition
from .animation import Spring

timer = Timer()

class Scene:
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        pass
        # for event in reversed(events or []):
        #     if self.handle_event(event):
        #         events.remove(event)

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.game = Game(size)
        self.home_ui = HomeUI(size)
        self.game_overlay = GameOverlay(size)
        self.pause_menu = PauseMenu(size)
        self.game_over_ui = GameOverUI(size)
        self.lower_layer = Surface(size)
        self.pixelate_radius = Spring(0, natural_freq=12)
        self.pixelated_lower_layer = Surface(size)
        self.transition = Transition(size, 32)

        self._will_reset = False
        
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):      
        for event in reversed(events or []):
            if self.handle_event(event):
                events.remove(event)
        
        if self._will_reset and self.transition.is_fully_covered:
            self._reset()
            self._will_reset = False

        # timer.start("update")
        self.update(dt)
        # timer.stop()
        # timer.start("draw")
        self.draw(display)
        # timer.stop()

    def update(self, dt: int):
        self.update_animation(dt)

        if self.state == "waiting":
            self.game_overlay.hide()
            self.pixelate_radius.animate_to(0)

        elif self.state == "running":
            self.game_overlay.show()
            self.pause_menu.hide()
            self.pixelate_radius.animate_to(0)
        
        elif self.state == "paused":
            self.game_overlay.show()
            self.pause_menu.show()
            self.pixelate_radius.animate_to(24)

        elif self.state == "finished":
            # self.game_overlay.hide()
            self.game_over_ui.show()
            self.pause_menu.hide()
            self.pixelate_radius.animate_to(24)

        self.game.run(self.lower_layer, dt)
        self.game_overlay.score = self.game.score
        self.game_overlay.hp = self.game.player.hp
        self.game_over_ui.score = self.game.score

        if self.state != "paused":
            self.home_ui.update(dt=dt, is_game_started=self.game.is_started)
        self.game_overlay.update(dt)
        self.pause_menu.update(dt)
        self.game_over_ui.update(dt)
        self.transition.update(dt)

    def update_animation(self, dt: int):
        self.pixelate_radius.update(dt)
    
    def draw(self, display: Surface):
        self.home_ui.draw(self.lower_layer)
        self.game_overlay.draw(self.lower_layer)
        # blurred_lower_layer = blur(self.lower_layer, 2 * self.pixelate_radius.value, step=4)
        # blurred_lower_layer = pixelate(self.lower_layer, self.pixelate_radius.value)
        blurred_lower_layer = smooth_pixelate(self.lower_layer, self.pixelate_radius.value, self.pixelated_lower_layer)
        display.blit(blurred_lower_layer, (0, 0))
        self.game_over_ui.draw(display)
        self.pause_menu.draw(display)

        self.transition.draw(display, (0, 0))

    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            if self.state == "waiting":
                if event.key == 32:
                    self.game.start()
                if event.key == 27:
                    pygame.quit()
                    sys.exit()
                return True
            
            if self.state == "running":
                if event.key == 27:
                    self.game.pause()
                return True
            
            if self.state == "paused":
                if event.key == 27:
                    self.game.resume()
                if event.key == 119 or event.key == K_UP:
                    self.pause_menu.select_previous()
                if event.key == 115 or event.key == K_DOWN:
                    self.pause_menu.select_next()
                if event.key == 32 or event.key == 13:
                    message = self.pause_menu.activate_selected()
                    if message == "resume":
                        self.game.resume()
                    elif message == "restart":
                        self.reset()
                    elif message == "quit":
                        pygame.quit()
                        sys.exit()
                return True
            
            if self.state == "finished":
                if (event.key == 27 or event.key == 32) and not self.transition.is_in_progress:
                    self.reset()
                return True
            
        return False

    def reset(self):
        # This is the fun part: WE DONT HAVE A RESET FUNCTION
        self.transition.start()
        self._will_reset = True

    def _reset(self):
        self.game = Game(self.size)
        self.home_ui = HomeUI(self.size)
        self.game_overlay = GameOverlay(self.size)
        self.pause_menu = PauseMenu(self.size)
        self.game_over_ui = GameOverUI(self.size)
        self.lower_layer = Surface(self.size)
        self.pixelate_radius.value = 0

    @property
    def state(self):
        return self.game.state
