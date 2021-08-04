import time
import pyautogui
from support_functions import locate_and_click, click_element, adjusted_click

def nightmare_custom():

    time.sleep(10)

    #Round 1
    #Roschard
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
    
    time.sleep(4)
    adjusted_click(35, -26)
    time.sleep(5)

    # Roschard - last move on manual
    adjusted_click(35, -26)
    time.sleep(5)
    #auto 
    #locate_and_click('rsl')
    locate_and_click('auto', conf=0.8)