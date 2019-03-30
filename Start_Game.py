import pygame, time

import constants
import levels
import menu

from player import Player



def main():
    """ Main Program """
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("My Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    levels.level_list = []
    levels.level_list.append(levels.Level_01(player))
    levels.level_list.append(levels.Level_02(player))

    # Set the current level
    levels.current_level_no = 0
    levels.current_level = levels.level_list[levels.current_level_no]

    player.level = levels.current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 50

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    done = False
    MainMenu = menu.Menu01()
    MainMenu.menu(screen)

    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()
        levels.current_level.update()

        """
        current_position = player.rect.x + current_level.world_shift_x
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
        """

        levels.current_level.draw(screen)
        active_sprite_list.draw(screen)


        clock.tick(60)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
