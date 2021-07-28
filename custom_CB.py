import time
import pyautogui
from support_functions import locate_and_click, click_element, adjusted_click

def unm_custom_raid2():

    time.sleep(10)

    #dutches shield
    locate_and_click('rsl')
    pyautogui.press('w')
    adjusted_click(-108, 269)
    time.sleep(5)
    # hotatsu aa
    pyautogui.press('a') 
    adjusted_click(35, -26)
    time.sleep(10)
    
    # ROUND 2
    time.sleep(3)
    # Farakhin poison ---------------
    pyautogui.press('w') 
    adjusted_click(35, -26)
    time.sleep(5)
    
    # Vizier AA
    adjusted_click(35, -26)
    time.sleep(5)

    # Martyr AA
    adjusted_click(35, -26)
    time.sleep(5)

    # Lilithu AA
    adjusted_click(35, -26)
    time.sleep(5)

    # Hotatsu A3 ---------------
    pyautogui.press('e')
    adjusted_click(-108, 269)
    time.sleep(10)

    # ROUND 3

    # Farakhin Ally attack
    pyautogui.press('e') 
    adjusted_click(35, -26)
    time.sleep(10)
    
    # duthcess AA
    adjusted_click(35, -26)
    time.sleep(5)

    # vizier AA
    adjusted_click(35, -26)
    time.sleep(5)

    # Martyr A3
    pyautogui.press('e')
    adjusted_click(35, -26)
    time.sleep(5)

    # Hotatsu A2
    pyautogui.press('w')
    adjusted_click(35, -26)
    time.sleep(4)

    # ROUND 4


    # pyautogui.press('w') 
    locate_and_click('auto', conf=0.8)


def nm_custom_raid2():

    time.sleep(10)

    locate_and_click('rsl')
    #pyautogui.press('w')
    #adjusted_click(-108, 269)

    #dutches AA
    adjusted_click(35, -26)
    time.sleep(5)
    
    #bad el W 
    pyautogui.press('w')
    adjusted_click(-108, 269)
    time.sleep(5)
    #locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # Farakhin Ally attack
    pyautogui.press('e')
    adjusted_click(35, -26)
    time.sleep(5)

   
    locate_and_click('auto', conf=0.8)


def unm_custom():

    time.sleep(10)

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

    time.sleep(10)

    #Round 1
    #Roschard
    locate_and_click('rsl')
    adjusted_click(35, -26)
    time.sleep(5)

    # Support
    adjusted_click(35, -26)
    time.sleep(5)
    
    #banshee
    pyautogui.press('e')
    adjusted_click(35, -26)
    time.sleep(5)

    # Septimus
    pyautogui.press('w')
    adjusted_click(35, -26)
    time.sleep(5)

    # Valkyrie - CA
    pyautogui.press('w')
    adjusted_click(35, -26)
    time.sleep(10)

    #Round 2
    #Roschard
    adjusted_click(35, -26)
    time.sleep(5)

    # Support
    adjusted_click(35, -26)
    time.sleep(5)
    
    #banshee
    adjusted_click(35, -26)
    time.sleep(5)

    # Septimus
    adjusted_click(35, -26)
    time.sleep(5)

    # Roschard
    adjusted_click(35, -26)
    time.sleep(5)

    # Valkyrie 
    adjusted_click(35, -26)
    time.sleep(10)


    #Round 3
    #Support
    adjusted_click(35, -26)
    time.sleep(5)

    # Banshee
    adjusted_click(35, -26)
    time.sleep(5)
    
    #Roschard
    adjusted_click(35, -26)
    time.sleep(5)

    # Septimus
    adjusted_click(35, -26)
    time.sleep(5)

    # Roschard
    adjusted_click(35, -26)
    time.sleep(5)

    # Valkyrie 
    adjusted_click(35, -26)
    time.sleep(10)


    #Round 4
    #Support
    time.sleep(4)
    adjusted_click(35, -26)
    time.sleep(5)

    # Roschard - last move on manual
    adjusted_click(35, -26)
    time.sleep(5)
    
    #auto 
    #locate_and_click('rsl')
    locate_and_click('auto', conf=0.8)