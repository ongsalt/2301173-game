import pygame
from typing import Literal

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.color: Literal["red", "green", "blue"] = "red"
        self.y = 0.0
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.frame_counter = 0
        self.animation_frame = 0
        # Or we can just tint this programmatically
        self.textures = {
            "running": {
                "red": self.load_frames("red_running", 1),
                "green": self.load_frames("green_running", 1),
                "blue": self.load_frames("blue_running", 1)
            },
            "flying": {
                "red": self.load_frames("red_flying", 1),
                "green": self.load_frames("green_flying", 1),
                "blue": self.load_frames("blue_flying", 1)
            },
            "dying": {
                "red": self.load_frames("red_dying", 1),
                "green": self.load_frames("green_dying", 1),
                "blue": self.load_frames("blue_dying", 1),
            }
        }

    def load_frames(self, prefix: str, frames: int) -> list[pygame.Surface]:
        # we don't have any assets for that yet
        # return [
        #     pygame.image.load(f"Assets/images/player/{prefix}_{frame}.png")
        #     for frame in range(1, frames)
        # ]
        return [
            pygame.image.load(f"Assets/images/tee.png")
        ]

    def update(self):
        frames = self.textures[self.get_state()][self.color]
        self.frame_counter += 1
        if self.frame_counter == 3:
            self.frame_counter = 0
            self.animation_frame += 1
            if self.animation_frame == len(frames):
                self.animation_frame = 0

    def draw(self, surface: pygame.Surface):
        frames = self.textures[self.state][self.color]
        surface.blit(frames[self.animation_frame], self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    @property
    def state(self) -> Literal["running", "flying", "dying"]:
        return "running"
    
    def move_y(self, dy: float):
        self.y += dy
        self.rect.y = int(self.y)

    @property
    def hitbox(self) -> pygame.Rect:
        return self.rect
