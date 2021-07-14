from numpy.lib.polynomial import _polyint_dispatcher
import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui

from clan_boss import unm_custom, nightmare_custom
from support_functions import adjusted_move, get_difference

from windowcapture import WindowCapture
from vision import Vision
import pytesseract
tes_path = pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import timeit

from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element, go_to_stage



class Dungeon():

    def __init__(self, dungeon, runs, refill):

        self.dungeon = dungeon
        self.runs = runs

        self.game_runs = 0
        self.victory = 0
        self.defeat = 0

        self.STATE = 1

        self.energy_refill = refill

        # Faction Wars
        self.defeated_fw = []

    def save_data(self):
        pass
    
    def stage_selection(self):
        pass

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
            'dwarfs': (579, -22)
        }

        second_cords = {
            'knight_revenant':(-203, 151),
            'lizardmen':(-360, -20),
            'skinwalkers':(-195, -174),
            'undead_horde':(-14, -32),
            'demonspawn':(138, -177),
            'ogryn_tribe':(271, 139),
            'orc':(-368, -23),
            'high_elves':(462, -193)
        }

        faction_wars_stages = {
            'dark_elves': 1,
            'sacred_order':12,
            'banner_lords':1,
            'barbarians': 1,
            'dwarfs': 5,
            'knight_revenant':1,
            'lizardmen':11,
            'skinwalkers':9,
            'undead_horde':1,
            'demonspawn': 12,
            'ogryn_tribe':11,
            'orc':1,
            'high_elves': 16
        }      


        def click_cords(cords):

            for key, value in cords.items():
                self.STATE = 1

                if key in self.defeated_fw:
                    continue
                else:
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
                            continue
                        else:
                            while self.STATE == 1:
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
                                        self.STATE == 0
                                        pyautogui.press('esc')
                                        time.sleep(2)
                                        pyautogui.press('esc')
                                        time.sleep(2)
                                        continue
                                elif pyautogui.locateOnScreen('./images/victory_fw.png', confidence=0.8) != None:
                                    # Record status
                                    self.victory +=1
                                    self.game_runs +=1
                                    time.sleep(1)
                                    adjusted_click(92,314)
                                    time.sleep(5)
                                    if pyautogui.locateOnScreen('./images/out_of_key.png', confidence=0.8) != None:
                                        self.STATE == 0
                                        pyautogui.press('esc')
                                        time.sleep(2)
                                        pyautogui.press('esc')
                                        time.sleep(2)
                                        continue
                        
                        return key      
            return False

        if click_cords(first_cords) == False:

            time.sleep(2)
            adjusted_move(0, 125)
            mouse_position = pyautogui.position()
            time.sleep(1)
            pyautogui.dragTo(mouse_position[0]+ 800, mouse_position[1], duration=4)

            click_cords(second_cords)

    

    def to_spider(self):

        go_to_base()

        locate_and_click('rsl')
        # Battle location
        adjusted_click(505.0, 310.5)

        locate_and_click('dungeons', 0.7)

        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]- 1000, mouse_position[1], duration=5)
        locate_and_click('spider', 0.8)

        for i in range(60):
            pyautogui.scroll(-1)

        x,y = get_center()
        time.sleep(1)
        click_element(x + 400, y +190)

        time.sleep(2)
        if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
            if self.energy_refill == True:
                locate_and_click('energy_refill_dungeons', conf=0.8)
                time.sleep(2)
                click_element(x + 400, y +190)
            else:
                self.STATE = 0
                

        locate_and_click('dragon_start')

        if self.STATE == 1:
            while self.runs >= 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_spider.png') == None:
                    print(f'Waiting for the game to finish, round: {self.runs}. Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_spider.png', confidence=0.9) != None:
                        self.victory +=1

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1

                    self.runs -= 1

                    if self.runs >= 1:
                        #check if daimond refresh
                        locate_and_click('replay_spider')
    
                        if pyautogui.locateOnScreen('./images/gem_energy_refill.png') != None:
                            print('Aborting, no gem refills.')
                            self.STATE = 0
                            break
                        else:
                            if self.energy_refill == True:
                                time.sleep(2)
                                if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
                                    locate_and_click('energy_refill_dungeons', conf=0.8)
                                    time.sleep(2)
                                    locate_and_click('replay_spider')
                            
                            
                    else:   
                        print('Finished games')
                        self.STATE = 0
                        break
    def minotaur(self):

        go_to_base()

        locate_and_click('rsl')
        # Battle location
        adjusted_click(505.0, 310.5)

        locate_and_click('dungeons', 0.7)

        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]- 1000, mouse_position[1], duration=5)
        
        locate_and_click('minotaur', 0.7)
        '''
        for i in range(60):
            pyautogui.scroll(-1)

        x,y = get_center()
        time.sleep(1)
        
        click_element(x + 500, y +300)
        '''
        go_to_stage(15)

    

        time.sleep(2)
        if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
            if self.energy_refill == True:
                locate_and_click('energy_refill_dungeons', conf=0.8)

            else:
                self.STATE = 0
                

        locate_and_click('minotaur_start', conf=0.6)

        if self.STATE == 1:
            while self.runs >= 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_minotaur.png') == None:
                    print(f'Waiting for the game to finish, round: {self.runs}. Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_minotaur.png', confidence=0.9) != None:
                        self.victory +=1

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1

                    self.runs -= 1
                    if self.runs >= 1:
                        #check if daimond refresh
                        locate_and_click('replay_minotaur')
    
                        if pyautogui.locateOnScreen('./images/gem_energy_refill.png') != None:
                            print('Aborting, no gem refills.')
                            self.STATE = 0
                            break
                        else:
                            if self.energy_refill == True:
                                time.sleep(2)
                                if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
                                    locate_and_click('energy_refill_dungeons', conf=0.8)
                                    time.sleep(2)
                                    locate_and_click('replay_minotaur')
                            
                            
                    else:   
                        print('Finished games')
                        self.STATE = 0
                        break

    def dragon(self, stage=25):

        go_to_base()

        locate_and_click('rsl')
        # Battle location
        adjusted_click(505.0, 310.5)

        locate_and_click('dungeons', 0.7)

        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0]- 1000, mouse_position[1], duration=5)
        
        
        locate_and_click('dragon', 0.7)

        go_to_stage(stage)

        time.sleep(2)
        if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
            if self.energy_refill == True:
                locate_and_click('energy_refill_dungeons', conf=0.8)
                time.sleep(2)
                click_element(x + 400, y +190)
            else:
                self.STATE = 0
    

        locate_and_click('minotaur_start')

        if self.STATE == 1:
            while self.runs >= 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_minotaur.png') == None:
                    print(f'Waiting for the game to finish, round: {self.runs}. Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_minotaur.png', confidence=0.9) != None:
                        self.victory +=1

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1

                    self.runs -= 1
                    if self.runs >= 1:
                        #check if daimond refresh
                        locate_and_click('replay_minotaur')
    
                        if pyautogui.locateOnScreen('./images/gem_energy_refill.png') != None:
                            print('Aborting, no gem refills.')
                            self.STATE = 0
                            break
                        else:
                            if self.energy_refill == True:
                                time.sleep(2)
                                if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
                                    locate_and_click('energy_refill_dungeons', conf=0.8)
                                    time.sleep(2)
                                    locate_and_click('replay_minotaur')
                            
                            
                    else:   
                        print('Finished games')
                        self.STATE = 0
                        break
        
        