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
        #self.mega_shift = SH - 900  # only for level_01 (1600x900)

        self.background_fill = (162, 231, 238)

        self.background = pygame.Surface([3000, 3000]).convert()
        self.background.set_colorkey(constants.BLACK)
        self.background = self.background.convert_alpha()
        sprite_sheet2 = pygame.image.load(blocks.PATH_02).convert_alpha()
        sprite_sheet2.set_colorkey(constants.BLACK)

        background = self.background
        gen_block(background, (0,3000 - 1300), 1, sprite_sheet2, blocks.CLOUD_1)
        gen_block(background, (400,3000 - 1100), 1, sprite_sheet2, blocks.CLOUD_1)
        gen_block(background, (600,3000 - 100), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (700,3000 - 600), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (800,3000 - 800), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (1000,3000 - 400), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (1600,3000 - 700), 1, sprite_sheet2, blocks.CLOUD_2)

        gen_block(background, (1600, 3000 - 500), 1, sprite_sheet2, blocks.CLOUD_1)
        gen_block(background, (2000, 3000 - 1100), 1, sprite_sheet2, blocks.CLOUD_1)
        gen_block(background, (2200, 3000 - 1000), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (2300, 3000 - 600), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (2400, 3000 - 800), 1, sprite_sheet2, blocks.CLOUD_2)
        gen_block(background, (2600, 3000 - 400), 1, sprite_sheet2, blocks.CLOUD_2)


        self.background_near = pygame.Surface([3000, 1000]).convert()
        self.background_near.set_colorkey(constants.BLACK)
        self.background_near = self.background_near.convert_alpha()

        background_near = self.background_near
        sprite_sheet = pygame.image.load(blocks.PATH_01).convert_alpha()
        sprite_sheet.set_colorkey(constants.BLACK)

        shift = SH
        gen_block(background_near, (0,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (1*70,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (2*70,shift-70), 3, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (3*70,shift-70), 3, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (4*70,shift-70), 4, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (5*70,shift-70), 5, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (6*70,shift-70), 5, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (7*70,shift-70), 6, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (8*70,shift-70), 7, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (9*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        #gen_block(background_near, (9*70,shift-8*70), 1, sprite_sheet, blocks.BLOCK_GRASS_LRIGHT2)
        gen_block(background_near, (10*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (11*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (12*70,shift-70), 8, sprite_sheet, blocks.BLOCK_EARTH)

        gen_block(background_near, (12 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (13 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (14 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (15 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (16 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (17 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (18 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)
        gen_block(background_near, (19 * 70, shift - 70), 8, sprite_sheet, blocks.BLOCK_EARTH)



        self.level_limit = -1500
        self.start_pos = (120, SH - player.rect.height - 500)

        # Array with type of platform, and x, y location of the platform.
        level = [ [blocks.BLOCK_GRASS_LEFT, 0*70, shift-5*70],
                  [blocks.BLOCK_GRASS_RIGHT, 1*70, shift-5*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 2*70, shift-4*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 3*70, shift-4*70],
                  [blocks.BLOCK_GRASS_LEFT, 4*70, shift-5*70],
                  [blocks.BLOCK_GRASS_LEFT, 5*70, shift-6*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 6*70, shift-6*70],
                  [blocks.BLOCK_GRASS_LEFT, 7*70, shift-7*70],
                  [blocks.BLOCK_GRASS_LRIGHT, 8*70, shift-8*70, 2, False],
                  #[blocks.BLOCK_GRASS_LRIGHT, 9*70, shift-9*70+1,False],
                  [blocks.BLOCK_GRASS_MIDDLE, 10*70, shift-9*70,  'OnlyUp'],
                  [blocks.BLOCK_GRASS_MIDDLE, 11*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 12*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 13*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 14*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 15*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 16*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 17*70, shift-9*70],
                  [blocks.BLOCK_GRASS_MIDDLE, 18*70, shift-9*70],
                  [blocks.BLOCK_GRASS_RIGHT, 19*70, shift-9*70],

                  [blocks.BLOCK_GRASS_RIGHT, 23 * 70, shift - 1 * 69],

                  [platforms.STONE_PLATFORM_LEFT, 12 * 70, shift - 13 * 70+45],
                  [platforms.STONE_PLATFORM_MIDDLE, 13 * 70, shift - 13 * 70+45],
                  [platforms.STONE_PLATFORM_MIDDLE, 14 * 70, shift - 13 * 70+45],
                  [platforms.STONE_PLATFORM_RIGHT, 15 * 70, shift - 13 * 70+45],
                  ]


        for platform in level:
            if len(platform) == 5:
                block = platforms.LateralPlatform(platform[0], platform[3], platform[4])
                self.lateral_list.add(block)
                block.set_pos(platform[1], platform[2])
            elif len(platform) == 4:
                if platform[3] == 'OnlyUp':
                    block = platforms.PlatformOnlyUp(platform[0])
                    self.platform_list.add(block)
                    block.rect.x = platform[1]
                    block.rect.y = platform[2]
            else:
                block = platforms.Platform(platform[0])
                self.platform_list.add(block)
                block.rect.x = platform[1]
                block.rect.y = platform[2]
            block.player = self.player
            block.level = self
            self.all_platforms_list.add(block)


        # Add a custom moving platform
        block = platforms.MovingTimerPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 950
        block.rect.y = shift - 9 * 70
        block.timers(180, 140)
        block.prioritet = 'X'
        block.change_x = 3
        block.change_y = 4
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        self.all_platforms_list.add(block)

        block = Finish(FINISH_ORANGE)
        block.rect.x = 2000
        block.rect.y = SH - block.rect.height
        block.player = self.player
        self.advance_list.add(block)
