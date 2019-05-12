import pygame, time, os

import constants, settings
import super_level
from levels import *
from menus.menu import Console, Menu01
from player import Player
import stats
from menus.pymenu import play_menu, menu, screen, wait, lose, func_nick, end_game
import menus.background_menu as background_menu




def main():
    background_menu.backgl = background_menu.Background_live()
    func_nick()

    # Create all the levels
    super_level.level_list = []
    super_level.level_list.append(Level_04)
    super_level.level_list.append(Level_03)
    super_level.level_list.append(Level_02)
    super_level.level_list.append(Level_01)
    player = Player()
    player.stats = stats.statistic

    menu.enable()
    events = pygame.event.get()
    menu.mainloop(events)
    pygame.quit()


def play():
    # Create the player
    player = Player()
    player.init2()

    # Set the current level
    super_level.current_level_no = 0
    super_level.current_level = super_level.level_list[super_level.current_level_no](player)

    player.level = super_level.current_level
    player.rect.topleft = super_level.current_level.start_pos

    # MainMenu = Menu01()
    # MainMenu.menu(screen)
    console = Console(screen, player)

    statistic = stats.statistic
    HUD = stats.Hud(screen, player, statistic)
    statistic.score = 0

    clock = pygame.time.Clock()
    done = False
    # -------- Main Program Loop -----------
    while not done:
        events = pygame.event.get()
        for event in events:
            player_event = False
            if event.type == pygame.QUIT:
                done = True # Flag that we are done so we exit this loop
            if event.type == constants.EVENT_LOSE:
                pygame.time.set_timer(constants.EVENT_LOSE, 0)
                statistic.save_data()
                lose()
                return
            if event.type == constants.EVENT_CLOSE:
                pygame.time.set_timer(constants.EVENT_CLOSE, 0)
                statistic.save_data()
                return
            if event.type == constants.EVENT_END:
                pygame.time.set_timer(constants.EVENT_END, 0)
                statistic.save_data()
                end_game(player)
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKQUOTE:
                    console.enable()
                if play_menu.is_disabled() and not console.is_enabled:
                    player_event = True
                if event.key == pygame.K_ESCAPE:
                    #MainMenu.menu(screen)
                    play_menu.enable()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player_event = True

            if event.type == pygame.KEYUP:
                player_event = True

            if player_event:
                player.get_event(event)



        #active_sprite_list.update()
        super_level.current_level.update()
#gwt
        super_level.current_level.draw(screen)
        HUD.draw()

        play_menu.mainloop(events)
        console.update(events)
        console.draw()

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
