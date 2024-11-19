import random
import pygame
from .obstacle import Obstacle
from .scorepoint import Scorepoint
from .color_change import ColorChange
from .assets_manager import AssetsManager

class Block:
    def __init__(self, obstacles: list[Obstacle], score_points: list[Scorepoint], color_changers: list[ColorChange], offset):
        self.obstacles = obstacles
        self.score_points = score_points
        self.color_changers = color_changers
        self.offset = offset
    
    def copy(self):
        copied_obs = []
        copied_scs = []
        copied_ccs = []
        for obstacle in self.obstacles:
            copied_op = obstacle.copy()
            copied_op.x += self.offset
            copied_op.hitbox.x += self.offset
            copied_obs.append(copied_op)
        for score_point in self.score_points:
            copied_sc = score_point.copy()
            copied_sc.x += self.offset
            copied_sc.hitbox.x += self.offset
            copied_scs.append(copied_sc)
        for color_changer in self.color_changers:
            copied_cc = color_changer.copy()
            copied_cc.x += self.offset
            copied_cc.rect.x += self.offset
            copied_ccs.append(copied_cc)
        return Block(copied_obs,copied_scs,copied_ccs, self.offset)

def initialize_block():
    image1 = AssetsManager().get("slime_2.gif")
    image2 = AssetsManager().get("ThaiRice.jpg")

    block1 = Block(
        obstacles = [
            Obstacle(100, 550, 50, 50, 0, image1),
            Obstacle(170, 350, 50, 50, 0, image1),
            Obstacle(200, 170, 50, 50, 0, image1),
            Obstacle(350, 50, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(50, 150, 30, 30, 10, image2),
            Scorepoint(150, 150, 30, 30, 10, image2),
            Scorepoint(200, 250, 30, 30, 10, image2),
            Scorepoint(250, 350, 30, 30, 10, image2),
            Scorepoint(300, 450, 30, 30, 10, image2),
            Scorepoint(350, 550, 30, 30, 10, image2),
            Scorepoint(400, 150, 30, 30, 10, image2),
            Scorepoint(450, 250, 30, 30, 10, image2),
            Scorepoint(500, 350, 30, 30, 10, image2),
            Scorepoint(550, 450, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(100,200,pygame.Color(255,0,0)),
            ColorChange(500,400,pygame.Color(0,255,0))],
        offset = 800
    )

    block2 = Block(
        obstacles = [
            Obstacle(120, 580, 50, 50, 0, image1),
            Obstacle(190, 400, 50, 50, 0, image1),
            Obstacle(220, 230, 50, 50, 0, image1),
            Obstacle(370, 100, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(60, 170, 30, 30, 10, image2),
            Scorepoint(160, 170, 30, 30, 10, image2),
            Scorepoint(210, 270, 30, 30, 10, image2),
            Scorepoint(260, 370, 30, 30, 10, image2),
            Scorepoint(310, 470, 30, 30, 10, image2),
            Scorepoint(360, 570, 30, 30, 10, image2),
            Scorepoint(410, 170, 30, 30, 10, image2),
            Scorepoint(460, 270, 30, 30, 10, image2),
            Scorepoint(510, 370, 30, 30, 10, image2),
            Scorepoint(560, 470, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(300,400,pygame.Color(0,0,255)),
            ColorChange(50,250,pygame.Color(0,255,0))
        ],
        offset = 800
    )

    block3 = Block(
        obstacles = [
            Obstacle(140, 600, 50, 50, 0, image1),
            Obstacle(210, 450, 50, 50, 0, image1),
            Obstacle(240, 280, 50, 50, 0, image1),
            Obstacle(390, 150, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(70, 190, 30, 30, 10, image2),
            Scorepoint(170, 190, 30, 30, 10, image2),
            Scorepoint(220, 290, 30, 30, 10, image2),
            Scorepoint(270, 390, 30, 30, 10, image2),
            Scorepoint(320, 490, 30, 30, 10, image2),
            Scorepoint(370, 590, 30, 30, 10, image2),
            Scorepoint(420, 190, 30, 30, 10, image2),
            Scorepoint(470, 290, 30, 30, 10, image2),
            Scorepoint(520, 390, 30, 30, 10, image2),
            Scorepoint(570, 490, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(700,200,pygame.Color(255,0,0)),
            ColorChange(400,380,pygame.Color(0,0,255))
        ],
        offset = 800
    )

    block4 = Block(
        obstacles = [
            Obstacle(150, 620, 50, 50, 0, image1),
            Obstacle(220, 470, 50, 50, 0, image1),
            Obstacle(250, 300, 50, 50, 0, image1),
            Obstacle(400, 170, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(80, 200, 30, 30, 10, image2),
            Scorepoint(180, 200, 30, 30, 10, image2),
            Scorepoint(230, 300, 30, 30, 10, image2),
            Scorepoint(280, 400, 30, 30, 10, image2),
            Scorepoint(330, 500, 30, 30, 10, image2),
            Scorepoint(380, 600, 30, 30, 10, image2),
            Scorepoint(430, 200, 30, 30, 10, image2),
            Scorepoint(480, 300, 30, 30, 10, image2),
            Scorepoint(530, 400, 30, 30, 10, image2),
            Scorepoint(580, 500, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(600,220,pygame.Color(255,0,0)),
            ColorChange(200,350,pygame.Color(0,255,0))
        ],
        offset = 800
    )

    block5 = Block(
        obstacles = [
            Obstacle(160, 640, 50, 50, 0, image1),
            Obstacle(230, 490, 50, 50, 0, image1),
            Obstacle(260, 320, 50, 50, 0, image1),
            Obstacle(410, 190, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(90, 210, 30, 30, 10, image2),
            Scorepoint(190, 210, 30, 30, 10, image2),
            Scorepoint(240, 310, 30, 30, 10, image2),
            Scorepoint(290, 410, 30, 30, 10, image2),
            Scorepoint(340, 510, 30, 30, 10, image2),
            Scorepoint(390, 610, 30, 30, 10, image2),
            Scorepoint(440, 210, 30, 30, 10, image2),
            Scorepoint(490, 310, 30, 30, 10, image2),
            Scorepoint(540, 410, 30, 30, 10, image2),
            Scorepoint(590, 510, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(50,600,pygame.Color(0,255,0)),
            ColorChange(300,500,pygame.Color(0,0,255))
        ],
        offset = 800
    )

    # เพิ่ม block6 ถึง block10
    block6 = Block(
        obstacles = [
            Obstacle(180, 660, 50, 50, 0, image1),
            Obstacle(250, 510, 50, 50, 0, image1),
            Obstacle(280, 340, 50, 50, 0, image1),
            Obstacle(430, 210, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(100, 220, 30, 30, 10, image2),
            Scorepoint(200, 220, 30, 30, 10, image2),
            Scorepoint(250, 320, 30, 30, 10, image2),
            Scorepoint(300, 420, 30, 30, 10, image2),
            Scorepoint(350, 520, 30, 30, 10, image2),
            Scorepoint(400, 620, 30, 30, 10, image2),
            Scorepoint(450, 220, 30, 30, 10, image2),
            Scorepoint(500, 320, 30, 30, 10, image2),
            Scorepoint(550, 420, 30, 30, 10, image2),
            Scorepoint(600, 520, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(170,220,pygame.Color(255,0,0)),
            ColorChange(400,600,pygame.Color(0,0,255))
        ],
        offset = 800
    )

    block7 = Block(
        obstacles = [
            Obstacle(190, 680, 50, 50, 0, image1),
            Obstacle(260, 530, 50, 50, 0, image1),
            Obstacle(290, 360, 50, 50, 0, image1),
            Obstacle(440, 220, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(110, 230, 30, 30, 10, image2),
            Scorepoint(210, 230, 30, 30, 10, image2),
            Scorepoint(260, 330, 30, 30, 10, image2),
            Scorepoint(310, 430, 30, 30, 10, image2),
            Scorepoint(360, 530, 30, 30, 10, image2),
            Scorepoint(410, 630, 30, 30, 10, image2),
            Scorepoint(460, 230, 30, 30, 10, image2),
            Scorepoint(510, 330, 30, 30, 10, image2),
            Scorepoint(560, 430, 30, 30, 10, image2),
            Scorepoint(610, 530, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(100,200,pygame.Color(255,0,0)),
            ColorChange(500,400,pygame.Color(0,0,255))
        ],
        offset = 800
    )

    block8 = Block(
        obstacles = [
            Obstacle(200, 700, 50, 50, 0, image1),
            Obstacle(270, 550, 50, 50, 0, image1),
            Obstacle(300, 380, 50, 50, 0, image1),
            Obstacle(450, 230, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(120, 240, 30, 30, 10, image2),
            Scorepoint(220, 240, 30, 30, 10, image2),
            Scorepoint(270, 340, 30, 30, 10, image2),
            Scorepoint(320, 440, 30, 30, 10, image2),
            Scorepoint(370, 540, 30, 30, 10, image2),
            Scorepoint(420, 640, 30, 30, 10, image2),
            Scorepoint(470, 240, 30, 30, 10, image2),
            Scorepoint(520, 340, 30, 30, 10, image2),
            Scorepoint(570, 440, 30, 30, 10, image2),
            Scorepoint(620, 540, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(250,330,pygame.Color(255,0,0)),
            ColorChange(500,300,pygame.Color(0,0,255))
        ],
        offset = 800
    )

    block9 = Block(
        obstacles = [
            Obstacle(210, 720, 50, 50, 0, image1),
            Obstacle(280, 570, 50, 50, 0, image1),
            Obstacle(310, 400, 50, 50, 0, image1),
            Obstacle(460, 240, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(130, 250, 30, 30, 10, image2),
            Scorepoint(230, 250, 30, 30, 10, image2),
            Scorepoint(280, 350, 30, 30, 10, image2),
            Scorepoint(330, 450, 30, 30, 10, image2),
            Scorepoint(380, 550, 30, 30, 10, image2),
            Scorepoint(430, 650, 30, 30, 10, image2),
            Scorepoint(480, 250, 30, 30, 10, image2),
            Scorepoint(530, 350, 30, 30, 10, image2),
            Scorepoint(580, 450, 30, 30, 10, image2),
            Scorepoint(630, 550, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(140,280,pygame.Color(0,0,255)),
            ColorChange(450,670,pygame.Color(0,255,0))
        ],
        offset = 800
    )

    block10 = Block(
        obstacles = [
            Obstacle(220, 740, 50, 50, 0, image1),
            Obstacle(290, 590, 50, 50, 0, image1),
            Obstacle(320, 420, 50, 50, 0, image1),
            Obstacle(470, 250, 50, 50, 0, image1),
        ],
        score_points = [
            Scorepoint(140, 260, 30, 30, 10, image2),
            Scorepoint(240, 260, 30, 30, 10, image2),
            Scorepoint(290, 360, 30, 30, 10, image2),
            Scorepoint(340, 460, 30, 30, 10, image2),
            Scorepoint(390, 560, 30, 30, 10, image2),
            Scorepoint(440, 660, 30, 30, 10, image2),
            Scorepoint(490, 260, 30, 30, 10, image2),
            Scorepoint(540, 360, 30, 30, 10, image2),
            Scorepoint(590, 460, 30, 30, 10, image2),
            Scorepoint(640, 560, 30, 30, 10, image2),
        ],
        color_changers = [
            ColorChange(270,380,pygame.Color(255,0,0)),
            ColorChange(400,550,pygame.Color(0,255,0))
        ],
        offset = 800
    )

    return [block1, block2, block3, block4, block5, block6, block7, block8, block9, block10]