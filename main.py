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

from windowcapture_modified import WindowCapture as WCM
from windowcapture import WindowCapture
from vision import Vision
import pytesseract
tes_path = pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import timeit
import logging
from PIL import Image

screenWidth, screenHeight = pyautogui.size()

GAME_RESOLUTION = (1280, 720)

'''
Game settings -
Graphics Quality: Low
Frame Rate Limit: 60 FPS
Resolution 1280x720

'''


def open_raid():

    hwnd = win32gui.FindWindow(None, 'Raid: Shadow Legends')
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, 9)

    rect = win32gui.GetWindowRect(hwnd)
 
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    Center_x = x + (w/2)
    Center_y = y + (h/2)

    return Center_x, Center_y

CENTER_POSITION = open_raid()



def click_element(x, y):
    pyautogui.click(x, y)

def adjusted_click(x_adj, y_adj):

    x, y = CENTER_POSITION
    #print(x + x_adj, y + y_adj)
    click_element(x + x_adj, y + y_adj)


def adjusted_move(x_adj, y_adj):

    x, y = CENTER_POSITION
    #print(x + x_adj, y + y_adj)
    pyautogui.moveTo(x + x_adj, y + y_adj)

def get_position(image, conf=0.8, x_adj=0, y_adj=0):
    for i in range(5):
        print(f'Trying to locate {image}...{i}')
        if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
            location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
            lock = pyautogui.center(location)
            print(lock)
            return lock


def click_and_drag(image, x_adj=0, y_adj=0):

    for i in range(5):
        print(f'Trying to locate image...{i}')
        pos = get_position(image)
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.dragTo(pos[0] + x_adj, pos[1] + y_adj, duration=5)
        break



def go_to_base():

    '''
    Return the user from any point to the base of the game. 
    '''
    while (True):
        time.sleep(1)
        if pyautogui.locateOnScreen('./images/exit_game.png', confidence=0.7) != None:
            pyautogui.press('esc')
            print('Arrived at base')
            break
        else:
            pyautogui.press('esc')



def match_all(pic, threshold=0.8, debug=False, color=(0, 0, 255)):
        """ Match all template occurrences which have a higher likelihood than the threshold """
        image = pyautogui.screenshot()
        template = cv.imread('./images/{pic}'.format(screenshot_img))
        width, height = template.shape[:2]
        match_probability = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
        match_locations = np.where(match_probability >= threshold)

        # Add the match rectangle to the screen
        locations = []
        for x, y in zip(*match_locations[::-1]):
            locations.append(((x, x + width), (y, y + height)))

            if debug:
                cv.rectangle(image, (x, y), (x + width, y + height), color, 1)
        print(locations)
        return locations


def locate_on_screen(tpl_path):
    screenshot_img = 'locate_on_screen_image_{}.png'.format(time.time())
    pyautogui.screenshot('./images{}'.format(screenshot_img))

    img_rgb = cv.imread('./images/{}'.format(screenshot_img))
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(tpl_path, 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)

    # debug
    for pt in zip(*loc[::-1]):
        return (pt[0], pt[1],  w , h)

    return False



def locate_and_click(image, conf=0.8, x_adj=0, y_adj=0, wait_time = 3):
    for i in range(5):
        logging.warning(msg=f'Trying to locate {image}...{i}')
        print(f'Trying to locate {image}...{i}')
        if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
            location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
            lock = pyautogui.center(location)
            click_element(lock[0] + x_adj, lock[1] + y_adj)
            time.sleep(wait_time)
            break

def locate_all_and_click(image, conf=0.8, x_adj=0, y_adj=0, wait_time = 3):
    if pyautogui.locateAllOnScreen(f'./images/{image}.png', confidence=conf) != None:
        location = pyautogui.locateAllOnScreen(f'./images/{image}.png', confidence=conf)
        for loc in location:  
            lock = pyautogui.center(loc)
            click_element(lock[0] + x_adj, lock[1] + y_adj)
            locate_and_click('get_mystery', wait_time=0, conf=0.7)
            #time.sleep(wait_time)



def location_on_screen(image, conf=0.8):
    if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) == None:
        print('false')
        return False
    else:
        return True


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


    print('Done.')




def find_leveling_heroes(image):

    vision_chracters = Vision(f'./images/{image}.jpg')
    wincap = WindowCapture('Raid: Shadow Legends')
    
    #vision = Vision()
    
   

    
    
    while True:
        
    # get an updated image of the game
        screenshot = wincap.get_screenshot()
        
        # display the processed image
        
        points, location = vision_chracters.find(screenshot, 0.4, 'rectangles')
        #print(pytesseract.image_to_string(points))
        #print(points, location)

  

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

#find_leveling_heroes('char_2')

def deselect():

    adjusted_click(-339.0, 20.5)
    time.sleep(1)
    adjusted_click(-458, -91)
    time.sleep(1)
    adjusted_click(-343, -179)
    

