import pygame, time, os

import constants
import super_level
from levels import *
import menu
from player import Player
import hud
from pymenu import play_menu, menu, screen





def main():
    menu.enable()
    events = pygame.event.get()
    menu.mainloop(events)
    pygame.quit()


def play():
    """ Main Program """

    # Create the player
    player = Player()

    # Create all the levels
    super_level.level_list = []
    super_level.level_list.append(Level_03)
    super_level.level_list.append(Level_02)
    super_level.level_list.append(Level_01)

    # Set the current level
    super_level.current_level_no = 0
    super_level.current_level = super_level.level_list[super_level.current_level_no](player)

    player.level = super_level.current_level

    player.rect.x = super_level.current_level.start_pos[0]
    player.rect.y = super_level.current_level.start_pos[1]

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    #MainMenu = menu.Menu01()
    #MainMenu.menu(screen)

    stats = hud.Stats(screen, player, "Markiz")
    player.stats = stats
    HUD = hud.Hud(screen, player, stats)
    stats.HUD = HUD

    clock = pygame.time.Clock()

    done = False
    # -------- Main Program Loop -----------
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: 
                done = True # Flag that we are done so we exit this loop
            if event.type == constants.EVENT_CLOSE:
                pygame.time.set_timer(constants.EVENT_CLOSE, 0)
                return

            if event.type == pygame.KEYDOWN:
                if play_menu.is_disabled():
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_UP:
                        player.jump()
                        player.minus_heal()
                if event.key == pygame.K_ESCAPE:
                    #MainMenu.menu(screen)
                    play_menu.enable()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

        active_sprite_list.update()
        super_level.current_level.update()
#gwt
        super_level.current_level.draw(screen)
        active_sprite_list.draw(screen)
        super_level.current_level.draw_adv(screen)
        HUD.draw()

        play_menu.mainloop(events)

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
