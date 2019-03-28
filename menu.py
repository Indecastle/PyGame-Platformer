import pygame, sys

done = False

clock = pygame.time.Clock()

class Menu:
    def __init__(self):
        self.punkts = None

    def render(self, screen, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))


class Menu01(Menu):
    def __init__(self):
        self.punkts = [(120, 140, u'Game', (250, 250, 30), (250, 30, 250), 0),
                       (130, 210, u'Quit', (250, 250, 30), (250, 30, 250), 1)]

    def menu(self, screen):
        done = True
        font_menu = pygame.font.Font("fonts/Lobster_1.3.otf", 30)
        punkt = 0

        while done:
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < mp[0] < i[0]+155 and i[1] < mp[1] < i[1]+50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN or e.key == pygame.K_RETURN:
                    if punkt == 0:
                        done = False
                    if punkt == 1:
                        sys.exit()

            clock.tick(60)
            pygame.display.flip()
