import pygame

import constants
import platforms
from spritesheet_functions import SpriteSheet

level_list, current_level, current_level_no = None, None, None

FINISH_YELLOW    = (203,0,    202,144,  144,434)
FINISH_ORANGE    = (274,144,  216,216,  203,72)
FINISH_BLUE      = (275,72,   275,0,    215,504)
FINISH_GREEN     = (216,432,  216,360,  216,288)


class Finish(pygame.sprite.Sprite):
    player = None

    def __init__(self, sprite_sheet_data):
        super().__init__()

        sprite_sheet = SpriteSheet("images/items_spritesheet.png")
        # Grab the image for this platform
        self.image_list = []
        self.image_list.append(sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], 72, 72))
        self.image_list.append(sprite_sheet.get_image(sprite_sheet_data[2], sprite_sheet_data[3], 72, 72))
        self.image_list.append(sprite_sheet.get_image(sprite_sheet_data[4], sprite_sheet_data[5], 72, 72))
        self.image = self.image_list[0]
        self.current_image_index = 0

        self.rect = self.image.get_rect()
        self.timer = 30


    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.current_image_index = (self.current_image_index + 1) % 2
            self.image = self.image_list[self.current_image_index]
            self.timer = 30

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.nextLevel()

    def nextLevel(self):
        global level_list, current_level, current_level_no
        if current_level_no < len(level_list)-1:
            current_level_no += 1
            current_level = level_list[current_level_no]
            self.player.level = current_level
            self.player.rect.x = 2000
           


class Level():
    platform_list = None
    enemy_list = None
    advance_list = None

    # Background image
    background = None
    background_fill = None

    # scrolled left/right and up/down
    world_shift_x = 0
    world_shift_y = 0
    level_limit = -1000


    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.advance_list = pygame.sprite.Group()
        self.player = player


    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

        SW = constants.SCREEN_WIDTH
        SH = constants.SCREEN_HEIGHT
        half_SW, half_SH, half2_SH = SW//2, SH//2, SH//3

        # shift the world left (-x)
        if self.player.rect.x > half_SW:
            diff = self.player.rect.x - half_SW
            self.player.rect.x = half_SW
            print(1)
            self.shift_world(-diff, 0)

        # shift the world right (+x)
        if self.player.rect.x < half_SW:
            real_pos = self.player.rect.x - self.world_shift_x
            if real_pos > half_SW:
                diff = half_SW - self.player.rect.x
                self.player.rect.x = half_SW
                print(2)
                self.shift_world(diff, 0)
            elif real_pos <= 0:
                self.player.rect.x = 0

        # shift the world up (real +y)
        if self.player.rect.y < half2_SH:
            diff = half2_SH - self.player.rect.y
            self.player.rect.y = half2_SH
            self.shift_world(0, diff)

        # shift the world down (real -y)
        if self.player.rect.y > half_SH:
            real_pos = self.player.rect.y - self.world_shift_y
            if real_pos < half_SH:
                diff = self.player.rect.y - half_SH
                self.player.rect.y = half_SH
                self.shift_world(0, -diff)
            elif real_pos >= SH:
                self.player.rect.bottom = SH

        self.advance_list.update()


    def draw(self, screen):
        screen.fill(self.background_fill)
        screen.blit(self.background,(self.world_shift_x // 3, self.world_shift_y // 3+300))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.advance_list.draw(screen)


    def shift_world(self, shift_x, shift_y):

        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        for platform in self.platform_list:
            platform.rect.x += shift_x
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.rect.y += shift_y

        for object in self.advance_list:
            object.rect.x += shift_x
            object.rect.y += shift_y


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):

        # Call the parent constructor
        Level.__init__(self, player)

        self.background_fill = (31, 73, 125)
        self.background = pygame.image.load("images/background_01.png").convert_alpha()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1500

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]

        mega_shift = constants.SCREEN_HEIGHT - 600 # only for level_01 (800x600)

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2] + mega_shift
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 500 + mega_shift
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = Finish(FINISH_ORANGE)
        block.rect.x = 2000
        block.rect.y = 500 + mega_shift
        block.player = self.player
        self.advance_list.add(block)




class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background_fill = (75, 172, 198)
        self.background = pygame.image.load("images/background_02.png").convert_alpha()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

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
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]

        mega_shift = constants.SCREEN_HEIGHT - 600 # only for level_02 (800x600)

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2] + mega_shift
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_RIGHT)
        block.rect.x = 1500
        block.rect.y = 300 + mega_shift
        block.boundary_top = 100 + mega_shift
        block.boundary_bottom = 550 + mega_shift
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
