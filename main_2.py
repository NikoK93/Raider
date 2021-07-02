import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision

# initialize the WindowCapture class
wincap = WindowCapture('Raid: Shadow Legends')

vision_chracters = Vision('./images/mystery_2.jpg')

'''
# https://www.crazygames.com/game/guns-and-bottle
wincap = WindowCapture()
vision_gunsnbottle = Vision('gunsnbottle.jpg')
'''

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # display the processed image
    points = vision_chracters.find(screenshot, 0.5, 'rectangles')
    #points = vision_gunsnbottle.find(screenshot, 0.7, 'points')
    #cv.imshow('Computer Vision', screenshot)
    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #targets = Vision.get_click_points(detector.rectangles)
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')