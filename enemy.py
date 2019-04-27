import pygame
import entity, blocks

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet

class Base_Enemy(entity.Entity):
    collide_damage = 2
    god = False
    impulse_y = -5
    weapon = None

    def collide_hit_me(self, enemy):
        enemy.change_y = self.impulse_y
        enemy.rect.bottom = self.rect.y
        if not self.god:
            self.minus_heal(enemy.collide_damage)

    def collide_hit_to(self, enemy):
        if self.collide_damage > 0:
            if enemy.health % 2 == 0:
                enemy.minus_heal(self.collide_damage)
            else:
                enemy.minus_heal(self.collide_damage - 1)

    def minus_heal(self, damage):
        if self.god:
            return
        super().minus_heal(damage)

class Enemy(Base_Enemy):
    stackFSM = None
    player = None
    health = 3
    max_health = 3
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    image_stay = None
    direction = 'R'
    direction_fire = 'R'
    _timer1, timer1 = 0, 100
    _timer2, timer2 = 0, 30

    def __init__(self, pos, change, level, player):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.walking_frames_l = []
        self.walking_frames_r = []
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

        self.rect.x, self.rect.y = pos
        self.change_x, self.change_y = change
        self.speed_X = change[0]
        self.level = level
        self.player = player
        level.entity_list.add(self)
        level.enemy_list.add(self)
        level.entity_ground_list.add(self)

        self.stackFSM = [self.event_run]

    def update(self):
        super().update()

        self.stackFSM[-1]()

    def timers(self, timer):
        self._timer1 = self.timer1 = timer

    def event_run(self):
        self.pos_move += self.change_x

        if self._timer1 > 0:
            self._timer1 -= 1
        else:
            self._timer1 = self.timer1
            self.direction = 'R' if self.direction == 'L' else 'L'
            self.change_x *= -1

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



        ll = self.rect.x - self.player.rect.x
        center_y = self.rect.y + self.rect.height / 2
        if abs(ll) < constants.SW - 650 and \
                (ll < 0 and self.direction == 'R' or ll > 0 and self.direction == 'L') and \
                self.player.rect.top < center_y < self.player.rect.bottom:
            self.stackFSM.append(self.event_fire)
            self.direction_fire = self.direction

    def event_fire(self):
        self.rect.x -= self.change_x # stop run

        ll = self.rect.x - self.player.rect.x
        center_y = self.rect.bottom - self.rect.height / 3
        if abs(ll) < constants.SW - 650 and self.player.rect.top < center_y < self.player.rect.bottom:
            if not (ll < 0 and self.direction_fire == 'R' or ll > 0 and self.direction_fire == 'L'):
                self.direction_fire = ('R' if self.direction_fire == 'L' else 'L')
                frame = (self.pos_move // 40) % (len(self.walking_frames_l))
                if self.direction_fire == 'R':
                    self.image = self.walking_frames_r[frame]
                else:
                    self.image = self.walking_frames_l[frame]

            if self._timer2 > 0:
                self._timer2 -= 1
            else:
                    self._timer2 = self.timer2

                    bullet = entity.Bullet(blocks.BULLET_LASER_PURPLE)
                    bullet.change_x = -10 if self.direction_fire == 'L' else 10
                    bullet.change_y = 0
                    bullet.rect.x = self.rect.x + (self.rect.width if self.direction_fire=='R' else 0)
                    bullet.rect.y = center_y
                    bullet.player = self.player
                    bullet.level = self.level
                    self.level.advance_list.add(bullet)
        else:
            self.stackFSM.pop()

    def death(self):
        self.kill()
        self.player.stats.up_score(50)




class Enemy2(Base_Enemy):
    player = None
    health = 3
    max_health = 3
    impulse_y = -11
    pos_move = 0
    walking_frames_l = []
    walking_frames_r = []
    image_stay = None
    direction = "L"
    _timer1, timer1 = 100, 100
    _timer2, timer2 = 100, 30

    def __init__(self, pos, change, level, player):
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

        self.rect.x, self.rect.y = pos
        self.change_x, self.change_y = change
        self.speed_X = change[0]
        self.level = level
        self.player = player
        level.entity_list.add(self)
        level.enemy_list.add(self)
        level.entity_ground_list.add(self)

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

    def death(self):
        self.kill()
        self.player.stats.up_score(20)
