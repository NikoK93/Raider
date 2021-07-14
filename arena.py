

from numpy.lib.polynomial import _polyint_dispatcher
from numpy.random import randint
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


class Arena():

    def __init__(self, arena_type):

        go_to_base()

        self.wins = 0
        self.STATE = 0

        self.arena_type = arena_type

    def arena_fight(self):

        
        if pyautogui.locateOnScreen('./images/tag_arena_refresh.png') != None:
            locate_and_click('tag_arena_refresh')
            # Edit, located start after refrest
            locate_and_click('classic_arena_start')
            
        elif pyautogui.locateOnScreen('./images/refresh_arena_classic.png') != None:
            locate_and_click('refresh_arena_classic')
            # Edit, located start after refrest
            locate_and_click('classic_arena_start')
        
        # Find the battle location and click to begin
        if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:
            locate_and_click('classic_arena_battle')
            time.sleep(2)
            # Refresh if possible and return False to start finding new matches
            if pyautogui.locateOnScreen('./images/confirm_arena_token.png') != None:
                locate_and_click("confirm_arena_token")
                return False
            # Return False and turn of STATE if gem refill has appeared
            elif pyautogui.locateOnScreen('./images/classic_arena_refill.png') != None:
                self.STATE = 0
                return False
            elif pyautogui.locateOnScreen('./images/tag_arena_gem.png') != None:
                self.STATE = 0
                return False

            # Start the arena figh
            else:
                locate_and_click('classic_arena_start')
                start = time.time()
                while self.STATE == 1:
                    time.sleep(2)
                    if pyautogui.locateOnScreen('./images/defeat_arena.png') != None:
                        print('Lost game, regresing list')
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
                        
                    elif pyautogui.locateOnScreen('./images/victory_arena.png') != None:
                        pyautogui.press('esc')
                        time.sleep(3)
                        if self.arena_type != 'classic':
                                pyautogui.press('esc')
                                time.sleep(1)
                        break
                        #
                    # Need to create a blacklist system for lost matches. 

                    else:
                        end = time.time()
                        time_elapsed = end - start
                        if time_elapsed > 500:
                            pyautogui.press('esc')
                            self.STATE = 0
                            return False
                        print('Waiting',(time_elapsed))
                        #print('game finished')
                        
                    
        else:
            return False

    def roam_and_fight(self):
        
        while self.STATE == 1:
            if self.arena_fight() == False:
                x, y = get_center()
                pyautogui.moveTo(x, y)
                mouse_position = pyautogui.position()

                pyautogui.dragTo(mouse_position[0], mouse_position[1] - 200, duration=2)
                
                #ran_int, y = self.get_scroll_parameters()
                #print(randint, y)
                #for i in range(randint):
                #  pyautogui.scroll(y)

        print('arena done')

    def go_to_arena(self):

        #locate_and_click('rsl')
        locate_and_click('battle', 0.6)
        locate_and_click('arena')
        if self.arena_type == 'classic':
            locate_and_click('classic_arena')
        else:
            locate_and_click('tag_arena')

        self.STATE = 1
        self.roam_and_fight()

    def get_scroll_parameters(self):
        
        rand_int = np.random.randint(1,100)
        rand_y = np.random.choice([1, -1], [0.3,0.7])

        return randint, rand_y