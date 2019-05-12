"""
Module for managing platforms.
"""
import pygame
from spritesheet_functions import SpriteSheet
import constants, blocks

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data, count=(1,1), path="images/tiles_spritesheet.png"):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(path)
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(*sprite_sheet_data, count)
        self.const_image = self.image

        self.rect = self.image.get_rect()

class PlatformOnlyUp(Platform):
    def onplatform(self, entity):
        x_center = entity.rect.x + entity.rect.width / 2
        diff = x_center - self.rect.x
        if entity.rect.bottom > self.rect.top  and (0 <= diff < self.rect.width):
            entity.rect.bottom = self.rect.top
            entity.change_y = 0

class LateralPlatform(Platform):
    level = None
    inverse = False
    count = 0

    def __init__(self, block, count, inverse = False, block2 = blocks.BLOCK_GRASS_LRIGHT2, path = "images/tiles_spritesheet.png"):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(path)
        image1 = sprite_sheet.get_image(*block)
        image2 = sprite_sheet.get_image(*block2)
        width = image1.get_rect().width
        height = image1.get_rect().height

        if inverse:
            image1 = pygame.transform.flip(image1, True, False)
            image2 = pygame.transform.flip(image2, True, False)

        self.inverse = inverse
        self.size_one = (width,height)
        self.size_x = count * width
        self.size_y = count * height
        self.diff_size = self.size_y/self.size_x
        newimage = pygame.Surface([width * count, height * (count+1)]).convert()
        newimage.set_colorkey(constants.BLACK)
        newimage = newimage.convert_alpha()
        if not inverse:
            for i in range(count):
                newimage.blit(image1, (width*i, self.size_y - height*(i+1)))
            for i in range(count):
                newimage.blit(image2, (width*i, self.size_y - height*(i)))
        else:
            for i in range(count):
                newimage.blit(image1, (width*i, height*i))
            for i in range(count):
                newimage.blit(image2, (width*i, height*(i+1)))
        self.image = newimage
        self.rect = newimage.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        if self.inverse:
            self.rect.y = y
        else:
            self.rect.y = y + self.size_one[1] - self.size_y

    def check_inblock(self, entity) -> bool:
        x_center = entity.rect.x + entity.rect.width // 2
        y_bottom = entity.rect.bottom
        if self.rect.left < x_center < self.rect.right  and  self.rect.top < y_bottom < self.rect.bottom:
            return True
        return False

    def check_onplatform(self, entity) -> bool:
        if not self.check_inblock(entity):
            return False
        x_center = entity.rect.x + entity.rect.width // 2
        diff = x_center - self.rect.x
        y = self.rect.bottom - ((self.size_y - diff) if self.inverse else (diff*self.diff_size)) - 70
        return entity.rect.bottom >= y and (0 < diff < self.size_x)

    def onplatform(self, entity, force = False):
        x_center = entity.rect.x + entity.rect.width // 2
        x_center2 = x_center - entity.change_x
        diff2 = x_center2 - self.rect.x
        diff = x_center - self.rect.x
        y = self.rect.bottom - ((self.size_y - diff) if self.inverse else (diff*self.diff_size)) - 70
        if ((entity.rect.bottom > y or force) and (0 <= diff <= self.size_x))  or  (entity.rect.bottom < y and \
            (self.size_x <= diff2 <= self.size_x+entity.rect.width / 2 and not self.inverse or -entity.rect.width / 2 <= diff2 <= 0 and self.inverse)):
            entity.rect.bottom = y
            entity.change_y = 0

    def calconplatform(self, entity):
        entity.rect.x -= entity.change_x
        entity.rect.y += 1
        hit = self.check_onplatform(entity)
        entity.rect.x += entity.change_x
        entity.rect.y -= 1
        if hit and entity.change_y != entity.speed_jump:  # -10 is event of jump
            if entity.change_x > 0:
                entity.rect.x -= entity.speed_X//3
            elif entity.change_x < 0:
                entity.rect.x -= -(entity.speed_X//3)
            if entity.change_x == 0:
                self.onplatform(entity)
            else:
                self.onplatform(entity, True)




class MovingPlatform(Platform):
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None

    def update(self):
        # Move up/down
        self.rect.y += self.change_y

        if self.change_y > 0:
            self.rect.y -= self.change_y*2
            hit = pygame.sprite.collide_rect(self, self.player)
            entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
            for entity in entity_hit_list:
                entity.rect.bottom = self.rect.top + self.change_y*2
                entity.change_y = 0
            self.rect.y += self.change_y*2

        entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
        for entity in entity_hit_list:
            if self.change_y < 0:
                entity.rect.bottom = self.rect.top
            else:
                entity.rect.top = self.rect.bottom


        cur_pos = self.rect.y - self.level.world_shift_y
        if cur_pos > self.boundary_bottom or cur_pos < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift_x
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

        # Move left/right
        self.rect.x += self.change_x
        self.rect.y -= 1
        entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
        self.rect.y += 1
        for entity in entity_hit_list:
            entity.rect.x += self.change_x

class MovingTimerPlatform(Platform):
    change_x = 0
    change_y = 0

    _timer_x = timer_x = 0
    _timer_y = timer_y = 0
    prioritet = 'X'
    _shift_timer = 0

    level = None

    def __init__(self, data, pos, speed, timers, prioritet, level, count=(1,1), path="images/tiles_spritesheet.png"):
        super().__init__(data, count, path)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.change_x = speed[0]
        self.change_y = speed[1]
        self.timers(*timers)
        self.prioritet = prioritet
        self.level = level
        level.platform_list.add(self)
        level.all_platforms_list.add(self)

    def timers(self, timer_x, timer_y):
        self._timer_x = self.timer_x = timer_x
        self._timer_y = self.timer_y = timer_y



    def update(self):
        # Move up/down
        if self._timer_y > 0:
            self.rect.y += self.change_y

            if self.change_y >= 0:
                self.rect.y -= self.change_y*2
                entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
                for entity in entity_hit_list:
                    entity.rect.bottom = self.rect.top + self.change_y*2
                    entity.change_y = 0
                self.rect.y += self.change_y*2

            entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
            for entity in entity_hit_list:
                if self.change_y < 0:
                    entity.rect.bottom = self.rect.top
                else:
                    entity.rect.top = self.rect.bottom

        

        if self._timer_x > 0:
            self._timer_x -= 1
        else:
            if self.prioritet == 'X':
                self._timer_x = self.timer_x
                self._timer_y = self.timer_y
                self.change_x *= -1
                self.change_y *= -1


        if self._timer_y > 0:
            self._timer_y -= 1
        else:
            if self.prioritet == 'Y':
                self._timer_y = self.timer_y
                self._timer_x = self.timer_x
                self.change_y *= -1
                self.change_x *= -1

        if self._timer_x > 0:
            # Move left/right
            self.rect.x += self.change_x
            self.rect.y -= 1
            entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_ground_list, False)
            self.rect.y += 1
            for entity in entity_hit_list:
                entity.rect.x += self.change_x
        

     

        
