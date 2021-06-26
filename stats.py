import pygame
import constants
from spritesheet_functions import SpriteSheet
import blocks

from pymongo import MongoClient

import socket
def is_connected(hostname="www.google.com"):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

print(is_connected())
assert is_connected(), 'No internet'


client = MongoClient('mongodb+srv://ezreal:Qwe123@firstcluster.xduia.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.get_database('platformer')
users = db.users
super_users = db.super_users
statistic = None

class Stats:
    screen = None
    player = None
    name = None
    password = None
    count_jump = 0
    count_death = 0
    count_fire = 0
    score = 0
    max_score = 0
    level = None

    def __init__(self, screen, nickname, password):
        self.screen = screen
        # self.player = player
        self.name = nickname
        self.password = password
        self.count_jump = 0
        self.count_death = 0

    def up_jump(self):
        self.count_jump += 1

    def up_death(self):
        self.count_death += 1

    def up_score(self, cost):
        self.score += cost
        if self.score > self.max_score:
            self.max_score = self.score

    def get_dict(self) -> dict:
        stats ={'count_death': self.count_death,
                'count_fire': self.count_fire,
                'count_jump': self.count_jump,
                'max_score': self.max_score}
        return stats

    def get_empty_dict(self):
        stats = {'count_death': 0,
                'count_fire': 0,
                'count_jump': 0,
                'max_score': 0}
        return stats

    def save_data(self, empty=False):
        stats = (self.get_empty_dict() if empty else self.get_dict())
        myquery = {"name": self.name}
        newvalues = {"$set": {"stats": stats}}
        users.update_one(myquery, newvalues)

    def save_new_password(self, password):
        myquery = {"name": self.name}
        newvalues = {"$set": {"password": password}}
        users.update_one(myquery, newvalues)

    def save_empty_data(self):
        self.save_data(True)
        self.max_score = 0
        self.count_death = self.count_fire = self.count_jump = 0


class Hud:
    screen = None
    player = None
    stats = None
    count_health_rend = 0

    def __init__(self, screen, player, stats):
        self.screen = screen
        self.player = player
        self.stats = stats
        self.font_menu = pygame.font.Font("fonts/Lobster_1.3.otf", 50)

        sprite_sheet = SpriteSheet("images/pack/Base pack/HUD/hud_spritesheet.png")
        self.image_heal1 = sprite_sheet.get_image(blocks.HEAL_FULL[0], blocks.HEAL_FULL[1], blocks.HEAL_FULL[2], blocks.HEAL_FULL[3])
        self.image_heal2 = sprite_sheet.get_image(blocks.HEAL_HALF[0], blocks.HEAL_HALF[1], blocks.HEAL_HALF[2], blocks.HEAL_HALF[3])
        self.image_heal3 = sprite_sheet.get_image(blocks.HEAL_EMPTY[0], blocks.HEAL_EMPTY[1], blocks.HEAL_EMPTY[2], blocks.HEAL_EMPTY[3])

        self.image_health = pygame.Surface([54*(self.player.max_health)//2, 45]).convert()
        self.image_health.set_colorkey(constants.BLACK)
        #self.image_health = self.image_health.convert_alpha()
        self.rend_health()

    def rend_health(self):
        if self.player.health < 0:
            return None
        i = 0
        self.image_health.fill(constants.BLACK)
        for _ in range(self.player.health//2):
            self.image_health.blit(self.image_heal1, (54*i, 0))
            i += 1
        if self.player.health % 2 == 1:
            self.image_health.blit(self.image_heal2, (54*i, 0))
            i+=1
        # for _ in range((self.player.max_health - i)//2):
        #     self.image_health.blit(self.image_heal3, (54*i, 0))
        #     i+=1

    def draw(self):
        if self.count_health_rend != self.player.health:
            self.count_health_rend = self.player.health
            self.rend_health()
        self.screen.blit(self.font_menu.render(str(self.stats.score), 1, (255,200,100)), (50, 50))
        self.screen.blit(self.image_health, (300, 50))
