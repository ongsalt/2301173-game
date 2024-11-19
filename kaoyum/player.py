import math
import pygame
from pygame.locals import * 
from pygame import Surface
from typing import Literal
from kaoyum.utils import coerce, tint, add
from kaoyum.assets_manager import AssetsManager
from kaoyum.ui.animation import Spring

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size: tuple[int, int], hp = 100, *groups):
        super().__init__(*groups)
        self.color: Literal["red", "green", "blue"] = "green"
        self.state: Literal["standard", "transitioning", "flying", "dying"] = "standard"
        self.hp = hp
        self.max_hp = 100
        self.y = (screen_size[1] - 100) / 2
        self.y_offset = Spring(self.y , natural_freq=10)
        self.x = Spring((screen_size[0] - 100) / 2, natural_freq=2)
        self.rect = pygame.Rect(self.x.value, self.y + self.y_offset.value, 100, 100)
        self.screen_size = screen_size
        self.rotation = Spring(0, natural_freq=12, damping_ratio=0.8)

        # For iframe
        self._iframe_cool_down = 0

        # For animation
        self._frame_time_counter = 0
        self._animation_frame = 0
        
        # This will be tinted programmatically
        self.textures = {
            # "placeholder": AssetsManager().get("tee.png"),
            "standard": self._load_frames("StandardPlayer/Main_Stand", frame_count=2),
            "flying":{
                "red": self._load_frames("RedPlayer/Red_Main_fly"),
                "green": self._load_frames("GreenPlayer/Green_Main_fly"),
                "blue": self._load_frames("BluePlayer/Blue_Main_fly"),
            },
        }

    def _load_frames(self, prefix, postfix = ".png", frame_count = 3) -> Surface:
        return [AssetsManager().get(f"{prefix}{i+1}{postfix}", (128, 128)) for i in range(frame_count)]

    def update(self, dt: int = 1000 // 60):
        self.rotate_frame(dt)
        self.rotation.update(dt)
        self.x.update(dt)
        self.y_offset.update(dt)
        self._iframe_cool_down = max(0, self._iframe_cool_down - dt)

        if self.state == "transitioning":
            self.rotation.animate_to(360)
            self.x.animate_to(25)
            self.y_offset.animate_to(0)
            if not self.rotation.is_animating:
                self.state = "flying"

        if self.state == "flying" or self.state == "transitioning":    
            self.process_key_pressed()
            self.hp -= dt * 0.005
            # self.y = self.y_offset.value
            # self.y = coerce(self.y, 0, self.screen_size[1] - self.rect.height)

        self.rect.y = self.y + self.y_offset.value
        self.rect.x = self.x.value

    def draw(self, surface: pygame.Surface):
        # I should precompute the tinted frames

        surface.blit(self.current_frame, add(self.rect.topleft, self.texture_offset))
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    def start_moving(self):
        self.state = "transitioning"

    def change_color(self, color: Literal["red", "green", "blue"]):
        self.color = color

    def take_damage(self, damage: int):
        if self._iframe_cool_down > 0:
            return
        self.hp -= damage
        self._iframe_cool_down = 300
        if self.hp <= 0:
            self.state = "dying"

    def shake(self, intensity: int):
        # self.x.damping_ratio = 0.5
        pass

    @property
    def texture_offset(self):
        texture = self.current_frame
        w, h = texture.get_size()
        return ((self.rect.width - w) // 2, (self.rect.height - h) // 2)
    
    @property
    def hitbox(self) -> pygame.Rect:
        return self.rect

    @property
    def current_frame(self):
        if self.state == "transitioning":
            if self.rotation.value < 180:
                frame = self.textures["standard"][self._animation_frame % 2]
            else:
                frame = self.textures["flying"]["green"][self._animation_frame]
            return pygame.transform.rotate(frame, self.rotation.value)

        if self._iframe_cool_down > 200:
            return tint(self.active_frames[self._animation_frame], (255, 200, 200))
        return self.active_frames[self._animation_frame]

    @property
    def active_frames(self):
        if self.state == "standard":
            return self.textures["standard"]
        else:
            return self.textures["flying"][self.color]
            
    def rotate_frame(self, dt: int):
        self._frame_time_counter += dt
        # print(self._frame_time_counter)
        if self._frame_time_counter > 250: # 250ms per frame
            self._frame_time_counter -= 250
            self._animation_frame += 1
            if self._animation_frame == len(self.active_frames):
                self._animation_frame = 0

    def process_key_pressed(self):
        keys_pressed = pygame.key.get_pressed()
        key_up = keys_pressed[K_w] or keys_pressed[K_UP]
        key_down = keys_pressed[K_s] or keys_pressed[K_DOWN]
        if key_up and not key_down:
            self.y -= 8
        elif key_down and not key_up:
            self.y += 8
        self.y = coerce(self.y, 0, self.screen_size[1] - self.rect.height)
