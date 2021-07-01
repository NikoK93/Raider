import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np

screenWidth, screenHeight = pyautogui.size()

print(screenWidth, screenHeight)


def click_element(x, y):
    pyautogui.click(x, y)


def go_one_back():
    pyautogui.press('escape')

def get_market():
    pyautogui.locateOnScreen('./images/market.png')

#go_one_back()

def get_rewards():
    
    if pyautogui.locateOnScreen('./images/shop_free.png') != None:
        shop_location = pyautogui.locateOnScreen('./images/shop_free.png')
        lock = pyautogui.center(shop_location)
        click_element(lock[0], lock[1])
        time.sleep(2)
        if pyautogui.locateOnScreen('./images/mystery_shard.png') != None:
            # Get mystery shard if available
            mystery_location = pyautogui.locateOnScreen('./images/mystery_shard.png')
            lock = pyautogui.center(mystery_location)
            click_element(lock[0], lock[1])
            time.sleep(2)
            claim_location = pyautogui.locateOnScreen('./images/claim.png')
            lock = pyautogui.center(claim_location)
            click_element(lock[0], lock[1])

        elif pyautogui.locateOnScreen('./images/limited_offer.png') != None:
            offer_location = pyautogui.locateOnScreen('./images/limited_offer.png')
            lock = pyautogui.center(offer_location)
            click_element(lock[0], lock[1])

#get_rewards()
def match_all(image, template, threshold=0.8, debug=False, color=(0, 0, 255)):
        """ Match all template occurrences which have a higher likelihood than the threshold """
        width, height = template.shape[:2]
        match_probability = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
        match_locations = np.where(match_probability >= threshold)

        # Add the match rectangle to the screen
        locations = []
        for x, y in zip(*match_locations[::-1]):
            locations.append(((x, x + width), (y, y + height)))

            if debug:
                cv.rectangle(image, (x, y), (x + width, y + height), color, 1)
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
    if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
        location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
        lock = pyautogui.center(location)
        click_element(lock[0] + x_adj, lock[1] + y_adj)
        time.sleep(wait_time)

def get_position(image, conf=0.8, x_adj=0, y_adj=0):
    if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
        location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
        lock = pyautogui.center(location)
        return lock

def location_on_screen(image, conf=0.8):
    if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) == None:
        print('false')
        return False
    else:
        return True


def market_refresh():
    if pyautogui.locateOnScreen('./images/market_refresh.png', confidence=0.6) != None:
        locate_and_click("market_refresh")

def get_rewards():
    
    locate_and_click('shop_free')

    locate_and_click('limited_offer')

    locate_and_click('small_pack')

    locate_and_click('claim_free_gift')

    while location_on_screen('home_base') == False:
        go_one_back()
        time.sleep(2)

def to_clan_boss():

    locate_and_click('rsl')
    locate_and_click('battle', 0.7)
    click_and_drag('drag_x_clan_boss', x_adj=-400)
    locate_and_click('clan_boss_enter')
    click_and_drag('drag_y_clan_boss', y_adj=-400)
    click_and_drag('drag_y_clan_boss_2', y_adj=-400)


def click_and_drag(image, x_adj=0, y_adj=0):

    pos = get_position(image)
    pyautogui.moveTo(pos[0], pos[1])
    pyautogui.dragTo(pos[0] + x_adj, pos[1] + y_adj, duration=5)

def clanboss():
    # Go to clan boss
    #to_clan_boss()

    # Select difficulty
    #locate_and_click('UNM', conf=0.7)

    # Battle 1
    #locate_and_click('clan_boss_battle', conf=0.7)

    #disable auto
    #locate_and_click("start_on_auto_ON", x_adj=-100, conf=1)

    #locate_and_click('clan_boss_start', conf=0.9)
    # Select team
    #time.sleep(5)
    # Start fight
    # Roschard open with E
    locate_and_click('rsl')
    pyautogui.press('e')
    locate_and_click('confirm_2', conf=0.5, y_adj=50, wait_time=4)

    #frozen banshee opens with E
    pyautogui.press('e')
    locate_and_click('cb',conf=0.5,  wait_time=5)
    
    #septimus 
    #locate_and_click('rsl')
    pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # valkyrie AA
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    #mage
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    #Roschard
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # mage
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # mage
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    #rosch
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    #valkyrie
    #locate_and_click('rsl')
    #pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    #mage
    #locate_and_click('rsl')
    pyautogui.press('w')
    locate_and_click('confirm_2', conf=0.5, y_adj=50, wait_time=4)

    # banshee
    #locate_and_click('rsl')
    pyautogui.press('e')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # rosch
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # septimus
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # valkyrie
    #locate_and_click('rsl')
    pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # mage
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=10)
  
    # rosch
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)
     # banshee
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)
    
    # septi
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)

    # valkyrie
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)
    
    # rosch
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)
    
    # mage
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=10)
    
    # banshee
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)

    # septimus
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)
    
    # rosch
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5,  wait_time=5)

    # valkyrie
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5, wait_time=5)

    # mage
    #locate_and_click('rsl')
    pyautogui.press('w')
    locate_and_click('confirm_2', conf=0.5, y_adj=50, wait_time=5)
    
    # banshee
    #locate_and_click('rsl')
    locate_and_click('cb', conf=0.5, wait_time=5)

    # rosch
    #locate_and_click('rsl')
    pyautogui.press('a')
    locate_and_click('cb', conf=0.5, wait_time=5)

    pyautogui.press('a')
    locate_and_click('cb', conf=0.5, wait_time=5)
 
    #auto 
    #locate_and_click('rsl')
    locate_and_click('auto', conf=0.8)
    # Manual first few rounds

    # Click auto
    
#to_clan_boss()
#locate_and_click('UNM', conf=0.9)
#locate_and_click('clan_boss_battle', conf=0.9)
#locate_and_click("start_on_auto_ON", x_adj=-100)

clanboss()
#get_rewards()
#location_on_screen('home_base')

#market_refresh()
#locate_and_click("market_refresh", 0.5)