"""
Module for managing platforms.
"""
import pygame
from spritesheet_functions import SpriteSheet

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("images/tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()


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

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        
