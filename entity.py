import pygame

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet


class Entity(pygame.sprite.Sprite):
    health = 3
    max_health = 3
    change_x = 0
    change_y = 0
    speed_jump = -10
    speed_X = 0
    speed_sidestar = 2

    levels = None
    level = None

    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([70,70])
        self.rect = self.image.get_rect()

    def update(self):
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

            # Stop our vertical movement


            #if isinstance(block, MovingPlatform):
            #    self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.level.gravity

        if  self.rect.top - self.level.world_shift_y >= constants.SCREEN_HEIGHT + 100:
            self.death()

        # # See if we are on the ground.
        # if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
        #     self.change_y = 0
        #     self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        lateral_hit_list = []
        if self.level.lateral_list:
            lateral_hit_list = list(filter(lambda block: block.check_inblock(self), self.level.lateral_list))
            platform_hit_list += lateral_hit_list

        if platform_hit_list: # or self.rect.bottom >= constants.SCREEN_HEIGHT:
            canJump = True
            lateral = lateral_hit_list
            if lateral:
                if not any(lat.check_onplatform(self) for lat in lateral):
                    canJump = False
            if canJump:
                self.change_y = self.speed_jump - self.level.gravity
            return canJump
        return False

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -self.speed_X

    def go_right(self):
        self.change_x = self.speed_X

    def stop(self):
        self.change_x = 0

    def death(self):
        self.kill()

    def minus_heal(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death()




class Bullet(pygame.sprite.Sprite):
    damage = 1
    change_x = 0
    change_y = 0
    level = None
    player = None
    is_enemy = True
    time_live = 100

    def __init__(self, data, isenemy = True):
        super().__init__()
        sprite_sheet = SpriteSheet(data[0])
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(data[1][0], data[1][1], data[1][2], data[1][3])
        #self.image = pygame.transform.scale(self.image, (100,10))
        self.rect = self.image.get_rect()
        self.is_enemy = isenemy

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.time_live > 0:
            self.time_live -= 1
        else:
            self.destruct()
        block_hit_list = pygame.sprite.spritecollide(self, self.level.all_platforms_list, False)
        for block in block_hit_list:
            if isinstance(block, LateralPlatform):
                if block.check_onplatform(self):
                    self.destruct()
            elif isinstance(block, PlatformOnlyUp):
                self.destruct()
            else:
                self.destruct()

        if self.is_enemy:
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit:
                self.hit_entity(self.player)
        else:
            enemy = pygame.sprite.spritecollideany(self, self.level.enemy_list, False)
            if enemy is not None:
                self.hit_entity(enemy)

    def destruct(self):
        self.kill()

    def hit_entity(self, entity):
        self.destruct()
        entity.minus_heal(self.damage)



