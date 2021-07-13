from main import go_to_tavern
from numpy.lib.polynomial import _polyint_dispatcher
from numpy.random import randint
import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui
import datetime
from support_functions import go_to_stage, locate_and_click, get_center, go_to_base, adjusted_click, click_element,adjusted_move


class Routine():

    def __init__(self):

        self.STATE = 0

        self.market_CD = None


    def routine(self):

        # get daily login rewards
        go_to_base()
        self.login_rewards()

        # get mine rewards
        go_to_base()
        self.get_mine_gems()

        # Get shards from market
        go_to_base()
        self.market_refresh()
        
        # Campaign 7x run
        go_to_base()
        self.campaign_run()

        # Kill boss 3x times
        go_to_base()
        self.boss_run()
        
        #Level up hero three times
        go_to_base()
        self.go_to_tavern()

        # Get free shop rewards
        go_to_base()
        self.get_shop_rewards()

        # Play time rewards
        go_to_base()
        self.play_time_rewards()

        # Summon 3 heroes
        go_to_base()
        self.summon_heroes()

        # upgrade armor
        go_to_base()
        self.upgrade_armor()
        
        # Collect daily quests
        go_to_base()
        self.daily_quests_collect()

        # Collect arena champion
        go_to_base()
        self.arena_shop()
        
    def mini_routine(self):


        # get mine rewards
        go_to_base()
        self.get_mine_gems()

        # Get shards from market
        go_to_base()
        self.market_refresh()

        # Play time rewards
        go_to_base()
        self.play_time_rewards()

        # Collect daily quests
        go_to_base()
        self.daily_quests_collect()

        # Collect arena champion
        go_to_base()
        self.arena_shop()

    def login_rewards(self):

        time.sleep(1)
        adjusted_click(-618.0,10)
        time.sleep(1)
        adjusted_click(-587.0, -286)
        time.sleep(1)
        locate_and_click('collect_login')

    def arena_shop(self):

        
        locate_and_click('battle', 0.6)
        locate_and_click('arena')
     
        locate_and_click('tag_arena')

        time.sleep(2)
        adjusted_click(-514, 180)
        time.sleep(1)
        adjusted_click(576, -118)
        time.sleep(2)
        locate_and_click('buy_champion')


    def go_to_tavern(self):

        # Champions location
        adjusted_click(332, 316)
        time.sleep(2)
        # Tavern location
        adjusted_click(179, 224)
        time.sleep(2)
        # Remove hero
        adjusted_click(213, -260)
        time.sleep(2)
        x, y = get_center()
        pyautogui.moveTo(x - 500, y)
        time.sleep(1)
        #pyautogui.dragTo((x - 500), y - 400, duration=3)
        for i in range(50):
            pyautogui.scroll(-1)
        
        time.sleep(2)
        #click hero
        adjusted_click(-489, 207)
        for i in range(50):
            pyautogui.scroll(-1)
        time.sleep(2)
        adjusted_click(-489, 207)
        #time.sleep(2)
        #adjusted_click(-400, 207)
        #time.sleep(2)
        #adjusted_click(-569, 207)
        time.sleep(2)
        adjusted_click(480, 312)
        time.sleep(2)
     

    def upgrade_armor(self):

        time.sleep(2)
        # Champions location
        adjusted_click(332, 316)
        time.sleep(2)
        # Item location
        adjusted_click(465, 39)
        time.sleep(2)
        # Upgrade location
        adjusted_click(-556, -43)
        time.sleep(2)
        # Upgrade item location
        for i in range(4):
            adjusted_click(126, 305)
            time.sleep(3)

    def market_refresh(self):

        if self.market_CD == None:
            self.market_CD = datetime.datetime.now()
            

        x, y = get_center()
        time.sleep(2)
        adjusted_move(400.0, 150.5)
        time.sleep(2)
        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]+ 400, mouse_position[1]-400, duration=5)
        
        adjusted_click(93, -16)

        time.sleep(2)
        #for i in range(3)
        for i in range(5):
            try:
                loc = pyautogui.locateOnScreen('./images/mystery_shard_market.png', confidence=0.7)
                location = pyautogui.center(loc)
                click_element(location[0]+200, location[1])
                time.sleep(1)
                locate_and_click('get_mystery')
            except Exception:
                print("Shard not found")

        for i in range(10):
            pyautogui.scroll(-1)


        for i in range(5):
            try:
                loc = pyautogui.locateOnScreen('./images/mystery_shard_market.png', confidence=0.7)
                location = pyautogui.center(loc)
                click_element(location[0]+200, location[1])
                time.sleep(1)
                locate_and_click('get_mystery')
            except Exception:
                print("Shard not found")


    
    def campaign_run(self):

        # Battle location
        adjusted_click(505.0, 310.5)
        time.sleep(2)
        locate_and_click('campaing_location')
        time.sleep(2)
        locate_and_click('clerog_castle')
        time.sleep(2)
        for i in range(7):
            pyautogui.scroll(-1)
        time.sleep(2)
        adjusted_click(510, 150)
        time.sleep(2)
        locate_and_click('start_clerog')

        n = 0
        while n < 6:
            time.sleep(1)
            print(f"round {n+1}")
            if pyautogui.locateOnScreen('./images/replay_clerog.png', confidence=0.7) != None:
                locate_and_click("replay_clerog")
                n+=1

        time.sleep(10)


    def boss_run(self):

        # Battle location
        adjusted_click(505.0, 310.5)
        time.sleep(2)
        locate_and_click('campaing_location')
        time.sleep(2)
        locate_and_click('clerog_castle')
        time.sleep(2)
        for i in range(7):
            pyautogui.scroll(-1)
        time.sleep(2)
        adjusted_click(510, 300)
        time.sleep(2)
        locate_and_click('start_clerog')

        n = 0
        while n < 2:
            time.sleep(1)
            print(f"round {n+1}")
            if pyautogui.locateOnScreen('./images/replay_clerog.png', confidence=0.7) != None:
                locate_and_click("replay_clerog")
                n+=1

        time.sleep(10)

    def summon_heroes(self):

        time.sleep(2)
        adjusted_move(400.0, 150.5)
        time.sleep(2)
        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]+ 500, mouse_position[1]+400, duration=5)

        adjusted_click(-156.0, 93.5)
        time.sleep(1)
        locate_and_click('summon_green')
        time.sleep(3)
        locate_and_click('summon_green_2')
        time.sleep(3)
        locate_and_click('summon_green_2')
        time.sleep(3)
        go_to_base()

    def daily_quests_collect(self):

        # Quests location
        adjusted_click(-248, 316)

        time.sleep(2)
        while pyautogui.locateOnScreen('./images/claim_daily.png') != None:
            locate_and_click('claim_daily')
            time.sleep(1)
            if pyautogui.locateOnScreen('./images/quests_continue.png') != None:
                locate_and_click('quests_continue')


    def to_leveling(self):

        time.sleep(2)
        # Battle location
        adjusted_click(505.0, 310.5)
        locate_and_click('to_leveling', 0.6)



    def play_time_rewards(self):
        '''
        Collects all playtime rewards
        '''
        time.sleep(1)
        adjusted_click(550.0, 221.5)
        time.sleep(1)
        #loc = pyautogui.locateOnScreen('./images/playtime_1.png', confidence=0.8)
        #location = pyautogui.center(loc)
        adjusted_click(-344, 112)
        #click_element(location[0], location[1])

        pct = 140
        time.sleep(2)
        for i in range(5):
            adjusted_click(-344 + pct, 112)
            pct += 140
            time.sleep(2)

    def get_mine_gems(self):

        x, y = get_center()
        time.sleep(2)
        adjusted_move(400.0, 150.5)
        time.sleep(2)
        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]+ 400, mouse_position[1]-400, duration=5)
        locate_and_click('mine', conf=0.7)

    def get_shop_rewards(self):
        
        time.sleep(1)
        locate_and_click('shop_free')
        locate_and_click('mystery_shard')
        locate_and_click('claim')
        locate_and_click('ancient_shard')
        locate_and_click('claim')

        locate_and_click('limited_offer')
 
        adjusted_click(-360, -252)
        #click_element(location[0], location[1])

        pct = 70
        time.sleep(2)
        for i in range(13):
            adjusted_click(-360 + pct, -252)
            pct += 70
            locate_and_click('claim_free_gift')
            time.sleep(2)




    