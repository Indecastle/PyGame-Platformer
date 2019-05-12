import pygame, sys
import constants
from colorsys import hsv_to_rgb
import re

done = False
sv_cheats = False

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



class Console:
    screen = None
    player = None
    width = 100
    height = 100
    pos = (3, 3)
    enabled = False
    font = pygame.font.match_font("Arial")
    maxLength = 17
    case = 0
    timer = 200
    admin_commands = ['god', 'jump', 'speed', 'speed', 'fun', 'gravity', 'impulse']
    commands = ['egg', 'name']


    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.text = ""
        self.text2 = ""
        self.is_enabled = False
        fontFace = pygame.font.match_font("Consolas")
        self.font = pygame.font.Font(fontFace, 30)
        self.font2 = pygame.font.Font(fontFace, 30)
        self.image = self.font.render(self.text, True, constants.WHITE)
        self.image2 = self.font.render(self.text2, True, constants.WHITE)
        self.is_show_text = False
        self._timer = self.timer
        self.egg = False

    def update(self, events):
        if not self.is_enabled:
            return None
        for event in events:
            if event.type == pygame.KEYDOWN:
                keyevent = event

                key = keyevent.key
                unicode = keyevent.unicode
                if key == pygame.K_BACKQUOTE:
                    continue
                if key == pygame.K_DELETE:
                    self.text = ""
                elif 31 < key < 127 and (
                        self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
                    if keyevent.mod in (1, 2) and self.case == 1 and 97 <= key <= 122:
                        # force lowercase letters
                        self.text += chr(key)
                    elif keyevent.mod == 0 and self.case == 2 and 97 <= key <= 122:
                        self.text += chr(key - 32)
                    else:
                        # use the unicode char
                        self.text += unicode
                elif key == 8:
                    # backspace. repeat until clear
                    self.text = self.text[0:len(self.text) - 1]
                elif key == 13:
                    # Enter.
                    self.cheat_event()
                    self.text = ""
                    self.is_enabled = False
        self.image = self.font.render(self.text, True, constants.WHITE)

    def enable(self):
        self.is_enabled = not self.is_enabled
        self.is_show_text = False
            
    def draw(self):
        if self.is_enabled:
            width = self.image.get_rect().width
            pygame.draw.rect(self.screen, (200,200,200), (0,0, 300, 33))
            pygame.draw.rect(self.screen, constants.WHITE, (0, 0, 300, 33), 2)
            self.screen.blit(self.image, self.pos)
        if self.is_show_text:
            self.show_text()

    def cheat_event(self):
        text = re.sub(r' {2,}', ' ', self.text).rstrip().split(' ')
        command = text[0]
        args = text[1:] + ['']
        self.text2 = "None"
        try:
            if sv_cheats:
                if command == 'god':
                    self.player.cheat_god = not self.player.cheat_god
                    self.text2 = 'God On' if self.player.cheat_god else 'God Off'
                elif command == 'jump':
                    speed = int(args[0])
                    self.player.speed_jump = -speed
                    self.text2 = f'jump = {speed}'
                elif command == 'speed':
                    speed = int(args[0])
                    self.player.speed_X = speed
                    self.text2 = f'speed = {speed}'
                elif command == 'gravity':
                    value = float(args[0])
                    self.player.level.gravity = .35 * value / 800
                    self.text2 = f'gravity = {value}'
                elif command == 'impulse':
                    if args[0] == '101':
                        self.player.health = self.player.max_health
                        self.text2 = 'Succesfull'
                elif command == 'fun':
                    value = float(args[0])
                    self.player.cheat_fun = True if value > 0 else False
                    self.text2 = f'Fun = {"on" if value > 0 else "off"}'
            elif command in self.admin_commands:
                self.text2 = 'No access'

            if command == 'egg':
                if self.player.health == 1 and 100 <= self.player.stats.score <= 1100:
                    self.text2 = 'you can use command "mario [\'\',1, 2] [small]"'
                    self.egg = True
            elif command == 'mario' and self.egg:
                if args[0] == '' or args[0] == '1' or args[0] == 'small':
                    if args[0] == 'small' or args[0] == '1' and args[1] == 'small':
                        self.player.init_image(2, True)
                    elif args[0] == '1' or args[0] == '':
                        self.player.init_image(1, True)
                elif args[0] == '2':
                    if args[1] == '':
                        self.player.init_image(3, True)
                    elif args[1] == 'small':
                        self.player.init_image(4, True)
        except (ValueError, IndexError):
            self.text2 = 'Error 404'
        self.image2 = self.font2.render(self.text2, True, constants.WHITE)
        self.is_show_text = True
        self._timer = self.timer

    def show_text(self):
        self.screen.blit(self.image2, (0, 0))
        if self._timer > 0:
            self._timer -= 1
        else:
            self.is_show_text = False



