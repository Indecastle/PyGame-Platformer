import pygame

import constants
import blocks
import platforms
from spritesheet_functions import SpriteSheet, gen_block
from super_level import *


class Level_03(Level):
    """ Definition for level 1. """

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)
        self.mega_shift = constants.SCREEN_HEIGHT - 600  # only for level_01 (800x600)

        self.background_fill = (162, 231, 238)

        self.background = pygame.Surface([3000, 2000]).convert_alpha()
        self.background.set_colorkey(constants.BLACK)
        self.background = self.background.convert_alpha()
        sprite_sheet2 = pygame.image.load(blocks.PATH_02).convert_alpha()
        sprite_sheet2.set_colorkey(constants.BLACK)

        background = self.background
        gen_block(background, (0,0), 10, sprite_sheet2, blocks.CLOUD_1)
        gen_block(background, (400,800), 10, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (600,1600), 10, sprite_sheet2, blocks.CLOUD_2)


        self.background_near = pygame.Surface([3000, 1000]).convert()
        self.background_near.set_colorkey(constants.BLACK)
        self.background_near = self.background_near.convert_alpha()

        background = self.background_near
        sprite_sheet = pygame.image.load(blocks.PATH_01).convert_alpha()
        sprite_sheet.set_colorkey(constants.BLACK)
        
        shift = SH - self.mega_shift
        gen_block(background, (0,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (1*70,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (2*70,shift-70), 3, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (3*70,shift-70), 3, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (4*70,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (5*70,shift-70), 5, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (6*70,shift-70), 5, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (7*70,shift-70), 6, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (8*70,shift-70), 7, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (9*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (10*70,shift-70), 9, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (11*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background, (12*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)



        self.level_limit = -1500
        self.start_pos = (120, constants.SCREEN_HEIGHT - player.rect.height - 500)

        # Array with type of platform, and x, y location of the platform.
        level = [ [blocks.BLOCK_GRASS_LEFT, 0*70, shift-5*70],
                  [blocks.BLOCK_GRASS_RIGHT, 1*70, shift-5*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 2*70, shift-4*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 3*70, shift-4*70],
                  [blocks.BLOCK_GRASS_LEFT, 4*70, shift-5*70],
                  [blocks.BLOCK_GRASS_LEFT, 5*70, shift-6*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 6*70, shift-6*70],
                  [blocks.BLOCK_GRASS_LEFT, 7*70, shift-7*70],
                  [blocks.BLOCK_GRASS_LEFT, 8*70, shift-8*70],
                  [blocks.BLOCK_GRASS_LEFT, 9*70, shift-9*70],
                  [blocks.BLOCK_GRASS_UP, 10*70, shift-10*70],
                  [blocks.BLOCK_GRASS_LEFT, 11*70, shift-9*70],
                  [blocks.BLOCK_GRASS_RIGHT, 12*70, shift-9*70],
                  ]

        

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2] + self.mega_shift
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 500 + self.mega_shift
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = Finish(FINISH_ORANGE)
        block.rect.x = 2000
        block.rect.y = constants.SCREEN_HEIGHT - block.rect.height
        block.player = self.player
        self.advance_list.add(block)
