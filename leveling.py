from numpy.lib.polynomial import _polyint_dispatcher
import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui

from windowcapture import WindowCapture
from vision import Vision

import pytesseract
tes_path = pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from support_functions import locate_and_click, adjusted_click, adjusted_move



class FindImage:

    def __init__(self, image, x_cut, y_cut):

    def find_images(image):

        vision_chracters = Vision(f'./images/{image}.jpg')
        wincap = WindowCapture('Raid: Shadow Legends')
        
        #vision = Vision()

        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        
        # display the processed image
        
        points, location = vision_chracters.find(screenshot, 0.4, 'rectangles')
        #print(pytesseract.image_to_string(points))
        #print(points, location)

        if location:

            # get's screen position
            x, y = location[0][0], location[0][1]
            x_, y_ = wincap.get_screen_position((x, y))
            # makes a screenshot based on the position
            im = pyautogui.screenshot(region=(x_, y_, location[0][2], location[0][3]))
            print(x, y)
            #print(type(im))
            #image_data = np.asarray(im)
            #img_1 = cv.resize(image_data, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
            #img_2 = cv.threshold(img_1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
            #print(type(img_2))
            
            #thresh = cv.threshold(image_data,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
            # ocr the text from the image
            text = pytesseract.image_to_string(im,  lang='eng')
            num = [el for el in text if el.isdigit()]
            #logging.warning(text)
            if num:
                if int(num[0]) == 1:
                    return num
                    


        #deselect champions by static position

        #print(num)
        #if text not in black_list:
        #    pyautogui.moveTo(x_+800, y_+50)
        #print(text)
        
    '''
    try:
        #x, y = points[0]
        #if points != None:
        #x_, y_ = wincap.get_screen_position((x, y))
        #adjusted_click(x, y)
        click_element(x_, y_)
    except:
        print('No points found...')

    '''
    #points = vision_gunsnbottle.find(screenshot, 0.7, 'points')
    #cv.imshow('Computer Vision', screenshot)
    # debug the loop rate

    #targets = Vision.get_click_points(detector.rectangles)
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses


      

    def find_leveling_heroes(image):

        vision_chracters = Vision(f'./images/{image}.jpg')
        wincap = WindowCapture('Raid: Shadow Legends', y_cut=500)
        
        #vision = Vision()
        
    

        
        time.sleep(1)
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        
        # display the processed image
        
        points, location = vision_chracters.find(screenshot, 0.4, 'rectangles')
        #print(pytesseract.image_to_string(points))
        #print(points, location)

        if location:

            # get's screen position
            x, y = location[0][0], location[0][1]
            x_, y_ = wincap.get_screen_position((x, y))
            # makes a screenshot based on the position
            #im = pyautogui.screenshot(region=(x_, y_, location[0][2], location[0][3]))
            print(x_, y_)
            try:
                return x_, y_
            except Exception:
                print('No cords')
            #return x_, y_
            #print(type(im))
            #image_data = np.asarray(im)
            #img_1 = cv.resize(image_data, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
            #img_2 = cv.threshold(img_1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
            #print(type(img_2))
            
            #thresh = cv.threshold(image_data,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
            # ocr the text from the image
        


            #deselect champions by static position

            #print(num)
            #if text not in black_list:
            #    pyautogui.moveTo(x_+800, y_+50)
            #print(text)
            
        '''
        try:
            #x, y = points[0]
            #if points != None:
            #x_, y_ = wincap.get_screen_position((x, y))
            #adjusted_click(x, y)
            click_element(x_, y_)
        except:
            print('No points found...')

        '''
        #points = vision_gunsnbottle.find(screenshot, 0.7, 'points')
        #cv.imshow('Computer Vision', screenshot)
        # debug the loop rate

        #targets = Vision.get_click_points(detector.rectangles)
        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses


        print('Done.')

class AutoLeveler():

    def __init__(self):
        pass
        
        self.leveling_state = False

    def generate_cords(self):

        start_x = 245
        start_y = 293

        adjust = 100

        positions = []
        for i in range(30):
            positions.append((start_x, start_y))
            start_x-=adjust
        
        a = iter(positions)

        return a

    def to_leveling():

        locate_and_click('rsl')
        # Battle location
        adjusted_click(505.0, 310.5)
        locate_and_click('to_leveling', 0.6)  
    
    def leveling_loop(self):

        locate_and_click('start_leveling')

        while self.leveling_state:
            print('leveling champions')

            if pyautogui.locateOnScreen('./images/max_level.png', confidence=0.7) != None:
                pyautogui.press('esc')
                break
            else:
                locate_and_click('replay_leveling')

    def deselect(self):

        adjusted_click(-339.0, 20.5)
        time.sleep(1)
        adjusted_click(-458, -91)
        time.sleep(1)
        adjusted_click(-343, -179)

    def add_leveling_heroes():
    
        #locate_and_click("market_refresh", conf=0.6)
        cords = self.generate_cords()

        while pyautogui.locateOnScreen('./images/empty_leveling_slot.png', confidence=0.7) != None:
            #x, y = find_leveling_heroes('char_2')
            
            #pyautogui.moveTo(x+20, y+20)
            x, y = next(cords)
            print(x, y)
            adjusted_move(x, y)
            time.sleep(1)
            pyautogui.mouseDown(duration=2)
            time.sleep(1)
            pyautogui.mouseUp()
            
            level = find_images('test_3')

            print(level)
            if level:
                if int(level[0]) == 1:
                    pyautogui.press('esc')
                    time.sleep(2)
                    adjusted_click(x, y)
                    #pyautogui.click()
        
            elif pyautogui.locateOnScreen('./images/empty_leveling_slot.png', confidence=0.7) != None:
                continue
            else:
                pyautogui.press('esc')
                time.sleep(2)
        
        
        
        time.sleep(1)

    #deselect()

    #locate_all_and_click('mystery_shard_market')
    #match_all('get_mystery')
    #click_and_drag('market_drag',  x_adj=0, y_adj=-200)
    #locate_all_and_click('mystery_shard_market')

    #go_to_base()#
#get_difference()
