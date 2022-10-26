import time
import numpy as np
import datetime as dt
import sys
import argparse

from numpy.random import randint

import pyautogui
from pyautogui import run

from leveling import AutoLeveler
from clan_boss import ClanBoss
from clan_boss import unm_custom, nightmare_custom
from dungeon_master import Dungeon
from support_functions import open_raid, isNowInTimePeriod, locate_and_click, get_center, go_to_base, adjusted_click, click_element
from arena import Arena
from routines import Routine
import database

import timeit
from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element, go_to_stage, adjusted_move, check_if_no_aura


from custom_CB import unm_custom, unm_custom_raid2, nm_custom_raid2, unm_new_account, nm_new_account
from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element
from cb_test import nightmare_custom

'''
Game settings -
Graphics Quality: Low
Frame Rate Limit: 60 FPS
Resolution 1280x720

GAME_RESOLUTION = (1280, 720)

'''

parser = argparse.ArgumentParser('Bot configuration')
parser.add_argument('-c','--account', type=str)
parser.add_argument('-u','--dungeon', type=str)
parser.add_argument('-a', '--action', type=str)
parser.add_argument('-l','--leveling', action='store_true')
parser.add_argument('-e','--energy_spender_last', action='store_true')
parser.add_argument('-o','--action_one_time', action='store_true')
parser.add_argument('-g','--gem_refill', action='store_true')
parser.add_argument('-d','--dungeon_runs', type=int, default=None)
parser.add_argument('-s','--star_leveling', type=int, default=2)
parser.add_argument('-t','--dt_difficutly', type=str, default='hard')
args = parser.parse_args()

