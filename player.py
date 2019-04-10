import pygame
import entity

import constants
from platforms import MovingPlatform, LateralPlatform, PlatformOnlyUp
from spritesheet_functions import SpriteSheet


class Player(entity.Entity):
    change_x = 0
    change_y = 0
    speed_jump = -10
    speed_X = 5
    speed_sidestar = 2
    stats = None

    health = 8
    max_health = 8

    pos_move = 0

    walking_frames_l = []
    walking_frames_r = []

    direction = "R"

    levels = None
    level = None

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
                self.image = self.walking_frames_r[frame]
            else:
                frame = (self.pos_move // 40) % (len(self.walking_frames_l) - 2)
                self.image = self.walking_frames_l[frame]
        else:
            if self.direction == "R":
                self.image = self.walking_frames_r[6]
            else:
                self.image = self.walking_frames_l[6]

    def calc_grav(self):
        super().calc_grav()

    def jump(self):
        super().jump()

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -self.speed_X
        self.direction = "L"

    def go_right(self):
        self.change_x = self.speed_X
        self.direction = "R"

    def stop(self):
        self.change_x = 0


    def minus_heal(self):
        self.health -= 1
        self.stats.HUD.rend_health()
        if self.health == 0:
            pygame.time.set_timer(constants.EVENT_CLOSE, 100)


