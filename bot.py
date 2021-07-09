import time
import numpy as np
import datetime as dt

from main import to_clan_boss
from clan_boss import unm_custom, nightmare_custom
from dungeon_master import Dungeon
from support_functions import open_raid, isNowInTimePeriod
from arena import Arena


class Raider():

    def __init__(self, action=None):

        self.CENTER_POSITION = open_raid()
        self.actions = ['arena', 'spider', 'tag_arena']
        #self.probabilities = [0.5, 0.5]

        self.user_action = action

        temperature = dict.fromkeys(self.actions, 1)

        self.IDLE = 1
    
    def get_status():
        pass
        # get current energy and arena coins status

    def action_refresh():
        pass

    def main_loop(self):

        #actions = ['UNM', 'NM', 'spider']

        if self.user_action != None:
            action = self.user_action
        elif isNowInTimePeriod(dt.time(12,30), dt.time(14,30), dt.datetime.now().time()):
            action = 'UNM'
        else:
            action = np.random.choice(self.actions)

        print(f"Executing {action}...")

        if self.IDLE == 1:
            if action == 'NM':
                to_clan_boss('NM')
            elif action == 'UNM':
                to_clan_boss('UNM', repeat=2)
            elif action == 'spider':
                #set idle 
                self.IDLE = 0

                d = Dungeon('spider', 100, refill=True)
                d.to_spider()

                time.sleep(1)
                if d.STATE == 1:
                    self.IDLE = 1
            elif action == 'arena':

                #set idle 
                self.IDLE = 0

                arena = Arena('classic')
                arena.go_to_arena()

                time.sleep(1)
                if arena.STATE == 0:
                    self.IDLE = 1

            elif action == 'tag_arena':

                #set idle 
                self.IDLE = 0

                arena = Arena('tag')
                arena.go_to_arena()

                time.sleep(10)
                if arena.STATE == 0:
                    self.IDLE = 1 
b = Raider('spider')

while True:
    
    b.main_loop()
    time.sleep(30)
    print("trying action...")

