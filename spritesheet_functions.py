"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame

import constants

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite_sheet.set_colorkey(constants.BLACK)
        self.sprite_sheet = self.sprite_sheet.convert_alpha()

    def get_image(self, x, y, width, height, count = 1):

        # Create a new blank image
        image = pygame.Surface([width*count, height]).convert()
        # Assuming black works as the transparent color
        image.set_colorkey(constants.BLACK)
        image = image.convert_alpha()

        # Copy the sprite from the large sheet onto the smaller image
        for i in range(count):
            image.blit(self.sprite_sheet, (width*i, 0), (x, y, width, height))

        # Return the image
        return image


def gen_block(background, pos, height, count, sprite_sheet, block=(0,0, 70, 70)):
    for j in range(count):
        for i in range(height):
            background.blit(sprite_sheet, (pos[0] + block[2]*j, pos[1]-i*block[3]), (block[0], block[1], block[2], block[3]))