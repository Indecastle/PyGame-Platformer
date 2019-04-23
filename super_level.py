import pygame

import constants
import platforms
from spritesheet_functions import SpriteSheet
from pymenu import wait



level_list, current_level, current_level_no = None, None, None

FINISH_YELLOW    = (203,0,    202,144,  144,434)
FINISH_ORANGE    = (274,144,  216,216,  203,72)
FINISH_BLUE      = (275,72,   275,0,    215,504)
FINISH_GREEN     = (216,432,  216,360,  216,288)

SW = constants.SCREEN_WIDTH
SH = constants.SCREEN_HEIGHT
half_SW, half_SH, half2_SH, half3_SH = SW//2, SH//2, SH//3, SH//4


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
        self.isNext = False



    def update(self):
        if self.isNext:
            self.animNext()
            return

        if self.timer > 0:
            self.timer -= 1
        else:
            self.current_image_index = (self.current_image_index + 1) % 2
            self.image = self.image_list[self.current_image_index]
            self.timer = 30

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.isNext = True
            self.timer = 60
            self.image = self.image_list[2]


    def animNext(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.nextLevel()

    def nextLevel(self):
        global level_list, current_level, current_level_no
        if current_level_no < len(level_list)-1:
            current_level_no += 1
            wait(False)
            current_level = level_list[current_level_no](self.player)
            self.player.level = current_level
            self.player.rect.x = current_level.start_pos[0]
            self.player.rect.y = current_level.start_pos[1]
            self.player.pos_move = 0
           


class Level():
    platform_list = None
    lateral_list = None
    all_platforms_list = None
    enemy_list = None
    advance_list = None

    # Background image
    background = None
    background_near = None
    background_const = None
    background_fill = None

    # scrolled left/right and up/down
    world_shift_x = 0
    world_shift_y = 0
    level_limit = -1000
    start_pos = (0,0)
    gravity = .35


    def __init__(self, player):
        self.all_platforms_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.lateral_list = pygame.sprite.Group()
        self.advance_list = pygame.sprite.Group()

        self.enemy_list = pygame.sprite.Group()
        #self.enemy_ground_list = pygame.sprite.Group()
        self.enemy_fly_list = pygame.sprite.Group()
        self.entity_list = pygame.sprite.Group()
        self.entity_ground_list = pygame.sprite.Group()

        self.player = player
        self.entity_list.add(player)
        self.entity_ground_list.add(player)

        self.world_shift_x = 0
        self.world_shift_y = 0
        self.score = 0

    def update(self):
        self.entity_list.update()
        self.platform_list.update()




        

        # shift the world left (-x)
        if self.player.rect.x > half_SW:
            real_pos = self.player.rect.x - self.world_shift_x
            if real_pos > half_SW:
                diff = half_SW - self.player.rect.x
                self.player.rect.x = half_SW
                self.shift_world(diff, 0)
            elif real_pos <= 0:
                self.player.rect.x = 0

            diff = self.player.rect.x - half_SW
            self.player.rect.x = half_SW
            self.shift_world(-diff, 0)

        # shift the world right (+x)
        if self.player.rect.x < half_SW:
            real_pos = self.player.rect.x - self.world_shift_x
            if real_pos > half_SW:
                diff = half_SW - self.player.rect.x
                self.player.rect.x = half_SW
                self.shift_world(diff, 0)
            elif real_pos <= 0:
                self.player.rect.x = 0

        # shift the world up (real +y)
        if self.player.rect.y < half3_SH:
            diff = half3_SH - self.player.rect.y
            self.player.rect.y = half3_SH
            self.shift_world(0, diff)

        # shift the world down (real -y)
        if self.player.rect.y >= half_SH:
            real_pos = self.player.rect.y - self.world_shift_y
            if real_pos <= half_SH:
                diff = self.player.rect.y - half_SH
                self.player.rect.y = half_SH
                self.shift_world(0, -diff)

        # if self.player.rect.y >= half_SH:
        #     real_pos = self.player.rect.y - self.world_shift_y
        #     if real_pos <= half_SH:
        #         diff = self.player.rect.y - half_SH
        #         self.player.rect.y = half_SH
        #         self.shift_world(0, -diff)
        #     elif real_pos >= SH:
        #         self.player.rect.bottom = SH

        self.advance_list.update()


    def draw(self, screen):
        screen.fill(self.background_fill)
        if self.background_near is not None:
            screen.blit(self.background,(self.world_shift_x // 3, self.world_shift_y // 3 - 3000 + constants.SCREEN_HEIGHT))
            screen.blit(self.background_near,(self.world_shift_x, self.world_shift_y ))
        else:
            screen.blit(self.background,(self.world_shift_x // 3, self.world_shift_y // 3+self.mega_shift))
            
        

        self.platform_list.draw(screen)
        self.lateral_list.draw(screen)
        self.enemy_list.draw(screen)


    def draw_adv(self, screen):
        self.advance_list.draw(screen)


    def shift_world(self, shift_x, shift_y):

        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        for platform in self.platform_list:
            platform.rect.x += shift_x
            platform.rect.y += shift_y

        for lateral in self.lateral_list:
            lateral.rect.x += shift_x
            lateral.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.rect.y += shift_y

        for object in self.advance_list:
            object.rect.x += shift_x
            object.rect.y += shift_y


