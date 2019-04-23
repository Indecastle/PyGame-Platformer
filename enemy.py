import pygame
import entity, blocks

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet

class Enemy(entity.Entity):
    player = None
    health = 3
    max_health = 3
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    image_stay = None
    direction = "R"
    _timer1, timer1 = 100, 100
    _timer2, timer2 = 100, 30

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

        if self._timer1> 0:
            self._timer1 -= 1
        else:
            self._timer1 = self.timer1
            self.direction =  'R' if self.direction == 'L' else 'L'
            self.change_x *= -1

        if self._timer2 > 0:
            self._timer2 -= 1
        else:
            ll = self.rect.x - self.player.rect.x
            center_y = self.rect.y + self.rect.height / 2
            if abs(ll) < constants.SW-650 and (ll < 0 and self.direction == 'R' or ll > 0 and self.direction == 'L') and self.player.rect.top < center_y < self.player.rect.bottom:
                self._timer2 = self.timer2

                bullet = entity.Bullet(blocks.BULLET_LASER_PURPLE)
                bullet.change_x = -10 if self.direction == 'L' else 10
                bullet.change_y = 0
                bullet.rect.x = self.rect.x
                bullet.rect.y = self.rect.y + self.rect.height/2
                bullet.player = self.player
                bullet.level = self.level
                self.level.advance_list.add(bullet)


    def timers(self, timer):
        self._timer1 = self.timer1 = timer



class Enemy2(entity.Entity):
    player = None
    health = 3
    max_health = 3
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    image_stay = None
    direction = "L"
    _timer1, timer1 = 100, 100
    _timer2, timer2 = 100, 30

    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/pack/Extra animations and enemies/Enemy sprites/slime.png")
        image = sprite_sheet.get_image(0, 0, 49,34)
        self.walking_frames_r.append(image)
        sprite_sheet = SpriteSheet("images/pack/Extra animations and enemies/Enemy sprites/slime_walk.png")
        image = sprite_sheet.get_image(0, -3, 57, 34)
        self.walking_frames_r.append(image)

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

        if self._timer1> 0:
            self._timer1 -= 1
        else:
            self._timer1 = self.timer1
            self.direction =  'R' if self.direction == 'L' else 'L'
            self.change_x *= -1

        if self._timer2 > 0:
            self._timer2 -= 1
        else:
            ll = self.rect.x - self.player.rect.x
            center_y = self.rect.y + self.rect.height / 2
            if abs(ll) < constants.SW - 650 and (
                    ll < 0 and self.direction == 'L' or ll > 0 and self.direction == 'R') and self.player.rect.top < center_y < self.player.rect.bottom:
                self._timer2 = self.timer2

                bullet = entity.Bullet(blocks.BULLET_LASER_PURPLE)
                bullet.change_x = -10 if self.direction == 'R' else 10
                bullet.change_y = 0
                bullet.rect.x = self.rect.x
                bullet.rect.y = center_y
                bullet.player = self.player
                bullet.level = self.level
                self.level.advance_list.add(bullet)

    def death(self):
        self.kill()
