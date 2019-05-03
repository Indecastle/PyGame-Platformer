import pygame
import entity

import constants, settings
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet
import blocks
import enemy, images


class Player(entity.Entity):
    stats = None
    health = 8
    max_health = 8
    collide_damage = 3
    pos_move = 0
    speed_X = 5
    walking_frames_l = []
    walking_frames_r = []
    direction = "R"

    _timer1, timer1 = 100, 5 # fire
    _timer2, timer2 = 200,200 # time_god
    _timer3, timer3 = 10,10 # time_god_2
    time_god = False
    time_god_2 = False
    temp_image = None  # for alpha impulse

    cheat_god = False
    cheat_fun = False


    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)


        data = images.player
        sprite_sheet = SpriteSheet(data[0])
        for sprite in data[1]:
            image = sprite_sheet.get_image(*sprite)
            self.walking_frames_r.append(image)
        for sprite in data[1][-2:0:-1]:
            image = sprite_sheet.get_image(*sprite)
            self.walking_frames_r.append(image)

        for image in self.walking_frames_r[::-1]:
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

        self.image_stay = sprite_sheet.get_image(*data[2], reverse=True)
        self.image_jump = sprite_sheet.get_image(*data[3], reverse=True)
        self.image_fire = sprite_sheet.get_image(*data[4], reverse=True)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        rect2 = self.rect.inflate(-30,-30)
        self.shift_rect = ((self.rect.width  - rect2.width)/2 , self.rect.height - rect2.height)
        self.rect = rect2

        if settings.difficulty == "EASY":
            self.max_health = self.health = 8
        elif settings.difficulty == "MEDIUM":
            self.max_health = self.health = 4
        elif settings.difficulty == "HARD":
            self.max_health = self.health = 2

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

        enemy = pygame.sprite.spritecollideany(self, self.level.enemy_list, False)
        if enemy is not None and not self.time_god:
            enemy.collide_hit_to(self)

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

        enemy = pygame.sprite.spritecollideany(self, self.level.enemy_list, False)
        if enemy is not None and not self.time_god:
            if self.change_y > 0:
                enemy.collide_hit_me(self)
            else:
                enemy.collide_hit_to(self)


        self.pos_move += self.change_x

        if self.change_y == 0:
            if self.direction == "R":
                if self.change_x != 0:
                    frame = (self.pos_move // 60) % len(self.walking_frames_r)
                    self.temp_image = self.walking_frames_r[frame]
                else:
                    self.pos_move = 0
                    self.temp_image = self.image_stay[0]
            else:
                if self.change_x != 0:
                    frame = (self.pos_move // 60) % len(self.walking_frames_l)
                    self.temp_image = self.walking_frames_l[frame]
                else:
                    self.pos_move = 0
                    self.temp_image = self.image_stay[1]
        else:
            if self.direction == "R":
                self.temp_image = self.image_jump[0]
            else:
                self.temp_image = self.image_jump[1]

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
            self.stats.count_jump += 1

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
        #self.stats.HUD.rend_health()
        self.time_god = True
        if self.health <= 0:
            self.death()

    def death(self):
        pygame.time.set_timer(constants.EVENT_LOSE, 10)
        self.stats.count_death += 1

    def fire(self):
        if self._timer1 == 0:
            self._timer1 = self.timer1
            self.stats.count_fire += 1

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

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.go_left()
                if event.key == pygame.K_RIGHT:
                    self.go_right()
                if event.key == pygame.K_UP:
                    self.jump()
                if event.key == pygame.K_e:
                    self.fire()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                self.spawn_enemy(pos, 1)
            elif event.button == 3:
                self.spawn_enemy(pos, 2)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.change_x < 0:
                    self.stop()
            if event.key == pygame.K_RIGHT and self.change_x > 0:
                    self.stop()

    def spawn_enemy(self, pos, index):
        if not self.cheat_fun:
            return
        if index == 1:
            enemy.Enemy(pos, (2, 0), self.level, self, 5, 50)
        if index == 2:
            enemy1 = enemy.Enemy2(pos, (2, 0), self.level, self, 1, 10)
            #enemy1.collide_damage = 1
            #enemy1.god = True

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x - self.shift_rect[0], self.rect.y - self.shift_rect[1]))
