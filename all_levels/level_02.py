import pygame

import constants
import platforms
from spritesheet_functions import SpriteSheet
from super_level import *
import blocks

class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background_fill = (75, 172, 198)
        self.background = pygame.image.load("images/background_02.png").convert_alpha()
        #self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000
        self.start_pos = (120, constants.SCREEN_HEIGHT - player.rect.height - 200)

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],

                  [platforms.STONE_PLATFORM_LEFT, 1120, 400],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 400],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 400],

                  [platforms.STONE_PLATFORM_LEFT, 1120, 270],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 270],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 270],

                  [blocks.BLOCK_GRASS_MIDDLE, 0 * 70, SH - 130, (100, 1)],
                  ]

        self.mega_shift = constants.SCREEN_HEIGHT - 600 # only for level_02 (800x600)

        for platform in level:
            if len(platform) == 4:
                block = platforms.Platform(platform[0], platform[3])
            else:
                block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2] + self.mega_shift
            block.player = self.player
            self.platform_list.add(block)
            self.all_platforms_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_RIGHT)
        block.rect.x = 1500
        block.rect.y = 300 + self.mega_shift
        block.boundary_top = 100 + self.mega_shift
        block.boundary_bottom = 550 + self.mega_shift
        block.change_y = -3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        self.all_platforms_list.add(block)

        block = Finish(FINISH_ORANGE)
        block.rect.x = 2000
        block.rect.y = constants.SCREEN_HEIGHT - block.rect.height
        block.player = self.player
        self.advance_list.add(block)
