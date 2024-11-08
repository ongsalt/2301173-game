import pygame
from pygame.locals import * 
from typing import Literal
from utils import coerce

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size: tuple[int, int], *groups):
        super().__init__(*groups)
        self.color: Literal["red", "green", "blue"] = "red"
        self.y = 0.0
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.screen_size = screen_size

        # For animation
        self.frame_counter = 0
        self.animation_frame = 0
        
        # This will be tinted programmatically
        self.textures = {
            "placeholder": pygame.image.load("Assets/images/tee.png"),
        }

    def update(self):
        self.process_key_pressed()
        self.rotate_frame()

    def draw(self, surface: pygame.Surface):
        # frames = self.textures[self.state][self.color]
        surface.blit(self.textures["placeholder"], self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    @property
    def state(self) -> Literal["running", "flying", "dying"]:
        return "running"
    
    @property
    def hitbox(self) -> pygame.Rect:
        return self.rect
    
    def rotate_frame(self):
        self.frame_counter += 1
        if self.frame_counter == 3:
            self.frame_counter = 0
            self.animation_frame += 1
            # if self.animation_frame == len(frames):
            #     self.animation_frame = 0

    def process_key_pressed(self):
        keys_pressed = pygame.key.get_pressed()
        key_up = keys_pressed[K_w] or keys_pressed[K_UP]
        key_down = keys_pressed[K_s] or keys_pressed[K_DOWN]
        if key_up and not key_down:
            self.y -= 10
        elif key_down and not key_up:
            self.y += 10
        self.y = coerce(self.y, 0, self.screen_size[1] - self.rect.height)
        self.rect.y = self.y
