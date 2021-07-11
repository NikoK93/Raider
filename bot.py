import time
import numpy as np
import datetime as dt

from clan_boss import ClanBoss
from clan_boss import unm_custom, nightmare_custom
from dungeon_master import Dungeon
from support_functions import open_raid, isNowInTimePeriod
from arena import Arena
from routines import Routine

class Raider():

    def __init__(self, action=None):

        # Get center and open raid
        self.CENTER_POSITION = open_raid()

        # Some default actions
        self.actions = ['arena', 'tag_arena','spider', 'mini_routine']
        #self.probabilities = [0.5, 0.5]

        self.user_action = action

        temperature = dict.fromkeys(self.actions, 1)

        self.IDLE = 1
        self.market_refresh = None
    
    def get_status():
        pass
        # get current energy and arena coins status

    def action_refresh(self):

        now = dt.datetime.now()
        #last_hour_date_time = dt.now() - dt(hours = 1)
        if self.market_refresh is not None:
            if (now - self.market_refresh).total_seconds() > 3600:
                if "routine_market_refresh" not in self.actions:
                    self.actions.append('routine_market_refresh')

    def main_loop(self):

        self.action_refresh()

        if isNowInTimePeriod(dt.time(11,00), dt.time(11,30), dt.datetime.now().time()):
            if 'routine' not in self.actions:
                self.actions.insert(1,'routine')

        if isNowInTimePeriod(dt.time(12,30), dt.time(14,30), dt.datetime.now().time()) and self.user_action == 'CB':
            action = 'UNM'

        elif isNowInTimePeriod(dt.time(19,30), dt.time(21,30), dt.datetime.now().time()) and self.user_action == 'CB':
            action = 'NM'
        elif self.user_action != None:
            action = self.user_action
        else:
            action = self.actions[0]
            self.actions = self.actions[1:]
            if action != "routine":
                self.actions.append(action)
                print(self.actions)

        print(f"Executing {action}...")

        if self.IDLE == 1:
            if action == 'NM':
                self.IDLE = 0

                clan_boss = ClanBoss('NM')
                clan_boss.to_clan_boss()
                time.sleep(900)
                self.IDLE = 1

            elif action == 'UNM':
                self.IDLE = 0

                clan_boss = ClanBoss('UNM')
                clan_boss.to_clan_boss()

                time.sleep(900)
                self.IDLE = 1

            elif action == 'spider':
                #set idle 
                self.IDLE = 0

                d = Dungeon('spider', 100, refill=True)
                d.to_spider()

                time.sleep(1)

                print('Bot: IDLE')
                self.IDLE = 1
                    
            elif action == 'arena':

                #set idle 
                self.IDLE = 0

                arena = Arena('classic')
                arena.go_to_arena()

                time.sleep(1)
 
                print('Bot: IDLE')
                self.IDLE = 1
                 

            elif action == 'tag_arena':

                #set idle 
                self.IDLE = 0

                arena = Arena('tag')
                arena.go_to_arena()

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1
                    
                    
            elif action == 'routine':

                self.IDLE = 0
                routine = Routine()
                routine.routine()

                self.market_refresh = routine.market_CD
                print(self.market_refresh)

                self.IDLE = 1

            elif action == 'routine_market_refresh':

                self.IDLE = 0
                routine = Routine()
                routine.market_refresh()

                self.market_refresh = routine.market_CD
                print(self.market_refresh)
                    
            elif action == 'mini_routine':

                self.IDLE = 0
                routine = Routine()
                routine.mini_routine()

                self.IDLE = 1

            elif action == 'FW':

                self.IDLE = 0
                fw = Dungeon('FW', 100, refill=True)
                fw.faction_wars()

                self.IDLE = 1
               

raid = Raider('CB')

while True:
    
    raid.main_loop()
    time.sleep(30)
    print("trying action...")

