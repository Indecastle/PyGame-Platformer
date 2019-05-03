"""
Global constants
"""
from pygame import USEREVENT

# Colors
BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)

# Screen dimensions
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
SW = SCREEN_WIDTH
SH = SCREEN_HEIGHT
half_SW, half_SH, half2_SH = SW//2, SH//2, SH//3


GRAVITY = .35


EVENT_CLOSE = USEREVENT + 1
EVENT_LOSE = USEREVENT + 2
EVENT_END = USEREVENT + 3