class Raider():

    def __init__(self, account, dungeon=None, energy_spender_last=False, leveling=False, dungeon_runs=None, gem_refill=False, action=None, action_one_time=False, star_leveling=2,  dt_difficulty='normal'):

        # Get center and open raid
        #self.CENTER_POSITION = open_raid()
        print(dt_difficulty)
        # Some default actions
        self.actions = ['arena', 'FW', 'tag_arena','doom_tower','mini_routine']
        #self.actions = ['arena']
        # Action which will not be appended and reapeated
        self.daily_action = ['UNM', 'NM', 'routine', 'routine_market_refresh']

        # Avaliable dungeons
        self.dungeons = ['force', 'spirit', 'magic', 'void', 'arcane', 'dragon', 'spider', 'ice_golem', 'fire_knight', 'minotaur'] 
        self.dungeons_subset = ['dragon', 'spider', 'ice_golem', 'fire_knight'] 

        # User defined single action
        self.user_action = action

        # account information 
        self.account = account
        
        # Single runs through action
        self.action_one_time = action_one_time

        # If energy_spender_last == True, dungeon or leveling action will be taken after other actions
        self.energy_spender_last = energy_spender_last

        # Dungeon runs
        self.runs = dungeon_runs

        # Gem refill bool
        self.gem_refill = gem_refill

        # DoomTower difficulty
        self.dt_difficulty = dt_difficulty

        # Minimum star for leveling
        self.star_leveling = star_leveling

        # Leveling bool
        self.leveling = leveling

        # Choosing energy spender, and inserting it into actions stack at index 0
        #if not action:
        if self.leveling:
            if energy_spender_last:
                self.actions.append('leveling')
            else:
                self.actions.insert(0,'leveling')
        else:
            # if dungeon is defined, append to list. Else insert a random dungeon
            if dungeon:
                if energy_spender_last:
                    self.actions.append(dungeon)
                else:
                    self.actions.insert(0, dungeon)
            else:
                if energy_spender_last:
                    self.actions.append(np.random.choice(self.dungeons_subset))
                else:
                    self.actions.insert(0, np.random.choice(self.dungeons_subset))
            
        # Bot status
        self.IDLE = 1
        self.ON = 1
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

        # Print arguments
        print(self.account)
        print(f"Chosen dungeon: {dungeon}")
        print(f"Energy spender last: {self.energy_spender_last}")
        print(f"Leveling status: {self.leveling}")
        if action:
            print(f"Action chosen: {action}")

        #self.run()
    
    def run(self):

        while True:

            if len(self.actions) == 0:
                print('No actions left, quiting')
                break

        self.main_loop()
        time.sleep(30)
        print("trying action...")


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
    
    def arena(self):

        if self.IDLE:
            go_to_base()

        self.wins = 0
        self.STATE = 0
        self.refresh = False


        def arena_fight(self):

            # Check if refresh avaliable and refresh opponents
            if self.refresh == False:
                try:
                    locate_and_click('tag_arena_refresh')
                    self.refresh = True
                except:
                    print('Refresh not avaliable')
                    
            
            # Find the battle location and click to begin
            if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:
                locate_and_click('classic_arena_battle')
                time.sleep(1)

                # If pop-up for token refresh appears, confirm it
                if pyautogui.locateOnScreen('./images/confirm_arena_token.png') != None:
                    locate_and_click("confirm_arena_token")
                    #return False

                # Return False and set STATE to 0 if gem refill has appeared
                elif pyautogui.locateOnScreen('./images/classic_arena_refill.png') != None:
                    print('No gem refills, aborting.')
                    self.IDLE = 1
                    return False

                elif pyautogui.locateOnScreen('./images/tag_arena_gem.png') != None:
                    print('No gem refills, aborting.')
                    self.IDLE = 1
                    return False

                # Start the arena fight
                else:
                    # Make sure auto is ON
                    if pyautogui.locateOnScreen('./images/start_on_auto_OFF.png') != None:
                        locate_and_click("start_on_auto_OFF", x_adj=-100, conf=0.9)

                    # Click start
                    locate_and_click('classic_arena_start')

                    # Time the battle 
                    start = time.time()

                    while self.IDLE == 0:
                        
                        # Every two seconds
                        time.sleep(2)
                        
                        # Check for defeat
                        if pyautogui.locateOnScreen('./images/defeat_arena.png') != None:
                            print('Lost game.')
                            pyautogui.press('esc')
                            time.sleep(2)
                            if self.arena_type != 'classic':
                                pyautogui.press('esc')
                                time.sleep(1)
                                if pyautogui.locateOnScreen('./images/tag_arena_refresh.png'):
                                    locate_and_click('tag_arena_refresh')
                                    break
                            if pyautogui.locateOnScreen('./images/refresh_arena_classic.png') != None:
                                locate_and_click('refresh_arena_classic')
                                break
                            else:
                                self.IDLE = 1
                                break

                        # Check for victory
                        elif pyautogui.locateOnScreen('./images/victory_arena.png') != None:
                            pyautogui.press('esc')
                            time.sleep(3)
                            if self.arena_type != 'classic':
                                    pyautogui.press('esc')
                                    time.sleep(1)
                            break

                        # Check wether game is going on for too long
                        else:
                            # Failsafe for potential infinite games i.e. apothecary
                            end = time.time()
                            time_elapsed = end - start
                            if time_elapsed > 1000:
                                if self.arena_type == "tag_arena":
                                    time.sleep(2)
                                    locate_and_click('skip_battle')
                                    time.sleep(2)
                                    locate_and_click('skip_battle_2')
                                    
                                    #self.STATE = 0
                                    #return False
                                else:
                                    pyautogui.press('esc')
                                    time.sleep(2)
                                    locate_and_click('leave_battle')
                                    time.sleep(2)
                                    locate_and_click('leave_battle_2')
                                    time.sleep(2)
                                    pyautogui.press('esc')
                                    self.IDLE = 1
                                    return False

                            print(f'Waiting - {round(time_elapsed, 0)} seconds.')
        
                            
            # if arena battle button is not found, return False to scroll down    
            else:
                return False
    def main_loop(self):
        '''
        while self.ON:

            if len(self.actions) == 0:
                print('No actions left, quiting')
                break

            #raid.main_loop()
            time.sleep(10)
            print("trying action...")
        '''
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
            
        elif isNowInTimePeriod(dt.time(18,30), dt.time(23,30), dt.datetime.now().time()) and self.cb_MM == 0:
            # Insert NM as priority 1
            if 'NM' not in self.actions:
                self.actions.insert(0,'NM')
                # Write to database
                self.database.update_value('NM')

        elif self.user_action != None:
            #action = self.user_action
            ac = self.user_action.strip()
            self.actions.insert(0, ac)

        # Select action from index 0
        action = self.actions[0].strip()
        # Slice actions to remove the first element from priority queue
        self.actions = self.actions[1:]
        # Moving selected action to the bottom of the priority queue
        # Do not append actions which occour only once per day
        if action not in self.daily_action:
            # Do not append if action will be taken only once
            if self.action_one_time == False:
                self.actions.append(action)
        
        print(self.actions)

        #sys.stdout.write(f"Executing {action}...")
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

                dungeon = Dungeon(action, runs=self.runs, refill=self.gem_refill)
                while self.IDLE == 0:
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
                while self.IDLE == 0:
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
                
