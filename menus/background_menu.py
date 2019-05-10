from random import randint, choice
from constants import SW, SH
from spritesheet_functions import *
import blocks


class Background_live:
    def __init__(self):
        self.background_fill = (162, 231, 238)
        self.width = SW
        self.height = SH
        self.objects = []
        self.custom_tick = 3
        sprite_sheet = SpriteSheet(blocks.PATH_02)
        clouds = (blocks.CLOUD_1, blocks.CLOUD_2, blocks.CLOUD_3)
        for i in range(10):
            image = sprite_sheet.get_image(*choice(clouds))
            self.objects.append([image, image.get_rect(topleft=(randint(0, SW), randint(0, SH))), randint(-2,-1)])

    def update(self):
        for obj in self.objects:
            self.custom_tick = (self.custom_tick+1)%3
            if obj[1].x > -200:
                if self.custom_tick % 3 == 0:
                    obj[1].x += obj[2]
            else:
                obj[1].x = SW + randint(0, 300)
                obj[1].y = randint(0, SH)
                obj[2] = randint(-2, -1)

    def draw(self,surface):
        surface.fill(self.background_fill)
        for obj in self.objects:
            surface.blit(obj[0], obj[1])

backgl = None