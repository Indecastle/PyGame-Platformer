from random import randint
from constants import SW, SH
from spritesheet_functions import *
import blocks


class Background_live:
    def __init__(self):
        self.background_fill = (75, 172, 198)
        self.width = SW
        self.height = SH
        self.objects = []
        self.clk = 3
        sprite_sheet = SpriteSheet(blocks.PATH_02)
        for i in range(10):
            image = sprite_sheet.get_image(*blocks.CLOUD_1)
            self.objects.append([image, image.get_rect(topleft=(SW+randint(0, 300), randint(0,SH))), randint(-2,-1)])
        print(self.objects)

    def update(self):
        for obj in self.objects:
            self.clk = (self.clk+1)%3
            if obj[1].x < -100:
                obj[1].x = SW + randint(0, 300)
                obj[1].y = randint(0,SH)
                obj[2] = randint(-2,-1)
            else:
                if self.clk % 3 == 0:
                    obj[1].x += obj[2]


    def draw(self,surface):
        surface.fill(self.background_fill)
        for obj in self.objects:
            surface.blit(obj[0], obj[1])