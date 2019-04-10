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

    def __init__(self, sprite_sheet_data, path="images/tiles_spritesheet.png"):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(path)
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.const_image = self.image

        self.rect = self.image.get_rect()

class PlatformOnlyUp(Platform):
    def onplatform(self, entity):
        x_center = entity.rect.x + entity.rect.width / 2
        diff = x_center - self.rect.x
        if entity.rect.bottom > self.rect.top  and (0 <= diff <= 70):
            entity.rect.bottom = self.rect.top
            entity.change_y = 0

class LateralPlatform(Platform):
    level = None
    inverse = False
    count = 0

    def __init__(self, block, count, inverse = False, block2 = blocks.BLOCK_GRASS_LRIGHT2, path = "images/tiles_spritesheet.png"):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(path)
        image1 = sprite_sheet.get_image(block[0], block[1], block[2], block[3])
        image2 = sprite_sheet.get_image(block2[0], block2[1], block2[2], block2[3])

        if inverse:
            image1 = pygame.transform.flip(image1, True, False)
            image2 = pygame.transform.flip(image2, True, False)

        self.inverse = inverse
        self.size = count * 70
        newimage = pygame.Surface([70 * count, 70 * count]).convert()
        newimage.set_colorkey(constants.BLACK)
        newimage = newimage.convert_alpha()
        if not inverse:
            for i in range(count):
                newimage.blit(image1, (70*i, self.size - 70*(i+1)), (0,0,70,70))
            for i in range(1, count):
                newimage.blit(image2, (70*i, self.size - 70*(i)), (0,0,70,70))
        else:
            for i in range(count):
                newimage.blit(image1, (70*i, 70*i), (0,0,70,70))
            for i in range(count-1):
                newimage.blit(image2, (70*i, 70*(i+1)), (0,0,70,70))
        self.image = newimage
        self.rect = newimage.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y + 70 - self.size

    def check_inblock(self, entity):
        x_center = entity.rect.x + entity.rect.width / 2
        y_bottom = entity.rect.bottom
        if self.rect.left < x_center < self.rect.right  and  self.rect.top < y_bottom < self.rect.bottom:
            return True
        return False

    def check_onplatform(self, entity):
        if not self.check_inblock(entity):
            return False
        x_center = entity.rect.x + entity.rect.width / 2
        diff = x_center - self.rect.x
        y = self.rect.bottom - ((self.size - diff) if self.inverse else diff)
        return entity.rect.bottom >= y and (0 < diff < self.size)

    def onplatform(self, entity, force = False):
        x_center = entity.rect.x + entity.rect.width / 2
        x_center2 = x_center - entity.change_x
        diff2 = x_center2 - self.rect.x
        diff = x_center - self.rect.x
        y = self.rect.bottom - ((self.size - diff) if self.inverse else diff)
        if ((entity.rect.bottom > y or force) and (0 <= diff <= self.size))  or  (entity.rect.bottom < y and (self.size <= diff2 <= self.size+entity.rect.width / 2)):
            entity.rect.bottom = y
            entity.change_y = 0

    def calconplatform(self, entity):
        entity.rect.x -= entity.change_x
        entity.rect.y += 1
        hit = self.check_onplatform(entity)
        entity.rect.x += self.player.change_x
        entity.rect.y -= 1
        if hit and entity.change_y != entity.speed_jump:  # -10 is event of jump
            if entity.change_x > 0:
                entity.rect.x -= 1
            elif entity.change_x < 0:
                entity.rect.x -= -1
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
    player = None

    def update(self):



        # Move up/down
        self.rect.y += self.change_y

        if self.change_y > 0:
            self.rect.y -= self.change_y*2
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                self.player.rect.bottom = self.rect.top + self.change_y*2
                self.player.change_y = 0
            self.rect.y += self.change_y*2

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        



        cur_pos = self.rect.y - self.level.world_shift_y
        if cur_pos > self.boundary_bottom or cur_pos < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift_x
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

        # Move left/right
        self.rect.x += self.change_x
        self.rect.y -= 1
        hit = pygame.sprite.collide_rect(self, self.player)
        self.rect.y += 1
        if hit:
            self.player.rect.x += self.change_x

class MovingTimerPlatform(Platform):
    change_x = 0
    change_y = 0

    _timer_x = 0
    _timer_y = 0
    timer_x = 0
    timer_y = 0
    prioritet = 'X'
    _shift_timer = 0

    level = None
    player = None

    def timers(self, timer_x, timer_y):
        self._timer_x = self.timer_x = timer_x
        self._timer_y = self.timer_y = timer_y



    def update(self):
        # Move up/down
        if self._timer_y > 0:
            self.rect.y += self.change_y

        if self.change_y > 0:
            self.rect.y -= self.change_y*2
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                self.player.rect.bottom = self.rect.top + self.change_y*2
                self.player.change_y = 0
            self.rect.y += self.change_y*2
        else:
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                self.player.rect.bottom = self.rect.top

        

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
        hit = pygame.sprite.collide_rect(self, self.player)
        self.rect.y += 1
        if hit:
            self.player.rect.x += self.change_x
        

     

        
