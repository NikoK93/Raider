import pyautogui
import time

def locate_and_click(image, conf=0.8, x_adj=0, y_adj=0, wait_time = 3):
    for i in range(5):
        print(f'Trying to locate image...{i}')
        if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
            location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
            lock = pyautogui.center(location)
            click_element(lock[0] + x_adj, lock[1] + y_adj)
            time.sleep(wait_time)
            break

def click_element(x, y):
    pyautogui.click(x, y)
        
def unm_custom():

    time.sleep(5)

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

    #auto 
    #locate_and_click('rsl')
    locate_and_click('auto', conf=0.8)
    # Manual first few rounds

    # Click auto

def nightmare_custom():

    time.sleep(5)

    #Round 1
    #Roschard
    locate_and_click('rsl')
    locate_and_click('cb', conf=0.6,  wait_time=4)

    # Support
    locate_and_click('cb', conf=0.6,  wait_time=4)
    
    #banshee
    pyautogui.press('e')
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Septimus
    pyautogui.press('w')
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Valkyrie - CA
    pyautogui.press('w')
    locate_and_click('cb',conf=0.6,  wait_time=10)

    #Round 2
    #Roschard
    locate_and_click('cb', conf=0.6,  wait_time=4)

    # Support
    locate_and_click('cb', conf=0.6,  wait_time=4)
    
    #banshee
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Septimus
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Roschard
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Valkyrie 
    locate_and_click('cb',conf=0.6,  wait_time=10)


    #Round 3
    #Support
    locate_and_click('cb', conf=0.6,  wait_time=4)

    # Banshee
    locate_and_click('cb', conf=0.6,  wait_time=4)
    
    #Roschard
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Septimus
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Roschard
    locate_and_click('cb',conf=0.6,  wait_time=4)

    # Valkyrie 
    locate_and_click('cb',conf=0.6,  wait_time=5)


    #Round 4
    #Support
    locate_and_click('cb', conf=0.6,  wait_time=4)

    # Roschard - last move on manual
    locate_and_click('cb', conf=0.6,  wait_time=4)
    
    #auto 
    #locate_and_click('rsl')
    locate_and_click('auto', conf=0.8)