class Arena():

    def __init__(self, arena_type):
        
        go_to_base()

        self.wins = 0
        self.STATE = 0
        self.refresh = False

        self.arena_type = arena_type


    def arena_fight(self):

        # Check if refresh avaliable and refresh opponents
        if self.refresh == False:
            try:
                locate_and_click('tag_arena_refresh')
                self.refresh = True
            except:
                print('Refresh not avaliable')
                
        
        # Find the battle location and click to begin
        if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:
            locate_and_click('classic_arena_battle')
            time.sleep(1)

            # If pop-up for token refresh appears, confirm it
            if pyautogui.locateOnScreen('./images/confirm_arena_token.png') != None:
                locate_and_click("confirm_arena_token")
                #return False

            # Return False and set STATE to 0 if gem refill has appeared
            elif pyautogui.locateOnScreen('./images/classic_arena_refill.png') != None:
                print('No gem refills, aborting.')
                self.STATE = 0
                return False

            elif pyautogui.locateOnScreen('./images/tag_arena_gem.png') != None:
                print('No gem refills, aborting.')
                self.STATE = 0
                return False

            # Start the arena fight
            else:
                # Make sure auto is ON
                if pyautogui.locateOnScreen('./images/start_on_auto_OFF.png') != None:
                    locate_and_click("start_on_auto_OFF", x_adj=-100, conf=0.9)

                # Click start
                locate_and_click('classic_arena_start')

                # Time the battle 
                start = time.time()

                while self.STATE == 1:
                    
                    # Every two seconds
                    time.sleep(2)
                    
                    # Check for defeat
                    if pyautogui.locateOnScreen('./images/defeat_arena.png') != None:
                        print('Lost game.')
                        pyautogui.press('esc')
                        time.sleep(2)
                        if self.arena_type != 'classic':
                            pyautogui.press('esc')
                            time.sleep(1)
                            if pyautogui.locateOnScreen('./images/tag_arena_refresh.png'):
                                locate_and_click('tag_arena_refresh')
                                break
                        if pyautogui.locateOnScreen('./images/refresh_arena_classic.png') != None:
                            locate_and_click('refresh_arena_classic')
                            break
                        else:
                            self.STATE = 0
                            break

                    # Check for victory
                    elif pyautogui.locateOnScreen('./images/victory_arena.png') != None:
                        pyautogui.press('esc')
                        time.sleep(3)
                        if self.arena_type != 'classic':
                                pyautogui.press('esc')
                                time.sleep(1)
                        break

                    # Check wether game is going on for too long
                    else:
                        # Failsafe for potential infinite games i.e. apothecary
                        end = time.time()
                        time_elapsed = end - start
                        if time_elapsed > 1000:
                            if self.arena_type == "tag_arena":
                                time.sleep(2)
                                locate_and_click('skip_battle')
                                time.sleep(2)
                                locate_and_click('skip_battle_2')
                                
                                #self.STATE = 0
                                #return False
                            else:
                                pyautogui.press('esc')
                                time.sleep(2)
                                locate_and_click('leave_battle')
                                time.sleep(2)
                                locate_and_click('leave_battle_2')
                                time.sleep(2)
                                pyautogui.press('esc')
                                self.STATE = 0
                                return False

                        print(f'Waiting - {round(time_elapsed, 0)} seconds.')
    
                        
        # if arena battle button is not found, return False to scroll down    
        else:
            return False

    def roam_and_fight(self):
        
        while self.STATE == 1:
            if self.arena_fight() == False:
                x, y = get_center()
                pyautogui.moveTo(x, y)
                mouse_position = pyautogui.position()

                pyautogui.dragTo(mouse_position[0], mouse_position[1] - 200, duration=2)

        print('Arena done')

    def go_to_arena(self):
        
        # Battle location
        locate_and_click('battle', 0.6)

        # Arena location
        locate_and_click('arena')

        # Choose arena
        if self.arena_type == 'classic':
            locate_and_click('classic_arena')
        else:
            locate_and_click('tag_arena')

        # Begin main loop
        self.roam_and_fight()


    def get_scroll_parameters(self):
        
        rand_int = np.random.randint(1,100)
        rand_y = np.random.choice([1, -1], [0.3,0.7])

        return randint, rand_y

