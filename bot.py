import time
import numpy as np
import datetime as dt

from leveling import AutoLeveler
from clan_boss import ClanBoss
from clan_boss import unm_custom, nightmare_custom
from dungeon_master import Dungeon
from support_functions import open_raid, isNowInTimePeriod
from arena import Arena
from routines import Routine
import database


'''
Game settings -
Graphics Quality: Low
Frame Rate Limit: 60 FPS
Resolution 1280x720

GAME_RESOLUTION = (1280, 720)

'''

class Raider():

    def __init__(self, account, dungeon=None, leveling=False, gem_refill=False, action=None, action_one_time=False, star_leveling=2,  dt_difficulty='normal'):

        # Get center and open raid
        self.CENTER_POSITION = open_raid()

        # Some default actions
        self.actions = ['arena', 'tag_arena', 'FW', 'doom_tower','mini_routine']
        # Action which will not be appended and reapeated
        self.daily_action = ['UNM', 'NM', 'routine', 'routine_market_refresh']

        # Avaliable dungeons
        self.dungeons = ['force', 'spirit', 'magic', 'void', 'arcane', 'dragon', 'spider', 'ice_golem', 'fire_knight', 'minotaur'] 
        self.dungeons_subset = ['dragon', 'spider', 'ice_golem', 'fire_knight'] 

        # User defined single action
        self.user_action = action

        # account information 
        self.account = account
        
        # Gem refill bool
        self.gem_refill = gem_refill

        # DoomTower difficulty
        self.dt_difficulty = dt_difficulty

        # Minimum star for leveling
        self.star_leveling = star_leveling

        # Leveling bool
        self.leveling = leveling

        # Choosing energy spender, and inserting it into actions stack at index 0
        if self.leveling:
            self.actions.insert(0,'leveling')
        else:
            # if dungeon is defined, append to list. Else insert a random dungeon
            if dungeon:
                #self.actions.insert(0, dungeon)
                self.actions.append(dungeon)
            else:
                self.actions.insert(0, np.random.choice(self.dungeons_subset))
            
        # Bot status
        self.IDLE = 1

        # Market refresh status
        self.market_refresh = None

        # Once per day activites 
        self.cb_UMM = 0
        self.cb_MM = 0
        self.routine = 0

        # Saved leveling runs left 
        self.leveling_runs = 0

        # Load in the database
        self.database = database.DataBaseManager(account=self.account)

        # If no new dateime stamp exists from today, initialie it with fresh values
        if self.database.select_data() == None:
            self.database.initialize()
        # Get data about states
        self.get_status()

    def get_status(self):
        
        self.cb_UMM = self.database.get_posts(difficulty='UNM')
        self.cb_MM =self.database.get_posts(difficulty='NM')
        self.routine = self.database.get_posts(difficulty='routine')
        self.leveling_runs = self.database.get_levling_value()

        print(f" NM status: {self.cb_MM}, UNM status: {self.cb_UMM}, Routine status: {self.routine}")

    def action_refresh(self):

        now = dt.datetime.now()
        #last_hour_date_time = dt.now() - dt(hours = 1)
        if self.market_refresh is not None:
            if (now - self.market_refresh).total_seconds() > 3600:
                if "routine_market_refresh" not in self.actions:
                    # Insert market refresh as first priority
                    self.actions.insert(0,'routine_market_refresh')

        self.get_status()

    def main_loop(self):

        # Call action refresh 
        self.action_refresh()

        if isNowInTimePeriod(dt.time(7,00), dt.time(18,00), dt.datetime.now().time()) and self.routine == 0:
            if 'routine' not in self.actions:
                self.actions.insert(0,'routine')
                self.database.update_value('routine')

        if isNowInTimePeriod(dt.time(12,10), dt.time(14, 00), dt.datetime.now().time()) and self.cb_UMM == 0:
            # Insert UNM as priority 1
            if 'UNM' not in self.actions:
                self.actions.insert(0,'UNM')
                # Write to database
                self.database.update_value('UNM')
            
        elif isNowInTimePeriod(dt.time(19,30), dt.time(23,30), dt.datetime.now().time()) and self.cb_MM == 0:
             # Insert NM as priority 1
            if 'NM' not in self.actions:
                self.actions.insert(0,'NM')
                # Write to database
                self.database.update_value('NM')

        elif self.user_action != None:
            #action = self.user_action
            self.actions.insert(0, self.user_action)

        # Select action from index 0
        action = self.actions[0]
        # Slice actions to remove the first element from priority queue
        self.actions = self.actions[1:]
        # Moving selected action to the bottom of the priority queue
        # Do not append actions which occour only once per day
        if action not in self.daily_action:
            self.actions.append(action)
        
        print(self.actions)

        print(f"Executing {action}...")
        
        # Make sure the bot is idle
        if self.IDLE == 1:
            if action == 'leveling':

                self.IDLE = 0

                Leveler = AutoLeveler(refill=self.gem_refill,minimum_star=self.star_leveling, runs_left=self.leveling_runs)
                Leveler.to_leveling()

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action in self.dungeons:

                self.IDLE = 0

                dungeon = Dungeon(action, refill=self.gem_refill)
                dungeon.go_to_dungeon()

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action == 'NM':
                self.IDLE = 0

                clan_boss = ClanBoss('NM', self.account)
                clan_boss.to_clan_boss()
                time.sleep(950)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action == 'UNM':
                self.IDLE = 0

                clan_boss = ClanBoss('UNM', self.account)
                clan_boss.to_clan_boss()

                time.sleep(950)
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

                arena = Arena('tag_arena')
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

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action == 'routine_market_refresh':

                self.IDLE = 0
                routine = Routine()
                routine.market_refresh()

                self.market_refresh = routine.market_CD
                print(self.market_refresh)

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1
                    
            elif action == 'mini_routine':

                self.IDLE = 0
                routine = Routine()
                routine.mini_routine()
                
                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action == 'FW':

                self.IDLE = 0
                fw = Dungeon('FW', 100, refill=self.gem_refill)
                fw.faction_wars()

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1

            elif action == 'doom_tower':

                self.IDLE = 0
                dungeon = Dungeon('doom_tower', 100, refill=self.gem_refill, dt_difficulty=self.dt_difficulty)
                dungeon.doom_tower()

                time.sleep(1)
                print('Bot: IDLE')
                self.IDLE = 1
               

raid = Raider(account='raid3', leveling=False, action='fire_knight', dungeon='fire_knight', dt_difficulty='hard', gem_refill=False, star_leveling=2)

while True:
    
    raid.main_loop()
    time.sleep(30)
    print("trying action...")

