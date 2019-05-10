import sys, os, pprint
import pygame as pg
import constants
from boxes import TextBox, ButtonBox
import stats, menus.menu
from menus.background_menu import backgl
KEY_REPEAT_SETTING = (200,70)

class MenuControl2(object):
    def __init__(self, screena):
        self.screen = screena
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.current = 0
        textbox1 = TextBox((200,100,300,40), id = 0, command=None, active=True, password=True)
        textbox2 = TextBox((200,150,300,40), id = 1, command=None, password=True)

        button_login = ButtonBox((200,200,100,30), 'Change', command=self.event_login, id = 2)
        button_close = ButtonBox((200, 250, 80, 30), ' Back', command=self.back, id=3)
        self.prompts = self.make_prompts()
        self.boxes = [textbox1, textbox2, button_login, button_close]
        self.color = (100,100,100)


    def make_prompts(self, color="white"):
        color = pg.Color(color)
        color = (100,100,100)
        rendered = []
        font = pg.font.SysFont("arial", 33)

        message = 'Change password menu'
        rend = font.render(message, True, (0,0,0))
        rendered.append((rend, rend.get_rect(topright=(400, 30))))

        message = 'old password:'
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topright=(190,105))))
        message = 'new password:'
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topright=(190,155))))
        return rendered

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB or event.key == pg.K_DOWN or event.key == pg.K_RIGHT:
                    self.boxes[self.current].active = False
                    self.current = (self.current + 1) % len(self.boxes)
                    self.boxes[self.current].active = True
                    continue
                if event.key == pg.K_UP  or event.key == pg.K_LEFT:
                    self.boxes[self.current].active = False
                    self.current = (self.current - 1) % len(self.boxes)
                    self.boxes[self.current].active = True
                    continue
                elif event.key == pg.K_ESCAPE:
                    if stats.statistic is not None:
                        self.done = True
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
                self.current = len(self.boxes)-1

    def render(self):
        #self.screen.fill(self.color)
        backgl.update()
        backgl.draw(self.screen)
        for box in self.boxes:
            box.draw(self.screen)
        for prompt in self.prompts:
            self.screen.blit(*prompt)

    def main_loop(self):
        pg.key.set_repeat(*KEY_REPEAT_SETTING)
        while not self.done:
            self.event_loop()
            for box in self.boxes:
                box.update()
            self.render()
            pg.display.update()
            self.clock.tick(self.fps)
        pg.key.set_repeat()

    def event_login(self):
        old_pass = self.boxes[0].final.strip()
        new_pass = self.boxes[1].final.strip()
        self.boxes[1].buffer = []
        self.boxes[0].buffer = []
        print(f'old_pass: {old_pass}, new_pass: {new_pass}')

        if old_pass == new_pass:
            self.message("new pass = old pass")
        elif stats.statistic.password == old_pass:
            stats.statistic.save_new_password(new_pass)
            self.message("OK")
            self.back()
        else:
            self.message("invalid password")

    def message(self, text):
        font = pg.font.SysFont("arial", 40)
        rend = font.render(text, True, (255,255,255))
        if len(self.prompts) == 3:
            self.prompts.append((rend, rend.get_rect(topleft=(10, 300))))
        else:
            self.prompts[3] = (rend, rend.get_rect(topleft=(10, 300)))

    def back(self):
        if stats.statistic is not None:
            self.done = True
        else:
            pg.event.post(pg.event.Event(pg.QUIT))




# if __name__ == "__main__":
#     app = MenuControl(screen)
#     app.main_loop()
#     pg.quit()
#     sys.exit()
