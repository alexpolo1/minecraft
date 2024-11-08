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
    webhook_url = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    log_and_print(f"Posted to Discord: {message}")

def right_click(x, y):
    pyautogui.moveTo(x, y)
    log_and_print(f"Performing right click at ({x}, {y}).")
    pyautogui.rightClick()

def drag_slider(start_x, start_y, end_x, end_y):
    log_and_print(f"Dragging slider from ({start_x}, {start_y}) to ({end_x}, {end_y}).")
    pyautogui.mouseDown(start_x, start_y, button='left')
    pyautogui.moveTo(end_x, end_y, duration=2)
    pyautogui.mouseUp(button='left')

def click(x, y):
    pyautogui.moveTo(x, y)
    log_and_print(f"Performing left click at ({x}, {y}).")
    pyautogui.click()

def shift_click(x, y):
    log_and_print(f"Performing shift click at ({x}, {y}).")
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
    screenshot.save("debug_trade_window.png")  # Save screenshot for debugging
    r, g, b = screenshot.getpixel((51, 69))[:3]
    log_and_print(f"Color at check position: {r}, {g}, {b}")
    if (r, g, b) == (137, 51, 24):
        log_and_print("Trade window detected.")
        return True
    else:
        log_and_print("Trade window not detected.")
        return False

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("Starting now!")

def trade_actions():
    right_click(2725, 1203)
    time.sleep(1)

    if not check_trade_window():
        log_and_print("Trade window not detected. Stopping script.")
        return False

    drag_slider(2600, 1399, 2600, 1408)
    time.sleep(3)

    log_and_print("Taking a screenshot for color search...")
    screenshot = ImageGrab.grab()
    screenshot.save("debug_color_search.png")  # Save screenshot for debugging
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
        shift_click(2994, 1105)
        time.sleep(1)
        post_to_discord("Potion clicked.")

    log_and_print("Pressing 'Esc' key.")
    pyautogui.press('esc')
    time.sleep(1)

    log_and_print("Holding 'D' key for a step.")
    pyautogui.keyDown('d')
    time.sleep(0.45)  # Hold 'D' for 0.45 seconds
    pyautogui.keyUp('d')
    time.sleep(1)

    return True  # Indicate that the trade action was successful

# 5-second countdown before the script starts
countdown(5)

for _ in range(40):  # Number of trades to perform
    result = trade_actions()
    if not result:
        break  # Stop the script if trade window is not detected
