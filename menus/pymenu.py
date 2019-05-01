import pygame
import pygameMenu, os
from pygameMenu.locals import *
import constants
import stats



# os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{50},{50}"
pygame.init()
size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Platformer")


ABOUT = ['Game: {0}'.format("Platformer v1.0 Beta"),
         'Author: {0}'.format("Andrey"),
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(r"andred9991@gmail.com")]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
def get_stats():
    info = [f"NickName: {stats.statistic.name}",
            #PYGAMEMENU_TEXT_NEWLINE,
            f"Max_score = {stats.statistic.max_score}",
            f"Death = {stats.statistic.count_death}",
            f"Jump = {stats.statistic.count_jump}",
            f"Fires = {stats.statistic.count_fire}"]
    return info


W_SIZE = 800  # Width of window size
font = pygame.font.SysFont("nevis", 100)

def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    screen.fill(COLOR_BACKGROUND)
    if stats.statistic is not None:
        rend = font.render("Hello, " + stats.statistic.name, True, (255, 255, 255))
        screen.blit(rend, rend.get_rect(topleft=(350, 20)))
    #pygame.draw.rect(screen, (255,0,0), (constants.SW/4+20,constants.SH/4-20, constants.SW/2-40, constants.SH/2+40),)

def add_event():
    play_menu.disable()
    #my_event = pygame.event.Event(EVENT_CLOSE)
    #pygame.event.post(my_event)
    pygame.time.set_timer(constants.EVENT_CLOSE, 1)

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
def stats_menu():
    menu = pygameMenu.TextMenu(screen,
                                     bgfun=main_background,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     text_fontsize = 40,
                                     menu_color=(30, 50, 107),  # Background color
                                     menu_color_title=(120, 45, 30),
                                     onclose=PYGAME_MENU_CLOSE,  # Pressing ESC button does nothing
                                     title='Statistics',
                                     window_height=constants.SH,
                                     window_width=constants.SW
                                     )

    for m in get_stats():
        menu.add_line(m)
    events = pygame.event.get()
    menu.mainloop(events)

# -----------------------------------------------------------------------------
# About menu
settings_menu = pygameMenu.Menu(screen,
                                bgfun=main_background,
                                enabled=False,
                                font=pygameMenu.fonts.FONT_NEVIS,
                                menu_alpha=100,
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                title='Settings',
                                window_height=constants.SH,
                                window_width=constants.SW
                                )
settings_menu.add_selector('Difficulty', [('Easy', 'EASY'),
                                          ('Medium', 'MEDIUM'),
                                          ('Hard', 'HARD')],
                           onreturn=None, onchange=None)
settings_menu.add_selector('Sound', [('Easy', 'EASY'),
                                     ('Medium', 'MEDIUM'),
                                     ('Hard', 'HARD')],
                           onreturn=None, onchange=None)
settings_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
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
                       window_width=constants.SW,
                       menu_height = 450
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

def lose(fill=True):
    if fill:
        screen.fill(COLOR_BACKGROUND)
    #pygame.draw.rect(screen, (255, 180, 0), ((constants.SW - 300) / 2, (constants.SH - 200) / 2 - 50, 300,200))
    font = pygame.font.Font("fonts/Lobster_1.3.otf", 100)
    f = font.render('You Lose', 1, COLOR_WHITE)
    screen.blit(f, ((constants.SW - f.get_rect().width) / 2, constants.SH / 2 - 50))
    pygame.display.flip()


    timer = 100
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if timer > 0:
            timer -= 1
        else:
            return


def func():
    from Start_Game import play
    play_menu.disable()
    menu.reset(1)
    wait()
    pygame.key.set_repeat()
    play()
    #pygame.key.set_repeat(200, 200)

def func_nick():
    from menus.nickname_menu import MenuControl
    app = MenuControl(screen)
    app.main_loop()

menu.add_option(play_menu.get_title(), func)  # Add timer submenu
menu.add_option("Change account", func_nick)  # Add settings submenu
menu.add_option(settings_menu.get_title(), settings_menu)  # Add settings submenu
menu.add_option("Stats menu", stats_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function