class ClanBoss():

    def __init__(self, difficulty, account):

        self.difficulty = difficulty
        self.account = account

    def to_clan_boss(self):

        # Make sure that user is at base
        go_to_base()

        locate_and_click('battle', 0.6)
        mouse_position = pyautogui.position()
        pyautogui.moveTo(mouse_position[0], mouse_position[1] - 200)
        time.sleep(1)
        pyautogui.dragTo(mouse_position[0]- 400, mouse_position[1], duration=5)

        
        locate_and_click('clan_boss_enter')
        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0], mouse_position[1] - 400, duration=5)

        if self.difficulty == 'UNM':
            locate_and_click('UNM', conf=0.7)   
            locate_and_click('clan_boss_battle', conf=0.7)
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            #locate_and_click('team_setup', conf=0.9)

            #if self.account == 'raid3':
            #    locate_and_click('team_UNM', conf=0.9, x_adj=-250)
            #elif self.account == 'raid2':
            #    locate_and_click('team_UNM_raid2', conf=0.9, x_adj=-250)

            #pyautogui.press('esc')
            #locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('clan_boss_start', conf=0.9)

            if self.account == 'raid3':
                unm_new_account()
            elif self.account == 'raid2':
                unm_custom_raid2()

            while True:
                if pyautogui.locateOnScreen('./images/cb_replay.png') != None:
                    locate_and_click('cb_replay', conf=0.9)
                    if self.account == 'raid3':
                        unm_new_account()
                    elif self.account == 'raid2':
                        unm_custom_raid2()
                    break
                time.sleep(20)

        elif self.difficulty == 'NM':
            locate_and_click('NM', conf=0.9)  
            locate_and_click('clan_boss_battle', conf=0.9)
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            #locate_and_click('team_setup', conf=0.9)

            #if self.account == 'raid3':
            #    locate_and_click('team_NM', conf=0.9, x_adj=-250)
            #elif self.account == 'raid2':
            #    locate_and_click('team_NM_raid2', conf=0.9, x_adj=-250)

            #pyautogui.press('esc')
            #locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('clan_boss_start', conf=0.9)
            nm_new_account()
            
            '''
            if self.account == 'raid3':
                nm_new_account()
            elif self.account == 'raid2':
                nm_custom_raid2()
            '''




