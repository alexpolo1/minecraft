import requests
import pyautogui
import time
from PIL import ImageGrab
import logging

# Setup logging
logging.basicConfig(filename='minecraft_automation_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def log_and_print(message):
    print(message)
    logging.info(message)

def post_to_discord(message):
    webhook_url = 'https://discord.com/api/webhooks/1171735460729606145/Fyls4_uD7it29TNo7LktQFynb3k1K-BHLx9Y4WqzDK806o1_bVTNz94JNc996kDi-jE6'
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    log_and_print(f"Posted to Discord: {message}")

def right_click(x, y):
    pyautogui.moveTo(x, y)
    log_and_print("Performing right click.")
    pyautogui.rightClick()

def drag_slider(start_x, start_y, end_x, end_y):
    log_and_print("Dragging slider.")
    pyautogui.mouseDown(start_x, start_y, button='left')
    pyautogui.moveTo(end_x, end_y, duration=2)
    pyautogui.mouseUp(button='left')

def click(x, y):
    pyautogui.moveTo(x, y)
    log_and_print("Performing left click.")
    pyautogui.click()

def shift_click(x, y):
    log_and_print("Performing shift click.")
    pyautogui.keyDown('shift')
    click(x, y)
    pyautogui.keyUp('shift')

def find_color_in_image(target_color, image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y))[:3] == target_color:
                return x, y
    return None, None

def check_trade_window():
    log_and_print("Checking for trade window...")
    trade_window_area = (2314, 974, 3124, 1455)
    screenshot = ImageGrab.grab(trade_window_area)
    r, g, b = screenshot.getpixel((51, 69))[:3]
    if (r, g, b) == (137, 51, 24):
        log_and_print("Trade window detected.")
        return True
    else:
        log_and_print("Trade window not detected. Adjusting position.")
        adjustment_combinations = [('a', 0.1), ('d', 0.1), ('a', 0.2), ('d', 0.2)]
        for _ in range(5):  # Try up to three times
            for key, duration in adjustment_combinations:
                pyautogui.keyDown(key)
                time.sleep(duration)
                pyautogui.keyUp(key)
                time.sleep(0.1)
                right_click(2725, 1203)  # Right-click without moving the mouse
                time.sleep(3)
                screenshot = ImageGrab.grab(trade_window_area)
                r, g, b = screenshot.getpixel((51, 69))[:3]
                if (r, g, b) == (137, 51, 24):
                    log_and_print("Trade window detected after adjustment.")
                    return True

        log_and_print("Trade window not found after adjustments.")
        post_to_discord("Trade window not found.")
        return False

def trade_actions():
    right_click(2725, 1203)
    time.sleep(1)

    if not check_trade_window():
        log_and_print("Trade window not detected after adjustments. Stopping script.")
        return False

    drag_slider(2600, 1399, 2600, 1408)
    time.sleep(3)

    log_and_print("Taking a screenshot for color search...")
    screenshot = ImageGrab.grab()
    target_color = (222, 227, 114)  # The color to search for
    found_x, found_y = find_color_in_image(target_color, screenshot)

    for _ in range(2):
        if found_x is not None and found_y is not None:
            log_and_print(f"Color found at ({found_x}, {found_y}). Clicking at this position.")
            click(found_x, found_y)
        else:
            log_and_print("Color not found on the screen. Using fallback coordinates.")
            click(2535, 1421)
        time.sleep(1)

    for _ in range(2):
        click(found_x, found_y)
        shift_click(2994
