import pyautogui
import cv2 as cv
from PIL import ImageGrab
from functools import partial
import time
import numpy as np
import win32gui



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

def get_difference():

    while True:
        mouse_location = pyautogui.position()

        center = get_center()

        time.sleep(2)
        difference = center[0] - mouse_location[0], center[1] - mouse_location[1]
        print(difference)