def generate_cords():

    start_x = 245
    start_y = 293

    adjust = 100

    positions = []
    for i in range(30):
        positions.append((start_x, start_y))
        start_x-=adjust
    
    a = iter(positions)

    return a
        
    def training_data_utils(self):
        
        while True:
            user_input = input('Star')
            if user_input == 1:
                screen = self.hero_screenshot()
                
def add_leveling_heroes():
    
    #locate_and_click("market_refresh", conf=0.6)
    cords = generate_cords()

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
    
        if pyautogui.locateOnScreen('./images/empty_leveling_slot.png', confidence=0.7) == None:
            return True
  
    
    
    
    time.sleep(1)

    deselect()

    #locate_all_and_click('mystery_shard_market')
    #match_all('get_mystery')
    #click_and_drag('market_drag',  x_adj=0, y_adj=-200)
    #locate_all_and_click('mystery_shard_market')

    #go_to_base()#
#get_difference()

def leveling_loop():

        locate_and_click('start_leveling')

        while True:
            print('leveling champions')

            if pyautogui.locateOnScreen('./images/max_level.png', confidence=0.7) != None:
                pyautogui.press('esc')
                break
            else:
                locate_and_click('replay_leveling')
        

#leveling_loop()



def get_mine_gems():
    locate_and_click('mine')

def get_rewards():
    
    locate_and_click('shop_free')
    locate_and_click('mystery_shard')
    locate_and_click('claim')

    locate_and_click('limited_offer')
    locate_and_click('small_pack')
    locate_and_click('claim_free_gift')

    go_to_base()

def play_time_rewards():
    '''
    Collects all playtime rewards
    '''
    adjusted_click(550.0, 221.5)
    time.sleep(1)
    loc = pyautogui.locateOnScreen('./images/playtime_1.png', confidence=0.7)
    location = pyautogui.center(loc)
    click_element(location[0], location[1])

    pct = 1.06
    time.sleep(2)
    for i in range(5):
        click_element((location[0] * pct) , location[1])
        pct += 0.06
        time.sleep(2)

    go_to_base()

def adjusted_click(x_adj, y_adj):

    x, y = CENTER_POSITION
    click_element(x + x_adj, y + y_adj)

def to_minotaur(repeat=1):

    locate_and_click('rsl')
    # Battle location
    adjusted_click(505.0, 310.5)

    locate_and_click('dungeons', 0.7)

    mouse_position = pyautogui.position()
    pyautogui.dragTo(mouse_position[0]- 400, mouse_position[1], duration=5)
    locate_and_click('minotaur', 0.8)

    for i in range(100):
        pyautogui.scroll(-1)

    
    x,y = CENTER_POSITION
    time.sleep(1)
    click_element(x + 400, y +240)

    # Start battle
    locate_and_click('start_mino')

    while repeat >= 1:
        time.sleep(2)
        if pyautogui.locateOnScreen('./images/victory_general.png') == None:
            print(f'Waiting for game to finish, round {repeat}')
        else:
            repeat -= 1
            if repeat >= 1:
                locate_and_click('replay_mino')
            else:
                print('Finished games')
                go_to_base()
                break
    
def to_dragon(repeat=1):

    locate_and_click('rsl')
    # Battle location
    adjusted_click(505.0, 310.5)

    locate_and_click('dungeons', 0.7)

    mouse_position = pyautogui.position()
    pyautogui.dragTo(mouse_position[0]- 1000, mouse_position[1], duration=5)
    locate_and_click('dragon', 0.8)

    for i in range(100):
        pyautogui.scroll(-1)

    locate_and_click('dragon_25', 1)

    locate_and_click('dragon_start')

    while repeat >= 1:
        time.sleep(2)
        if pyautogui.locateOnScreen('./images/victory_general.png') == None:
            print(f'Waiting for game to finish, round {repeat}')
        else:
            repeat -= 1
            if repeat >= 1:
                locate_and_click('replay_mino')
            else:
                print('Finished games')
                go_to_base()
                break


def to_spider(repeat=1):

    victory = 0
    defeat = 0

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

    x,y = CENTER_POSITION
    time.sleep(1)
    click_element(x + 400, y +190)

    locate_and_click('dragon_start')

    while repeat >= 1:
        time.sleep(2)
        if pyautogui.locateOnScreen('./images/replay_spider.png') == None:
            print(f'Waiting for the game to finish, round: {repeat}. Win/loss: {victory}-{defeat}')
        else:
            if pyautogui.locateOnScreen('./images/victory_spider.png', confidence=0.9) != None:
                victory +=1

            elif pyautogui.locateOnScreen('./images/defeat_spider.png', confidence=0.9) != None:
                defeat +=1

            repeat -= 1
            if repeat >= 1:
                locate_and_click('replay_spider')
            else:
                print('Finished games')
                go_to_base()
                break


