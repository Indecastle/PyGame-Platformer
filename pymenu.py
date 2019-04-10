import pygame
import pygameMenu, os
from pygameMenu.locals import *
import constants



# os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{50},{50}"
pygame.init()
size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Platformer")


ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size


def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    screen.fill(COLOR_BACKGROUND)

def add_event():
    play_menu.disable()
    #my_event = pygame.event.Event(EVENT_CLOSE)
    #pygame.event.post(my_event)
    pygame.time.set_timer(constants.EVENT_CLOSE, 2000)

play_menu = pygameMenu.Menu(screen,
                             dopause=False,
                             font=pygameMenu.fonts.FONT_NEVIS,
                             menu_alpha=85,
                             menu_color=(0, 0, 0),  # Background color
                             menu_color_title=(0, 0, 0),
                             menu_height=int(H_SIZE / 2),
                             menu_width=600,
                             onclose=PYGAME_MENU_CLOSE,  # If this menu closes (press ESC) back to main
                             title='Play menu',
                             title_offsety=5,  # Adds 5px to title vertical position
                             window_height=constants.SH,
                             window_width=constants.SW
                             )

play_menu.add_option('Return to Menu', PYGAME_MENU_CLOSE)
play_menu.add_option('Exit Game', add_event)

# -----------------------------------------------------------------------------
# Help menu
help_menu = pygameMenu.TextMenu(screen,
                                bgfun=main_background,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Help',
                                window_height=constants.SH,
                                window_width=constants.SW
                                )
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in HELP:
    help_menu.add_line(m)

# -----------------------------------------------------------------------------
# About menu
about_menu = pygameMenu.TextMenu(screen,
                                 bgfun=main_background,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 font_size_title=30,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 menu_color_title=COLOR_BLUE,
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,  # Disable menu close (ESC button)
                                 text_fontsize=20,
                                 title='About',
                                 window_height=constants.SH,
                                 window_width=constants.SW
                                 )
about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# -----------------------------------------------------------------------------
# Main menu, pauses execution of the application
menu = pygameMenu.Menu(screen,
                       bgfun=main_background,
                       enabled=False,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_DISABLE_CLOSE,
                       title='Main Menu',
                       title_offsety=5,
                       window_height=constants.SH,
                       window_width=constants.SW
                       )

def wait(fill=True):
    timer = 100
    clock = pygame.time.Clock()
    if fill:
        screen.fill(COLOR_BACKGROUND)
    #pygame.draw.rect(screen, (255, 180, 0), ((constants.SW - 300) / 2, (constants.SH - 200) / 2 - 50, 300,200))
    font = pygame.font.Font("fonts/Lobster_1.3.otf", 100)
    f = font.render('Wait please', 1, COLOR_WHITE)
    screen.blit(f, ((constants.SW - f.get_rect().width) / 2, constants.SH / 2 - 50))
    pygame.display.flip()


    # while True:
    #     screen.fill((100, 100, 100))
    #     clock.tick(60)
    #     if timer > 0:
    #         timer -= 1
    #     else:
    #         return

def func():
    from Start_Game import play
    play_menu.disable()
    menu.reset(1)
    wait()
    play()

menu.add_option(play_menu.get_title(), func)  # Add timer submenu
menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

