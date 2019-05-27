import os
import pygameMenu
from pygameMenu.locals import *
import menus.background_menu as background_menu

import settings
import stats
from spritesheet_functions import *

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
COLOR_BACKGROUND = (75, 172, 198)
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
W_SIZE = 800  # Width of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
font = pygame.font.SysFont("nevis", 100)
music = pygame.mixer.Sound("sounds/The Playground Ensemble, David Farrell - 8-Bit a Rose E'er Blooming.ogg")


def get_stats():
    info = [f"NickName: {stats.statistic.name}",
            # PYGAMEMENU_TEXT_NEWLINE,
            f"Max_score = {stats.statistic.max_score}",
            f"Death = {stats.statistic.count_death}",
            f"Jump = {stats.statistic.count_jump}",
            f"Fires = {stats.statistic.count_fire}"]
    return info





def main_background():
    background_menu.backgl.update()
    background_menu.backgl.draw(screen)

    # screen.fill(COLOR_BACKGROUND)
    if stats.statistic is not None:
        rend = font.render("Hello, " + stats.statistic.name, True, (255, 255, 255))
        screen.blit(rend, rend.get_rect(topleft=(350, 20)))
    # pygame.draw.rect(screen, (255,0,0), (constants.SW/4+20,constants.SH/4-20, constants.SW/2-40, constants.SH/2+40),)


def add_event():
    play_menu.disable()
    # my_event = pygame.event.Event(EVENT_CLOSE)
    # pygame.event.post(my_event)
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
#
def account_menu():
    """
    Help menu
    """
    def func_pass():
        from menus.password_menu import MenuControl2
        app = MenuControl2(screen)
        app.main_loop()

    stats_menu = pygameMenu.Menu(screen,
                                 bgfun=main_background,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 menu_alpha=90,
                                 onclose=PYGAME_MENU_CLOSE,
                                 title='Account menu',
                                 title_offsety=5,
                                 window_height=constants.SH,
                                 window_width=constants.SW,
                                 # menu_height=450
                                 )
    info_menu = pygameMenu.TextMenu(screen,
                                    bgfun=main_background,
                                    font=pygameMenu.fonts.FONT_NEVIS,
                                    text_fontsize=30,
                                    menu_color=(30, 50, 107),  # Background color
                                    menu_color_title=(120, 45, 30),
                                    onclose=PYGAME_MENU_CLOSE,  # Pressing ESC button does nothing
                                    title='Statistics',
                                    window_height=constants.SH,
                                    window_width=constants.SW
                                    )
    info_menu.add_option('Back', PYGAME_MENU_BACK)
    for m in get_stats():
        info_menu.add_line(m)

    def reset_stats():
        stats.statistic.save_empty_data()
        # stats.super_users.delete_one({'name': stats.statistic.name})

    def close_menu():
        my_event = pygame.event.Event(pygame.KEYDOWN)
        my_event.key = pygame.K_ESCAPE
        pygame.event.post(my_event)

    stats_menu.add_option('Statistics', info_menu)
    stats_menu.add_option('Change password', func_pass)
    stats_menu.add_option('Reset stats', reset_stats)
    stats_menu.add_option('Return to Menu', close_menu)

    events = pygame.event.get()
    stats_menu.mainloop(events)


# -----------------------------------------------------------------------------
# About menu
def settings_menu():
    diff = settings.difficulty
    sound = settings.sound

    def change_difficulty(d):
        nonlocal diff
        diff = d
    def change_sound(s):
        nonlocal sound
        sound = s
    def save_settings():
        settings.difficulty = diff
        settings.sound = sound
        print("Saved: diff: %s, sound: %s" % (diff, sound))
        settings.save_settings()

    settings_menu = pygameMenu.Menu(screen,
                                    bgfun=main_background,
                                    enabled=True,
                                    font=pygameMenu.fonts.FONT_NEVIS,
                                    menu_alpha=100,
                                    onclose=PYGAME_MENU_CLOSE,
                                    title='Settings',
                                    window_height=constants.SH,
                                    window_width=constants.SW
                                    )
    settings_menu.add_selector('Difficulty', [('Easy', 'EASY'),
                                              ('Medium', 'MEDIUM'),
                                              ('Hard', 'HARD')],
                               onreturn=None, onchange=change_difficulty, default=settings.get_diff_index())
    settings_menu.add_selector('Sound', [('No', 'NO'),
                                         ('Low', 'LOW'),
                                         ('Medium', 'MEDIUM'),
                                         ('Large', 'HIGH')],
                               onreturn=None, onchange=change_sound, default=settings.get_sound_index())

    def close_menu():
        my_event = pygame.event.Event(pygame.KEYDOWN)
        my_event.key = pygame.K_ESCAPE
        pygame.event.post(my_event)

    settings_menu.add_option('Save', save_settings)
    settings_menu.add_option('Return to Menu', close_menu)

    events = pygame.event.get()
    settings_menu.mainloop(events)
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
                       menu_height=450
                       )


def end_game(player):
    clock = pygame.time.Clock()
    screen.fill(COLOR_BACKGROUND)
    # pygame.draw.rect(screen, (255, 180, 0), ((constants.SW - 300) / 2, (constants.SH - 200) / 2 - 50, 300,200))
    font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)
    f = font.render(f'The End, {player.stats.name}', 1, COLOR_WHITE)
    f2 = font.render(f"score: {player.stats.score}", 1, COLOR_WHITE)
    f3 = font.render(f"max score: {stats.statistic.max_score}", 1, COLOR_WHITE)
    screen.blit(f, ((constants.SW - f.get_rect().width) / 2 - 100, constants.SH / 2 - 200))
    screen.blit(f2, ((constants.SW - f.get_rect().width) / 2 - 100, constants.SH / 2 - 100))
    screen.blit(f3, ((constants.SW - f.get_rect().width) / 2 - 100, constants.SH / 2))

    pygame.display.flip()
    clock.tick(1 / 5)


def wait(fill=True):
    timer = 100
    clock = pygame.time.Clock()
    if fill:
        #screen.fill(COLOR_BACKGROUND)
        background_menu.backgl.draw(screen)
    # pygame.draw.rect(screen, (255, 180, 0), ((constants.SW - 300) / 2, (constants.SH - 200) / 2 - 50, 300,200))
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
    # pygame.draw.rect(screen, (255, 180, 0), ((constants.SW - 300) / 2, (constants.SH - 200) / 2 - 50, 300,200))
    font = pygame.font.Font("fonts/Lobster_1.3.otf", 100)
    f = font.render('You Lose', 1, COLOR_WHITE)
    screen.blit(f, ((constants.SW - f.get_rect().width) / 2, constants.SH / 2 - 50))
    pygame.display.flip()
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(1 / 2)

    # timer = 100
    # clock = pygame.time.Clock()
    # while True:
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
    pygame.key.set_repeat()
    play()
    pygame.mixer.stop()
    music.play()

    # pygame.key.set_repeat(200, 200)


def func_nick():
    from menus.nickname_menu import MenuControl
    app = MenuControl(screen)
    app.main_loop()



menu.add_option(play_menu.get_title(), func)  # Add timer submenu
menu.add_option("Change account", func_nick)  # Add settings submenu
menu.add_option("Settings", settings_menu)  # Add settings submenu
menu.add_option("Account", account_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function