class Dungeon():

    def __init__(self, dungeon, runs=None, refill=False, stage = None, dt_difficulty='normal'):

        self.dungeon = dungeon
        self.runs = runs
        self.energy_refill = refill
        self.stage = stage
        self.dt_difficulty = dt_difficulty

        self.potions_keeps = ['force', 'spirit', 'magic', 'void', 'arcane']
        self.dungeons = {'dragon':24,
                        'spider':24,
                        'ice_golem':24,
                        'fire_knight':24,
                        'minotaur':15}

        self.game_runs = 0
        self.victory = 0
        self.defeat = 0

        self.STATE = 1

        # Faction Wars
        self.defeated_fw = []

    def save_data(self):
        pass
    
    def stage_selection(self):
        pass

    def team_selector(self):
        pass

    def doom_tower(self):

        go_to_base()

        locate_and_click('battle', 0.6)
        mouse_position = pyautogui.position()
        pyautogui.moveTo(mouse_position[0], mouse_position[1] - 200)
        time.sleep(1)
        pyautogui.dragTo(mouse_position[0]- 700, mouse_position[1], duration=5)

        locate_and_click('doom_tower_enter')

        time.sleep(2)

        if self.dt_difficulty == 'hard':
            adjusted_click(-507.0, 318.5)
            time.sleep(2)
            adjusted_click(-507.0, 254.5)
        
        time.sleep(2)
       
        if pyautogui.locateOnScreen('./images/doom_tower_attack.png', confidence=0.5) != None:
            locate_and_click('doom_tower_attack', conf=0.5)
            time.sleep(2)
            locate_and_click('start_battle_doom', conf=0.5)
        else:
            print('Boss stage, aborting')
            self.STATE = 0


        if self.STATE == 1:
            while self.STATE == 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_dt.png', confidence=0.5) == None:
                    print(f'Waiting for the game to finish, round: {self.game_runs+1} Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_dt.png', confidence=0.7) != None:
                        self.victory +=1
                        self.game_runs +=1
                        locate_and_click('next_dt')
                        time.sleep(2)
                        
                        # if victory still present, we're out of key, break
                        if pyautogui.locateOnScreen('./images/victory_dt.png', confidence=0.7) != None:
                            self.STATE = 0
                            break  
                        # elif roster is empty, we're at boss stage, break
                        elif pyautogui.locateOnScreen('./images/boss_stage.png', confidence=0.8) != None:
                            self.STATE = 0
                            break  
                        else:
                            time.sleep(2)
                            locate_and_click('start_battle_doom')

                    elif pyautogui.locateOnScreen('./images/defeat_dt.png', confidence=0.7) != None:
                        self.defeat +=1
                        self.game_runs +=1

                        if self.defeat >= 20:
                            self.STATE = 0
                            break

                        locate_and_click('replay_dt', conf=0.5)


                        

    def faction_wars(self):

        go_to_base()
        # Battle location
        adjusted_click(505.0, 310.5)
        time.sleep(1)

        locate_and_click('faction_wars')
        time.sleep(2)

        # adjusted cords based start state of FW
        first_cords = {
            'dark_elves': (0, 125),
            'sacred_order':(165, -33),
            'banner_lords':(348, -170),
            'barbarians': (388, 128),
            'orc':(-181, -34),
            'dwarfs': (579, -22)
        }

        second_cords = {
            'knight_revenant':(-203, 151),
            'lizardmen':(-360, -20),
            'skinwalkers':(-195, -174),
            'undead_horde':(-14, -32),
            'demonspawn':(138, -177),
            'ogryn_tribe':(271, 139),
            'high_elves':(462, -193)
        }

        faction_wars_stages = {
            'dark_elves': 17,
            'sacred_order':12,
            'banner_lords':14,
            'barbarians': 21,
            'dwarfs': 12,
            'knight_revenant':17,
            'lizardmen':21,
            'skinwalkers':18,
            'undead_horde':20,
            'demonspawn': 18,
            'ogryn_tribe':17,
            'orc':17,
            'high_elves': 21
        }      

        def battle(key, value):
            
            x, y = value
            adjusted_click(x, y)
            time.sleep(2)
            if pyautogui.locateOnScreen('./images/fw_screen.png', confidence=0.8) != None:
                print(f'entered {key} crypt')
                print(f'Progressing stage: {faction_wars_stages[key]}')
                go_to_stage(faction_wars_stages[key])
                time.sleep(2)

                # Start game
                adjusted_click(460,304)
                time.sleep(4)
                if pyautogui.locateOnScreen('./images/fw_screen.png', confidence=0.8) != None:
                    print('Out of keys')
                    self.defeated_fw.append(key)
                    pyautogui.press('esc')
                    time.sleep(2)
                    
                else:
                    while True:
                        time.sleep(2)
                        print(f'Waiting for the game to finish, round: {self.game_runs+1}. Win/loss: {self.victory}-{self.defeat}')
                        if pyautogui.locateOnScreen('./images/defeat_fw.png', confidence=0.8) != None:

                            # Record status
                            self.defeat +=1
                            self.game_runs +=1
                            #replay
                            time.sleep(1)
                            adjusted_click(92,314)
                            time.sleep(5)
                            if pyautogui.locateOnScreen('./images/out_of_key.png', confidence=0.8) != None:
                                #self.STATE == 0
                                pyautogui.press('esc')
                                time.sleep(2)
                                pyautogui.press('esc')
                                time.sleep(2)
                                break
                        elif pyautogui.locateOnScreen('./images/victory_fw.png', confidence=0.8) != None:
                            # Record status
                            self.victory +=1
                            self.game_runs +=1
                            time.sleep(1)
                            adjusted_click(92,314)
                            time.sleep(5)
                            if pyautogui.locateOnScreen('./images/out_of_key.png', confidence=0.8) != None:
                                #self.STATE == 0
                                pyautogui.press('esc')
                                time.sleep(2)
                                pyautogui.press('esc')
                                time.sleep(2)
                                break

        def click_cords(cords):

            for key, value in cords.items():
                #self.STATE = 1
                battle(key, value)
                    
    
        click_cords(first_cords) 

        time.sleep(2)
        adjusted_move(0, 125)
        mouse_position = pyautogui.position()
        time.sleep(1)
        pyautogui.dragTo(mouse_position[0]+ 800, mouse_position[1], duration=4)

        click_cords(second_cords)

                        
    def drag_to_dungeon_and_click(self, dungeon):

        if dungeon in self.potions_keeps:
            locate_and_click(dungeon, 0.5)

        else:
            x,y = get_center()
            pyautogui.moveTo(x+600, y)
            mouse_position = pyautogui.position()
            pyautogui.dragTo(mouse_position[0]- 1200, mouse_position[1], duration=5)
            time.sleep(2)
            locate_and_click(dungeon, 0.5)


    # Return the stage for dungeon
    def get_defualt_stage(self, dungeon):

        if dungeon in self.potions_keeps:
            return 12
        else:
            return self.dungeons[dungeon]

    def go_to_dungeon(self):
        
        # Returning to base
        go_to_base()

        # Clicking battle location
        adjusted_click(505.0, 310.5)

        # Clicking dungeons
        locate_and_click('dungeons', 0.7)

        # Go to dungeona and enter
        self.drag_to_dungeon_and_click(self.dungeon)

        # Go to designated stage, and click start
        if self.stage == None:
            go_to_stage(self.get_defualt_stage(self.dungeon))
        else:
            go_to_stage(self.stage)


        time.sleep(2)
        # Check if energy is avaliable and enter the game
        if pyautogui.locateOnScreen('./images/energy_refill_dungeons.png', confidence=0.9) != None:
                locate_and_click('energy_refill_dungeons', conf=0.8)
                time.sleep(2)
                adjusted_click(483.0, 281.5)

        # Check for gem refill, and enter if gem refill is true
        elif pyautogui.locateOnScreen('./images/gem_refill_confirm.png', confidence=0.9) != None:
            if self.energy_refill:
                locate_and_click('gem_refill_confirm')
                time.sleep(2)
                adjusted_click(483.0, 281.5)
            else:
                self.STATE = 0
                
        # Start the game
        locate_and_click('minotaur_start', conf=0.6)
        
        # Check if no aura 
        check_if_no_aura()

        # Main loop
        if self.STATE == 1:
            while self.STATE == 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_minotaur.png', confidence=0.8) == None:
                    print(f'Waiting for the game to finish, round: {self.game_runs+1}. Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/level_up.png', confidence=0.9) != None:
                        pyautogui.press('esc')
                        
                    elif pyautogui.locateOnScreen('./images/victory_minotaur.png', confidence=0.9) != None:
                        self.victory +=1
                        self.game_runs +=1

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1
                        self.game_runs +=1
                    

                    # If runs more than defined runs, quit 
                    if self.runs != None:
                        if self.game_runs >= self.runs:
                            print(f"{self.game_runs - self.runs} runs left")
                            self.STATE = 0
                            break

                    # Click replay button
                    locate_and_click('replay_minotaur', conf=0.7)

                    # Check for gem and non-gem refills
                    if pyautogui.locateOnScreen('./images/energy_refill_dungeons.png', confidence=0.9) != None:
                                locate_and_click('energy_refill_dungeons', conf=0.8)
                                time.sleep(2)
                                locate_and_click('replay_minotaur')

                    elif pyautogui.locateOnScreen('./images/gem_refill_confirm.png', confidence=0.9) != None:
                        if self.energy_refill:
                            locate_and_click('gem_refill_confirm')
                            time.sleep(2)
                            locate_and_click('replay_minotaur')
                        else:
                            print('Aborting, no gem refills.')
                            self.STATE = 0
                            break

                            
                        
                        


if __name__ == '__main__':

    #raid = Raider(account=sys.argv[1], dungeon=sys.argv[2], action=sys.argv[3])
    
    #if args.action:
    #    raid = Raider(account=args.account, dungeon=args.dungeon, action=args.action)
    #else:
    raid = Raider(account=args.account, dungeon=args.dungeon, action=args.action, leveling=args.leveling, 
        dungeon_runs=args.dungeon_runs, star_leveling=args.star_leveling, 
        energy_spender_last=args.energy_spender_last, gem_refill=args.gem_refill, dt_difficulty=args.dt_difficutly,
        action_one_time=args.action_one_time)

    while True:

        if len(raid.actions) == 0:
            print('No actions left, quiting')
            break

        raid.main_loop()
        time.sleep(30)
        print("trying action...")