def to_clan_boss(difficulty = 'UNM'):

    # Make sure that user is at base
    

    locate_and_click('rsl')
    locate_and_click('battle', 0.6)
    mouse_position = pyautogui.position()
    pyautogui.moveTo(mouse_position[0], mouse_position[1] - 200)
    time.sleep(1)
    pyautogui.dragTo(mouse_position[0]- 400, mouse_position[1], duration=5)

    
    locate_and_click('clan_boss_enter')
    mouse_position = pyautogui.position()
    pyautogui.dragTo(mouse_position[0], mouse_position[1] - 400, duration=5)

    if difficulty == 'UNM':
        locate_and_click('UNM', conf=0.7)   
        locate_and_click('clan_boss_battle', conf=0.7)
        locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
        locate_and_click('team_setup', conf=0.9)
        locate_and_click('team_UNM', conf=0.9, x_adj=-250)
        pyautogui.press('esc')
        locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
        locate_and_click('clan_boss_start', conf=0.9)

        unm_custom()
        while True:
            if pyautogui.locateOnScreen('./images/cb_replay.png') != None:
                locate_and_click('cb_replay', conf=0.9)
                unm_custom()
                break
            time.sleep(20)

    elif difficulty == 'NM':
        locate_and_click('NM', conf=0.9)  
        locate_and_click('clan_boss_battle', conf=0.9)
        locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
        locate_and_click('team_setup_nm', conf=0.9)
        locate_and_click('team_NM', conf=0.9, x_adj=-250)
        pyautogui.press('esc')
        locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
        locate_and_click('clan_boss_start', conf=0.9)

        nightmare_custom()

    #time.sleep(900)



def to_leveling():

    locate_and_click('rsl')
    # Battle location
    adjusted_click(505.0, 310.5)
    locate_and_click('to_leveling', 0.6)


def arena_fight():
    
    if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:
        locate_and_click('classic_arena_battle')
        if pyautogui.locateOnScreen('./images/confirm_arena_token.png') != None:
            locate_and_click("confirm_arena_token")
            locate_and_click('classic_arena_battle')

        locate_and_click('classic_arena_start')
        start = time.time()
        while (True):
            time.sleep(2)
            if pyautogui.locateOnScreen('./images/defeat.png') != None:
                print('Lost game, regresing list')
                pyautogui.press('esc')
                time.sleep(1)
                locate_and_click('refresh_arena_classic')
               
                break
            elif pyautogui.locateOnScreen('./images/victory.png') == None:
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

def roam_and_fight():
    

    while (True):
        if arena_fight() == False:

            pyautogui.moveTo(CENTER_POSITION)
            mouse_position = pyautogui.position()
            pyautogui.dragTo(mouse_position[0], mouse_position[1] - 200, duration=2)


    for i in range(100):
        pyautogui.scroll(-1)


def go_to_tavern():

    # Champions location
    adjusted_click(332, 316)
    time.sleep(2)
    # Tavern location
    adjusted_click(179, 224)
    time.sleep(2)
    # Remove hero
    adjusted_click(213, -260)
    time.sleep(2)
    x, y = CENTER_POSITION
    pyautogui.moveTo(x - 500, y)
    time.sleep(1)
    #pyautogui.dragTo((x - 500), y - 400, duration=3)
    for i in range(100):
        pyautogui.scroll(-1)
    
def upgrade_armor():

    # Champions location
    adjusted_click(332, 316)
    time.sleep(2)

def go_to_arena(type = 'classic'):

    locate_and_click('rsl')
    locate_and_click('battle', 0.6)
    locate_and_click('arena')
    if type == 'classic':
        locate_and_click('classic_arena')
    else:
        locate_and_click('tag_arena')
 
    roam_and_fight()

def daily_quests_collect():

    # Quests location
    adjusted_click(-248, 316)

    time.sleep(2)
    while pyautogui.locateOnScreen('./images/claim_daily.png') != None:
        locate_and_click('claim_daily')


def daily_quests():

    go_to_arena()

    #go_to_tavern()

def routine():

    get_mine_gems()

    get_rewards()

    play_time_rewards()

    daily_quests_collect()



#daily_quests()
#from arena import Arena
#arena = Arena()

#arena.go_to_arena()

#get_difference()
#go_to_tavern()
#daily_quests_collect()
#open_raid()
#to_clan_boss('UNM', repeat=2)
#to_dragon(repeat=100)
#to_minotaur(repeat=1)
#go_to_base()
#to_minotaur(repeat=30)
#to_dragon()
#go_to_arena()
#to_spider(100)
#locate_and_click('mino_15', x_adj=-200, conf=0.9)

#x, y = CENTER_POSITION
#print(x, y)
#pyautogui.moveTo(x + 400,y +240)
#to_clan_boss(difficulty='UNM')
#while True:
#    time.sleep(2)
#    print(pyautogui.position())