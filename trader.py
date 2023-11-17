import pyautogui
import cv2
import numpy as np
import time

def find_on_screen(template, threshold=0.8):
    screen = np.array(pyautogui.screenshot())
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if loc[0].size:
        return loc[1][0], loc[0][0]
    return None

def load_images():
    images = {
        'cleric': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/cleric.png', 0),
        'trade_window_top': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/trade_window_top.png', 0),
        'trade_window_bottom': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/trade_window_bottom.png', 0),
        'trade_window_potion_click': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/trade_window_potion_click.png', 0),
        'shift_click_potion': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/shift_click_potion.png', 0),
        'trade_blocked': cv2.imread('/home/alex/minecraft/pybot/screenshot_folder/trade_blocked.png', 0)
    }
    return images


def right_click(pos):
    pyautogui.rightClick(pos)

def drag_slider(top_pos, bottom_pos):
    pyautogui.moveTo(top_pos)
    pyautogui.dragTo(bottom_pos, duration=1)

def click(pos):
    pyautogui.click(pos)

def shift_click(pos):
    pyautogui.keyDown('shift')
    click(pos)
    pyautogui.keyUp('shift')

images = load_images()
cleric_pos = find_on_screen(images['cleric'])
if cleric_pos:
    right_click(cleric_pos)
    time.sleep(1)  # Wait for the trade window to open

    # Drag the trade window slider from top to bottom
    top_pos = find_on_screen(images['trade_window_top'])
    bottom_pos = find_on_screen(images['trade_window_bottom'])
    if top_pos and bottom_pos:
        drag_slider(top_pos, bottom_pos)

    # Click on the potion trade
    potion_pos = find_on_screen(images['trade_window_potion_click'])
    if potion_pos:
        click(potion_pos)

    # Shift-click on the potion in the player's inventory
    shift_click_pos = find_on_screen(images['shift_click_potion'])
    if shift_click_pos:
        shift_click(shift_click_pos)

    # Check if the trade is blocked
    if find_on_screen(images['trade_blocked']):
        print("Trade done")
