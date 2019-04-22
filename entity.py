import pygame

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet


class Entity(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    speed_jump = -10
    speed_X = 5
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
            self.change_y += .35

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

        if platform_hit_list or self.rect.bottom >= constants.SCREEN_HEIGHT:
            canJump = True
            lateral = lateral_hit_list
            if lateral:
                if not any(lat.check_onplatform(self) for lat in lateral):
                    canJump = False
            if canJump:
                self.change_y = self.speed_jump - constants.GRAVITY
            return canJump
        return False

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -self.speed_X

    def go_right(self):
        self.change_x = self.speed_X

    def stop(self):
        self.change_x = 0





class Bullet(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    level = None
    player = None
    time_live = 200

    def __init__(self, data):
        super().__init__()
        sprite_sheet = SpriteSheet(data[0])
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(data[1][0], data[1][1], data[1][2], data[1][3])
        #self.image = pygame.transform.scale(self.image, (100,10))
        self.rect = self.image.get_rect()

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

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.hit_player()

    def destruct(self):
        self.kill()

    def hit_player(self):
        self.destruct()
        self.player.minus_heal()


