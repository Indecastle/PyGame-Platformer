import sys, os, pprint
import pygame as pg
import constants
from boxes import TextBox, ButtonBox
from menus.pymenu import screen
import stats
KEY_REPEAT_SETTING = (200,70)

class Menu_statsControl(object):
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.current = 0
        button_close = ButtonBox((10, 250, 100, 30), 'Back', command=self.back, id=4)
        self.prompts = self.make_prompts()
        self.boxes = [button_close]
        self.color = (100,100,100)

    def make_prompts(self, color="white"):
        color = pg.Color(color)
        rendered = []
        font = pg.font.SysFont("arial", 22)
        message = 'Nickname: ' + stats.statistic.name
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topleft=(10,100))))
        message = 'Max_score: ' + stats.statistic.max_score
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topleft=(10,150))))
        message = 'Max_death: ' + stats.statistic.max_death
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topleft=(10, 150))))
        message = 'Max_: ' + stats.statistic.max_score
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topleft=(10, 150))))
        return rendered

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self.boxes[self.current].active = False
                    self.current = (self.current + 1) % len(self.boxes)
                    self.boxes[self.current].active = True
                    continue
            if event.type == pg.QUIT:
                self.done = True
                pg.quit()
                sys.exit()
            for box in self.boxes[::-1]:
                sms = box.get_event(event)
                if sms == 'curr':
                    self.current = box.id
                elif sms == 'next':
                    self.boxes[self.current].active = False
                    self.current = (box.id + 1) % len(self.boxes)
                    self.boxes[self.current].active = True
            if all(not box.active for box in self.boxes):
                self.current = 4

    def render(self):
        self.screen.fill(self.color)
        for box in self.boxes:
            box.draw(self.screen)
        for prompt in self.prompts:
            self.screen.blit(*prompt)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            for box in self.boxes:
                box.update()
            self.render()
            pg.display.update()
            self.clock.tick(self.fps)

    def back(self):
        if stats.statistic is not None:
            self.done = True




if __name__ == "__main__":
    app = MenuControl(screen)
    app.main_loop()
    pg.quit()
    sys.exit()
