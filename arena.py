from numpy.random import randint
import pyautogui
import time
import numpy as np

from support_functions import locate_and_click, get_center, go_to_base, adjusted_click, click_element


class Arena():

    def __init__(self, arena_type):

        go_to_base()

        self.wins = 0
        self.STATE = 0
        self.refresh = False

        self.arena_type = arena_type


    def arena_fight(self):

        # Check if refresh avaliable and refresh opponents
        if self.refresh == False:
            try:
                locate_and_click('tag_arena_refresh')
                self.refresh = True
            except:
                print('Refresh not avaliable')
                
        
        # Find the battle location and click to begin
        if pyautogui.locateOnScreen('./images/classic_arena_battle.png', confidence=0.8) != None:
            locate_and_click('classic_arena_battle')
            time.sleep(1)

            # If pop-up for token refresh appears, confirm it
            if pyautogui.locateOnScreen('./images/confirm_arena_token.png') != None:
                locate_and_click("confirm_arena_token")
                #return False

            # Return False and set STATE to 0 if gem refill has appeared
            elif pyautogui.locateOnScreen('./images/classic_arena_refill.png') != None:
                print('No gem refills, aborting.')
                self.STATE = 0
                return False

            elif pyautogui.locateOnScreen('./images/tag_arena_gem.png') != None:
                print('No gem refills, aborting.')
                self.STATE = 0
                return False

            # Start the arena fight
            else:
                # Make sure auto is ON
                if pyautogui.locateOnScreen('./images/start_on_auto_OFF.png') != None:
                    locate_and_click("start_on_auto_OFF", x_adj=-100, conf=0.9)

                # Click start
                locate_and_click('classic_arena_start')

                # Time the battle 
                start = time.time()

                while self.STATE == 1:
                    
                    # Every two seconds
                    time.sleep(2)
                    
                    # Check for defeat
                    if pyautogui.locateOnScreen('./images/defeat_arena.png') != None:
                        print('Lost game.')
                        pyautogui.press('esc')
                        time.sleep(2)
                        if self.arena_type != 'classic':
                            pyautogui.press('esc')
                            time.sleep(1)
                            if pyautogui.locateOnScreen('./images/tag_arena_refresh.png'):
                                locate_and_click('tag_arena_refresh')
                                break
                        if pyautogui.locateOnScreen('./images/refresh_arena_classic.png') != None:
                            locate_and_click('refresh_arena_classic')
                            break
                        else:
                            self.STATE = 0
                            break

                    # Check for victory
                    elif pyautogui.locateOnScreen('./images/victory_arena.png') != None:
                        pyautogui.press('esc')
                        time.sleep(3)
                        if self.arena_type != 'classic':
                                pyautogui.press('esc')
                                time.sleep(1)
                        break

                    # Check wether game is going on for too long
                    else:
                        # Failsafe for potential infinite games i.e. apothecary
                        end = time.time()
                        time_elapsed = end - start
                        if time_elapsed > 1000:
                            if self.arena_type == "tag_arena":
                                time.sleep(2)
                                locate_and_click('skip_battle')
                                time.sleep(2)
                                locate_and_click('skip_battle_2')
                                
                                #self.STATE = 0
                                #return False
                            else:
                                pyautogui.press('esc')
                                time.sleep(2)
                                locate_and_click('leave_battle')
                                time.sleep(2)
                                locate_and_click('leave_battle_2')
                                time.sleep(2)
                                pyautogui.press('esc')
                                self.STATE = 0
                                return False

                        print(f'Waiting - {round(time_elapsed, 0)} seconds.')
    
                        
        # if arena battle button is not found, return False to scroll down    
        else:
            return False

    def roam_and_fight(self):
        
        while self.STATE == 1:
            if self.arena_fight() == False:
                x, y = get_center()
                pyautogui.moveTo(x, y)
                mouse_position = pyautogui.position()

                pyautogui.dragTo(mouse_position[0], mouse_position[1] - 200, duration=2)

        print('Arena done')

    def go_to_arena(self):
        
        # Battle location
        locate_and_click('battle', 0.6)

        # Arena location
        locate_and_click('arena')

        # Choose arena
        if self.arena_type == 'classic':
            locate_and_click('classic_arena')
        else:
            locate_and_click('tag_arena')

        # set bot to active
        self.STATE = 1

        # Begin main loop
        self.roam_and_fight()


    def get_scroll_parameters(self):
        
        rand_int = np.random.randint(1,100)
        rand_y = np.random.choice([1, -1], [0.3,0.7])

        return randint, rand_y