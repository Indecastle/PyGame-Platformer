import pygame
import entity

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet

class Enemy(entity.Entity):
    health = 8
    max_health = 8
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    image_stay = None
    direction = "R"
    _timer, timer = 100, 100

    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/pack/Base pack/Player/p2_spritesheet.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(72*2, 0, 66, 92)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(72*3, 0, 66, 92)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(72*2, 93*1, 66, 92)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        for image in self.walking_frames_r:
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()

    def update(self):
        super().update()

        self.pos_move += self.change_x

        if self.change_y == 0:
            if self.direction == "R":
                frame = (self.pos_move // 40) % (len(self.walking_frames_r))
                self.image = self.walking_frames_r[frame]
            else:
                frame = (self.pos_move // 40) % (len(self.walking_frames_l))
                self.image = self.walking_frames_l[frame]
        else:
            if self.direction == "R":
                self.image = self.walking_frames_r[1]
            else:
                self.image = self.walking_frames_l[1]

        if self._timer > 0:
            self._timer -= 1
        else:
            self._timer = self.timer
            self.direction =  'R' if self.direction == 'L' else 'L'
            self.change_x *= -1


    def timers(self, timer_x):
        self._timer = self.timer = timer