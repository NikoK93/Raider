import time
import pyautogui
from support_functions import locate_and_click, click_element, adjusted_click

def unm_custom_raid2():

    time.sleep(5)

    #dutches shield
    locate_and_click('rsl')
    pyautogui.press('w')
    adjusted_click(-108, 269)

    # hotatsu aa
    locate_and_click('cb',conf=0.5,  wait_time=5)
    
    # ROUND 2

    # Farakhin poison ---------------
    pyautogui.press('w') 
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # Vizier AA
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # Martyr AA
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # Lilithu AA
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # Hotatsu A3 ---------------
    pyautogui.press('e')
    adjusted_click(-108, 269)

    # ROUND 3

    # Farakhin Ally attack
    pyautogui.press('e') 
    locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # duthcess AA
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # vizier AA
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # Martyr A3
    pyautogui.press('e')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # Hotatsu A2
    pyautogui.press('w')
    locate_and_click('cb', conf=0.5,  wait_time=4)

    # ROUND 4

    # pyautogui.press('w') 
    locate_and_click('auto', conf=0.8)


def nm_custom_raid2():

    time.sleep(5)

    locate_and_click('rsl')
    #pyautogui.press('w')
    #adjusted_click(-108, 269)

    #dutches AA
    locate_and_click('cb',conf=0.5,  wait_time=5)
    
    #bad el W 
    pyautogui.press('w')
    adjusted_click(-108, 269)
    #locate_and_click('cb', conf=0.5,  wait_time=4)
    
    # Farakhin Ally attack
    pyautogui.press('e')
    adjusted_click(-108, 269)
    locate_and_click('cb', conf=0.5,  wait_time=4)

   
    locate_and_click('auto', conf=0.8)


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