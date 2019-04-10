import pygame
from spritesheet_functions import SpriteSheet


class Score(pygame.sprite.Sprite):
    player = None
    level = None

    def __init__(self, data, path="images/items_spritesheet.png"):
        super().__init__()
        sprite_sheet = SpriteSheet(path)
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(data[0], data[1], data[2], data[3])
        self.const_image = self.image

        self.rect = self.image.get_rect()

    def update(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.player.stats.up_score()
            self.level.advance_list.remove(self)