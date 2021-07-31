from subprocess import run
from numpy.lib.polynomial import _polyint_dispatcher
import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui

from windowcapture_modified import WindowCapture as WC
from windowcapture import WindowCapture
from vision import Vision

import pytesseract
tes_path = pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from support_functions import go_to_base, locate_and_click, adjusted_click, adjusted_move, get_center, go_to_stage
import database

class AutoLeveler():

    def __init__(self, refill, runs_left=0, minimum_star=2):

        # Gem refill bool
        self.energy_refill = refill
        # Runs left from previous leveling
        self.runs_left = runs_left
        if runs_left != 0:
            print('Resuming previous runs')
        # Define the minimum star level to level up
        self.minimum_star = minimum_star

        # Asigning current star treshold to minimum star
        self.leveling_star = minimum_star
        
        # Number of runs based on star level with xp boost
        self.leveling_table = {
            1:3,
            2:10,
            3:24,
            4:52
        }
        # Bool - if energy avaliable
        self.energy = True
        
        # current runs
        self.game_runs = 0

        self.victory = 0
        self.defeat = 0

        # Load in the database
        self.database = database.DataBaseManager()

        # Set state to 1
        self.STATE = 1

        # Set state to 0 if no xp boost is active
        #if self.xp_boost_status() == False:
        #    self.STATE = 0

    def xp_boost_status(self):

        go_to_base()

        adjusted_click(505.0, 310.5)
        time.sleep(2)
        if pyautogui.locateOnScreen('./images/xp_boost_on.png') != None:
            print('XP buff on')
            return True
        else:
            print('no XP buff')
            return False

    def hero_screenshot(self):
        
        # OCR version for digit (LEVEL) recognition, currently replaced by a more primitive system.
        '''
        wincap = WC('Raid: Shadow Legends')

        #while True:
        # Geting a croped screenshot for selected hero
        screenshot = wincap.get_screenshot()

        # Preprocessing 
        gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (7, 7), 0)
        # Thresholding
        thr = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                    cv.THRESH_BINARY_INV, 21, 10)
        # Ocr
        text = pytesseract.image_to_string(blurred, lang='eng')

        # Geting the level
        num = [el for el in text if el.isdigit()]
        #logging.warning(text)
        #print(text)
        #print(num)
        '''
        # Check if hero is level one
        level = 0
        if pyautogui.locateOnScreen('./images/level_one.png', confidence=0.9) != None:
            print('Level one!')
            level = 1
        else:
            print('Not level one')

        # Check for star level of the hero by desceding order. Return level + star level
        if pyautogui.locateOnScreen('./images/five_star.png', confidence=0.9) != None:
            print('Five star character')
            return (level, 5)
        elif pyautogui.locateOnScreen('./images/four_star.png', confidence=0.9) != None:
            print('Four star character')
            return (level, 4)
        elif pyautogui.locateOnScreen('./images/three_star.png', confidence=0.9) != None:
            print('Three star character')
            return (level, 3)
        elif pyautogui.locateOnScreen('./images/two_star.png', confidence=0.9) != None:
            print('Two star character')
            return (level, 2)
        elif pyautogui.locateOnScreen('./images/one_star.png', confidence=0.9) != None:
            print('One star character')
            return (level, 1)
     

    def generate_cords(self):
        
        # Generate cords for bottom row
        start_x = 245
        start_y = 293
        adjust = 100

        positions_bottom = []

        for i in range(30):
            positions_bottom.append((start_x, start_y))
            start_x-=adjust
        
        # Generate cords for top row
        start_x = 245
        start_y = 293
        adjust = 100

        positions_top = []

        for i in range(30):
            positions_top.append((start_x, start_y-100))
            start_x-=adjust

        # Join by alternating top/bottom cords
        result = [None]*(len(positions_bottom)+len(positions_top))
        result[::2] = positions_bottom
        result[1::2] = positions_top

        # Create an iter object
        cords = iter(result)

        return cords

    def to_leveling(self):
        
        if self.STATE == 1:

            go_to_base()
           
            # Battle location
            adjusted_click(505.0, 310.5)
            locate_and_click('campaing_location', 0.8)  

            # Move to 12-3
            x,y = get_center()
            for i in range(3):
                pyautogui.moveTo(x+600, y)
                mouse_position = pyautogui.position()
                pyautogui.dragTo(mouse_position[0]- 1200, mouse_position[1], duration=5)
                time.sleep(2)

            # Go to stage 12-3 by default 
            locate_and_click('stage_12', 0.8)
            time.sleep(2)
            go_to_stage(3)
            time.sleep(2)

            # Deselect heroes if 0 runs left from previous uncompleted run
            if self.runs_left == 0:
                self.deselect()
            
            # Move to the far right, where heroes are level 1
            pyautogui.moveTo(x-300, y+300)
            for i in range(150):
                pyautogui.scroll(1)

            # if previous run was completed fully, add new heroes
            if self.runs_left == 0:
                self.add_leveling_heroes()

            # Start leveling loop
            self.leveling_loop()

    def repeat_leveling(self):

        pyautogui.press('esc')
        time.sleep(20)
        go_to_stage(3)
        time.sleep(2)
        self.deselect()

        x,y = get_center()
        pyautogui.moveTo(x-300, y+300)
        for i in range(150):
            pyautogui.scroll(1)

        self.add_leveling_heroes()

        self.leveling_loop()

    def leveling_loop(self):
        
        # Get the number of runs for specific star level
        if self.runs_left != 0:
            runs = self.runs_left
        else:
            runs = self.leveling_table[self.leveling_star]

        locate_and_click('start_leveling', conf=0.7)

        if self.STATE == 1:
            while self.STATE == 1:
                # Every 2 seconds check if game is done
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/replay_leveling.png', confidence=0.8) == None:

                    if pyautogui.locateOnScreen('./images/level_up.png', confidence=0.8) != None:
                        pyautogui.press('esc')
                    print(f'Waiting for the game to finish, round: {self.game_runs+1}, rounds untill max level: {runs-(self.game_runs+1)}')
                else:
                    
                    self.game_runs +=1
                    
                    # If runs more than defined runs, break 
                    if runs == self.game_runs:
                        # Reseting number of runs and leftover runs, sice heroes are max at this point.
                        self.game_runs = 0
                        self.runs_left = 0
                        # updating runs left to database
                        self.database.update_leveling_value(0)
                        
                        break

                    # Click replay button
                    locate_and_click('replay_leveling', conf=0.7)

                    # Check for gem and non-gem refills
                    if pyautogui.locateOnScreen('./images/energy_refill_dungeons.png', confidence=0.9) != None:
                                locate_and_click('energy_refill_dungeons', conf=0.8)
                                time.sleep(2)
                                locate_and_click('replay_leveling')

                    elif pyautogui.locateOnScreen('./images/gem_refill_confirm.png', confidence=0.9) != None:
                        if self.energy_refill:
                            locate_and_click('gem_refill_confirm')
                            time.sleep(2)
                            locate_and_click('replay_leveling')
                        else:
                            print('Aborting, no gem refills.')
                            self.energy = False
                            self.STATE = 0
                            print('Saving lefover runs')
                            runs_left = runs-self.game_runs
                            self.database.update_leveling_value(runs_left)
                            break
            # If energy still avaliable, repeat leveling process
            if self.energy:
                self.repeat_leveling()

    def deselect(self):

        adjusted_click(-339.0, 20.5)
        time.sleep(1)
        adjusted_click(-458, -91)
        time.sleep(1)
        adjusted_click(-343, -179)

    def add_leveling_heroes(self):
        
        print(f"Adding {self.leveling_star} star heroes")
        
        # Get cordinations for hero locations
        cords = self.generate_cords()

        # Number of tries before increasing star threshold
        number_of_tries = 0

        # While leveling slots are empty, keep searching for potential heroes
        while pyautogui.locateOnScreen('./images/empty_leveling_slot.png', confidence=0.7) != None:
            
            # if number of tries is greater than 5, increase the threshold 
            if number_of_tries > 10:
                print(f'Increasing star treshold to {self.leveling_star +1}')
                self.deselect()

                # check if current star threshold is allready 4 (which is a maximum)
                if self.leveling_star == 4:
                    print('No heroes avaliable, exiting leveling process')
                    self.STATE = 0
                    break

                self.leveling_star +=1
                number_of_tries = 0
                cords = self.generate_cords()

            # Get cords for next hero location
            x, y = next(cords)
            
            # Move to location and select hero
            adjusted_move(x, y)
            time.sleep(1)
            pyautogui.mouseDown(duration=2)
            time.sleep(1)
            pyautogui.mouseUp()
            number_of_tries +=1

            try:
                # Get level and star from selected hero
                level, star = self.hero_screenshot()

                # Return to previous window
                pyautogui.press('esc')
                time.sleep(3)
                print(level, star)
                # if level is 1 and the number of stars equals current leveling star level, add the hero
                if level == 1:
                    if star == self.leveling_star:
                        adjusted_click(x, y)

            except:
                print('No Hero selected')
            
        

#a = AutoLeveler(refill=False)
#a.hero_screenshot()