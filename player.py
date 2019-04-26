import pygame
import entity

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet
import blocks


class Player(entity.Entity):
    stats = None
    health = 8
    max_health = 8
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    direction = "R"

    _timer1, timer1 = 100, 5 # fire
    _timer2, timer2 = 200,200 # time_god
    _timer3, timer3 = 10,10 # time_god_2
    time_god = False
    time_god_2 = False
    cheat_god = False
    temp_image = None


    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.time_god_show()

        if self._timer1 > 0:
            self._timer1 -= 1
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.all_platforms_list, False)
        for block in block_hit_list:
            if isinstance(block, LateralPlatform):
                block.calconplatform(self)
            elif isinstance(block, PlatformOnlyUp):
                pass
            else:
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.all_platforms_list, False)
        for block in block_hit_list:
            if isinstance(block, LateralPlatform) or isinstance(block, PlatformOnlyUp):
                block.onplatform(self)
            else:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.change_y = 0

        self.pos_move += self.change_x

        if self.change_y == 0:
            if self.direction == "R":
                frame = (self.pos_move // 40) % (len(self.walking_frames_r) - 2)
                self.temp_image = self.walking_frames_r[frame]
            else:
                frame = (self.pos_move // 40) % (len(self.walking_frames_l) - 2)
                self.temp_image = self.walking_frames_l[frame]
        else:
            if self.direction == "R":
                self.temp_image = self.walking_frames_r[6]
            else:
                self.temp_image = self.walking_frames_l[6]

        if self.image != self.temp_image:
            self.image = self.temp_image.copy()
        self.rend_alpha()

    def calc_grav(self):
        super().calc_grav()
        # See if we are on the ground.
        # if self.rect.bottom > constants.SCREEN_HEIGHT and self.change_y >= 0:
        #     self.change_y = 0
        #     self.rect.bottom = constants.SCREEN_HEIGHT

    def jump(self):
        if super().jump():
            #self.minus_heal()
            pass

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -self.speed_X
        self.direction = "L"

    def go_right(self):
        self.change_x = self.speed_X
        self.direction = "R"

    def stop(self):
        self.change_x = 0


    def minus_heal(self, damage):
        if self.cheat_god or self.time_god:
            return
        self.health -= damage
        self.stats.HUD.rend_health()
        self.time_god = True
        if self.health == 0:
            self.death()

    def death(self):
        pygame.time.set_timer(constants.EVENT_LOSE, 10)

    def fire(self):
        if self._timer1 == 0:
            self._timer1 = self.timer1

            bullet = entity.Bullet(blocks.BULLET_LASER_PURPLE_DOT, False)
            bullet.damage = 1
            bullet.change_x = 10 if self.direction == 'R' else -10
            bullet.change_y = 0
            bullet.rect.x = self.rect.x + (self.rect.width if self.direction=='R' else 0)
            bullet.rect.y = self.rect.y + self.rect.height/2
            bullet.player = self
            bullet.level = self.level
            self.level.advance_list.add(bullet)

    def time_god_show(self):
        if not self.time_god:
            return None

        if self._timer2 > 0:
            self._timer2 -= 1
        else:
            self._timer2 = self.timer2
            self.time_god = False

        if self._timer3 > 0:
            self._timer3 -= 1
        else:
            self._timer3 = self.timer3
            self.time_god_2 = not self.time_god_2

        if not self.time_god and self.time_god_2:
            self.time_god_2 = False

    def rend_alpha(self):
        if self.time_god_2:
            self.image.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
