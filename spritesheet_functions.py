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


    def get_image(self, x, y, width, height):

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        # Assuming black works as the transparent color
        image.set_colorkey(constants.BLACK)
        image = image.convert_alpha()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image




def gen_block(background, pos, height, sprite_sheet, block=(0,0, 70, 70)):
    for i in range(height):
        background.blit(sprite_sheet, (pos[0], pos[1]-i*70), (block[0], block[1], block[2], block[3]))