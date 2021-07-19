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

from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element, go_to_stage, adjusted_move



class Dungeon():

    def __init__(self, dungeon, runs=None, refill=False, stage = None):

        self.dungeon = dungeon
        self.runs = runs
        self.energy_refill = refill
        self.stage = stage

        self.potions_keeps = ['force', 'spirit', 'magic', 'void', 'arcane']
        self.dungeons = {'dragon':25,
                        'spider':20,
                        'ice_golem':20,
                        'fire_knight':20,
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

    def doom_tower(self):

        go_to_base()

        locate_and_click('battle', 0.6)
        mouse_position = pyautogui.position()
        pyautogui.moveTo(mouse_position[0], mouse_position[1] - 200)
        time.sleep(1)
        pyautogui.dragTo(mouse_position[0]- 700, mouse_position[1], duration=5)

        locate_and_click('doom_tower_enter')

        time.sleep(2)

        try:
            locate_and_click('magma_dragon_raid', wait_time=0.5)
        except:
            locate_and_click('doom_tower_attack')
            time.sleep(2)
            locate_and_click('start_battle_doom')

        if self.STATE == 1:
            while self.STATE == 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_dt.png') == None:
                    print(f'Waiting for the game to finish, round: {self.game_runs+1} Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_dt.png', confidence=0.9) != None:
                        self.victory +=1
                        self.game_runs +=1
                        locate_and_click('next_dt')

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1
                        self.game_runs +=1
                        locate_and_click('next_dt')

                    # If runs more than defined runs, quit
                    if self.runs != None: 
                        if self.game_runs >= self.runs:
                            self.STATE = 0
                            break

                        

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
            'dark_elves': 13,
            'sacred_order':12,
            'banner_lords':15,
            'barbarians': 20,
            'dwarfs': 5,
            'knight_revenant':15,
            'lizardmen':11,
            'skinwalkers':9,
            'undead_horde':20,
            'demonspawn': 15,
            'ogryn_tribe':11,
            'orc':7,
            'high_elves': 20
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
            return 20
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

        # Go to designated stage
        if self.stage == None:
            go_to_stage(self.get_defualt_stage(self.dungeon))
        else:
            go_to_stage(self.stage)


        time.sleep(2)
        if pyautogui.locateOnScreen('./images/energy_refill.png', confidence=0.8) != None:
            if self.energy_refill == True:
                locate_and_click('energy_refill_dungeons', conf=0.8)

            else:
                self.STATE = 0
                

        locate_and_click('minotaur_start', conf=0.6)

        if self.STATE == 1:
            while self.STATE == 1:
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_minotaur.png', confidence=0.8) == None:
                    print(f'Waiting for the game to finish, round: {self.game_runs+1}. Win/loss: {self.victory}-{self.defeat}')
                else:
                    if pyautogui.locateOnScreen('./images/victory_minotaur.png', confidence=0.9) != None:
                        self.victory +=1
                        self.game_runs +=1

                    elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                        self.defeat +=1
                        self.game_runs +=1
                    

                    # If runs more than defined runs, quit 
                    if self.runs != None:
                        if self.game_runs >= self.runs:
                            self.STATE = 0
                            break
                    #check if daimond refresh
                    locate_and_click('replay_minotaur', conf=0.7)

                    if pyautogui.locateOnScreen('./images/gem_energy_refill.png', confidence=0.8) != None:
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
                        
                        
