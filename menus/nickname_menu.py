import sys, os, pprint
import pygame as pg
import constants
from boxes import TextBox, ButtonBox
import stats, menus.menu
from menus.background_menu import backgl
KEY_REPEAT_SETTING = (200,70)

from sklearn.externals import joblib
clf = joblib.load('menus/injection_model.pkl')

class MenuControl(object):
    def __init__(self, screena):
        self.screen = screena
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.current = 0
        screen_color = TextBox((500,250,300,40), id = 0, command=self.check_email, active=True)
        text_color = TextBox((500,300,300,40), id = 1, command=None, password=True)

        button_login = ButtonBox((500,350,80,30), ' Login', command=self.event_login, id = 2)
        button_register = ButtonBox((600, 350, 100, 30), 'Register', command=self.event_register, id = 3)
        button_close = ButtonBox((500, 400, 80, 30), ' Back', command=self.back, id=4)
        self.prompts = self.make_prompts()
        self.boxes = [screen_color, text_color, button_login, button_register, button_close]
        self.color = (100,100,100)

    def check_email(self, id, text):
        input_data = [text]
        ints = clf.predict(input_data).astype(int)
        if ints[0] == 1:
            self.message("its Email")
        else:
            self.message("its not Email")


    def make_prompts(self, color="white"):
        color = pg.Color(color)
        color = (100,100,100)
        rendered = []
        font = pg.font.SysFont("arial", 33)

        message = 'Account menu'
        rend = font.render(message, True, (0, 0, 0))
        rendered.append((rend, rend.get_rect(topright=(700, 180))))

        message = 'Nickname:'
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topright=(490,255))))

        message = 'Password:'
        rend = font.render(message, True, color)
        rendered.append((rend, rend.get_rect(topright=(490,305))))
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
        name = self.boxes[0].final.strip()
        password = self.boxes[1].final.strip()
        self.boxes[1].buffer = []
        print(f'name : {name}, password : {password}')

        info = stats.users.find_one({'name':name, 'password':password})
        if info is not None:
            stats.statistic = stats.Stats(self.screen, name, password)
            stats.statistic.max_score = int(info['stats']['max_score'])
            stats.statistic.count_death = int(info['stats']['count_death'])
            stats.statistic.count_jump = int(info['stats']['count_jump'])
            stats.statistic.count_fire = int(info['stats']['count_fire'])
            self.message("OK")
            pprint.pprint(info)
            self.back()
            check = stats.super_users.find_one({'name': name})
            pprint.pprint(check)
            menus.menu.sv_cheats = (False if check is None else True)
        else:
            self.message("invalid")
пше 
    def event_register(self):
        name = self.boxes[0].final.strip()
        password = hash(self.boxes[1].final.strip())
        print(f'name : {name}, password : {password}')

        info = stats.users.find_one({'name': name})

        if password == '' and name == '':
            self.message("Invalid nickname and password.")
        elif password == '':
            self.message("Invalid password.")
        elif name == '':
            self.message("Invalid nickname.")
        elif info is not None:
            self.message("This name is exist.")
        elif info is not None and password == '':
            self.message("Invalid password. This name is exist.")
        else:
            info = { 'name': name,
                     'password': password,
                     'stats': {'count_death': 0,
                               'count_fire': 0,
                               'count_jump': 0,
                               'max_score': 0}}
            stats.users.insert_one(info)
            stats.statistic = stats.Stats(self.screen, name, password)
            stats.statistic.max_score = int(info['stats']['max_score'])
            stats.statistic.count_death = int(info['stats']['count_death'])
            stats.statistic.count_jump = int(info['stats']['count_jump'])
            stats.statistic.count_fire = int(info['stats']['count_fire'])
            self.message("OK")
            pprint.pprint(info)
            self.back()

    def message(self, text):
        font = pg.font.SysFont("arial", 40)
        rend = font.render(text, True, (255,255,255))
        if len(self.prompts) == 2:
            self.prompts.append((rend, rend.get_rect(topleft=(310, 450))))
        else:
            self.prompts[2] = (rend, rend.get_rect(topleft=(310, 450)))

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
