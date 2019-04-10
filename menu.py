import pygame, sys
import constants
from colorsys import hsv_to_rgb

done = False

clock = pygame.time.Clock()
h = 0
class Menu:
    punkts = 0
    cycle = 0

    def render(self, screen, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))


class Menu01(Menu):
    def __init__(self):
        x = constants.SCREEN_WIDTH/2-100
        self.punkts = [(x+10, 140, u'Game', (250, 250, 30), (30, 250, 250), 0),
                       (x, 240, u'Settings', (250, 250, 30), (30, 250, 250), 1),
                       (x+10, 340, u'Quit', (250, 250, 30), (30, 250, 250), 2)]

    def menu(self, screen):
        global h
        self.cycle = True
        font_menu = pygame.font.Font("fonts/Lobster_1.3.otf", 100)
        punkt = 0
        canClick = False

        while self.cycle:
            rgb = hsv_to_rgb(h, 1, 1)
            screen.fill((rgb[0]*255, rgb[1]*255, rgb[2]*255))
            h = (h + 0.001) % 1.0

            canClick = False
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < mp[0] < i[0]+300 and i[1] < mp[1] < i[1]+100:
                    punkt = i[5]
                    canClick = True
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    #if e.key == pygame.K_ESCAPE:
                    #    sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if canClick:
                        self.event(punkt)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.event(punkt)
                    
            clock.tick(60)
            pygame.display.flip()
            
    def event(self, punkt):
        if punkt == 0:
            self.cycle = False
        if punkt == 2:
            sys.exit()
            

            
            