import pyautogui
import chilimangoes
pyautogui.screenshot = chilimangoes.grab_screen
pyautogui.pyscreeze.screenshot = chilimangoes.grab_screen
pyautogui.size = lambda: chilimangoes.screen_size

screenWidth, screenHeight = pyautogui.size()

print(screenWidth, screenHeight)


def click_element(position):
    pyautogui.click(position)


def go_one_back():
    click_element((2500, 800))
    pyautogui.press('escape')

def get_market():
    pyautogui.locateOnScreen('./images/market.png')

go_one_back()