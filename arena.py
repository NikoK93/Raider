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

from support_functions import locate_and_click, get_center


class Arena():

    CENTER_POSITION = get_center()

    def __init__(self, type='classic'):

        self.black_list = []
        self.wins = []

    def go_to_arena(self):

        locate_and_click('rsl')
        locate_and_click('battle', 0.6)
        locate_and_click('arena')
        locate_and_click('classic_arena')
    
        self.roam_and_fight()

    def find_images(self, image):

        vision_chracters = Vision(f'./images/{image}.jpg')
        wincap = WindowCapture('Raid: Shadow Legends')

 
        time.sleep(1)
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        
        # display the processed image
        
        points, location = vision_chracters.find(screenshot, 0.5, 'rectangles')
        #print(pytesseract.image_to_string(points))
        #print(points, location)


        # get's screen position
        x, y = location[0][0], location[0][1]
        x_, y_ = wincap.get_screen_position((x, y))
        # makes a screenshot based on the position
        im = pyautogui.screenshot(region=(x_, y_, location[0][2], location[0][3]))

        # ocr the text from the image
        text = pytesseract.image_to_string(im)
        
        #if text not in self.black_list:
        #    pyautogui.moveTo(x_+800, y_+50)

        return x_, y_, text

    def arena_fight(self):

        if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:

            x_, y_, player = self.find_images("test_3")
            print(x_, y_, player)

            if player in self.black_list or player in self.wins:
                # check if game can be accesed
                # pyautogui.click(x_+800, y_+50) 
                return True

            pyautogui.click(x_+800, y_+50)
            time.sleep(2)
            if pyautogui.locateOnScreen('./images/locate_if_arena.png') != None:
                return True


            locate_and_click('classic_arena_start')
            start = time.time()
            while (True):
                time.sleep(2)
                if pyautogui.locateOnScreen('./images/defeat.png') != None:
                    print('Lost game, regresing list')

                    self.black_list.append(player)

                    pyautogui.press('esc')
   
                    break
                elif pyautogui.locateOnScreen('./images/victory.png') == None:
                    self.wins.append(player)
                    end = time.time()
                    time_elapsed = end - start
                    if time_elapsed > 500:
                        break
                    print('Waiting',(time_elapsed))
                # Need to create a blacklist system for lost matches. 

                else:
                    print('game finished')
                    pyautogui.press('esc')
                    break
        else:
            return False

    def roam_and_fight(self):
        
        while (True):

            if self.arena_fight() == False:

                time.sleep(2)
                pyautogui.moveTo(self.CENTER_POSITION)
                mouse_position = pyautogui.position()
                pyautogui.dragTo(mouse_position[0], mouse_position[1] - 200, duration=2)

