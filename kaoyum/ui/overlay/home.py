from pygame import Surface, SRCALPHA
from ..widget.widget import Widget
from ..widget.text import Text
from kaoyum.assets_manager import AssetsManager
from ..animation import Loop, Spring, Acceleration

class HomeUI(Widget):
    def __init__(self, size):
        self.size = size
        self.static_surface = Surface(size, SRCALPHA, 32)
        self.surface = Surface(size, SRCALPHA, 32)
        self.offset_x = Acceleration(0, acceleration=0, max_speed=750)
        self.title_text = Text("Game Title", "upheavtt.ttf", 50, (255, 255, 255))
        self.description_text = Text("Press Space to start", "upheavtt.ttf", 20, (255, 255, 255))
        self.description_text_opacity = Loop(160, 235, angular_frequency=.5)
        self.static_part_opacity = Spring(255, natural_freq=10)
        self.prerender()

    def prerender(self):
        # draw key binding at the bottom
        y = self.size[1] - 16 - 24
        x = 12

        w_key = AssetsManager().get("keys/w.png", (32, 32))
        self.static_surface.blit(w_key, (x, y))
        up_key = AssetsManager().get("keys/up.png", (32, 32))
        self.static_surface.blit(up_key, (x + 32, y))
        text = Text("Move Up", "upheavtt.ttf", 20, (255, 255, 255))
        text.draw(self.static_surface, (x + 68, y + 10))

        x = text.size[0] + 92 + 24

        s_key = AssetsManager().get("keys/s.png", (32, 32))
        self.static_surface.blit(s_key, (x, y))
        down_key = AssetsManager().get("keys/down.png", (32, 32))
        self.static_surface.blit(down_key, (x + 32, y))
        text = Text("Move Down", "upheavtt.ttf", 20, (255, 255, 255))
        text.draw(self.static_surface, (x + 68, y + 10))

        x = self.size[0] - 12
        text = Text("Start / Restart", "upheavtt.ttf", 20, (255, 255, 255))
        x -= text.size[0]
        text.draw(self.static_surface, (x, y + 10))
        x -= 72
        space_key = AssetsManager().get("keys/space.png", (64, 32))
        self.static_surface.blit(space_key, (x, y))

        text = Text("Pause", "upheavtt.ttf", 20, (255, 255, 255))
        x -= text.size[0] + 24
        text.draw(self.static_surface, (x, y + 10))
        x -= 60
        esc_key = AssetsManager().get("keys/esc.png", (64, 32))
        self.static_surface.blit(esc_key, (x, y))
        

    def draw(self, display: Surface, offset: tuple[int, int] = (0, 0)):
        w, h = self.size
        self.surface.fill((0, 0, 0, 0), (0, 0, w, 400))
        x1 =(w // 2 - self.title_text.size[0] // 2)
        self.title_text.draw(self.surface, (x1, 120))

        w, h = self.size
        self.description_text.color = (255, 255, 255, self.description_text_opacity.value)
        x2 =(w // 2 - self.description_text.size[0] // 2)
        self.description_text.draw(self.surface, (x2, 180))
        x, y = offset
        x += self.offset_x.value

        self.static_surface.set_alpha(self.static_part_opacity.value)
        display.blit(self.static_surface, offset)
        display.blit(self.surface, (x, y))

    def update(self, dt = 1000 / 60, is_game_started = False):
        self.description_text_opacity.update(dt)
        self.static_part_opacity.update(dt)
        self.offset_x.update(dt)

        if is_game_started:
            if not self.offset_x.is_animating:
                self.offset_x.animate_to(-1000, initial_velocity=400)
                self.static_part_opacity.animate_to(0)