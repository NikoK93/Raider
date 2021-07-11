from numpy.lib.polynomial import _polyint_dispatcher
import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui

from clan_boss import unm_custom, nightmare_custom
from support_functions import get_difference

from windowcapture import WindowCapture
from vision import Vision
import pytesseract
tes_path = pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import timeit

from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element



class Dungeon():

    def __init__(self, dungeon, runs, refill):

        self.dungeon = dungeon
        self.runs = runs

        self.victory = 0
        self.defeat = 0

        self.STATE = 1

        self.energy_refill = refill

    def save_data(self):
        pass

    def faction_wars(self):

        go_to_base()
        # Battle location
        adjusted_click(505.0, 310.5)
        time.sleep(1)

        locate_and_click('faction_wars')
        time.sleep(2)

        locate_and_click('orc_crypt', conf=0.5)
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