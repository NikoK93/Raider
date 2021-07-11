import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui
import datetime


def get_center():

    # Return the center of the application window

    hwnd = win32gui.FindWindow(None, 'Raid: Shadow Legends')
    rect = win32gui.GetWindowRect(hwnd)
 
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    Center_x = x + (w/2)
    Center_y = y + (h/2)

    return Center_x, Center_y

CENTER_POSITION = get_center()

def get_difference():

    while True:
        mouse_location = pyautogui.position()

        center = get_center()

        time.sleep(2)
        difference = center[0] - mouse_location[0], center[1] - mouse_location[1]
        print(difference)

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

def locate_and_click(image, conf=0.8, x_adj=0, y_adj=0, wait_time = 3):
    for i in range(5):
        time.sleep(1)
        print(f'Trying to locate {image}...{i}')
        if pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf) != None:
            location = pyautogui.locateOnScreen(f'./images/{image}.png', confidence=conf)
            lock = pyautogui.center(location)
            click_element(lock[0] + x_adj, lock[1] + y_adj)
            time.sleep(wait_time)
            break


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

def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 


#get_difference()