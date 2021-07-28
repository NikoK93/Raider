import time
import pyautogui

from custom_CB import unm_custom, nightmare_custom, unm_custom_raid2, nm_custom_raid2
from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element



class ClanBoss():

    def __init__(self, difficulty, account):

        self.difficulty = difficulty
        self.account = account

    def to_clan_boss(self):

        # Make sure that user is at base
        go_to_base()

        locate_and_click('battle', 0.6)
        mouse_position = pyautogui.position()
        pyautogui.moveTo(mouse_position[0], mouse_position[1] - 200)
        time.sleep(1)
        pyautogui.dragTo(mouse_position[0]- 400, mouse_position[1], duration=5)

        
        locate_and_click('clan_boss_enter')
        mouse_position = pyautogui.position()
        pyautogui.dragTo(mouse_position[0], mouse_position[1] - 400, duration=5)

        if self.difficulty == 'UNM':
            locate_and_click('UNM', conf=0.7)   
            locate_and_click('clan_boss_battle', conf=0.7)
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('team_setup', conf=0.9)

            if self.account == 'raid3':
                locate_and_click('team_UNM', conf=0.9, x_adj=-250)
            elif self.account == 'raid2':
                locate_and_click('team_UNM_raid2', conf=0.9, x_adj=-250)

            pyautogui.press('esc')
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('clan_boss_start', conf=0.9)

            if self.account == 'raid3':
                unm_custom()
            elif self.account == 'raid2':
                unm_custom_raid2()

            while True:
                if pyautogui.locateOnScreen('./images/cb_replay.png') != None:
                    locate_and_click('cb_replay', conf=0.9)
                    if self.account == 'raid3':
                        unm_custom()
                    elif self.account == 'raid2':
                        unm_custom_raid2()
                    break
                time.sleep(20)

        elif self.difficulty == 'NM':
            locate_and_click('NM', conf=0.9)  
            locate_and_click('clan_boss_battle', conf=0.9)
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('team_setup', conf=0.9)

            if self.account == 'raid3':
                locate_and_click('team_NM', conf=0.9, x_adj=-250)
            elif self.account == 'raid2':
                locate_and_click('team_NM_raid2', conf=0.9, x_adj=-250)

            pyautogui.press('esc')
            locate_and_click("start_on_auto_ON", x_adj=-100, conf=0.9)
            locate_and_click('clan_boss_start', conf=0.9)

            if self.account == 'raid3':
                nightmare_custom()
            elif self.account == 'raid2':
                nm_custom_raid2()
            
