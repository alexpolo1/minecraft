import requests
import subprocess
import time
import pyautogui
from PIL import Image, ImageGrab
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
    move_mouse(x, y)
    log_and_print("Performing right click.")
    subprocess.run(['xdotool', 'click', '3'])  # Right-click

def drag_slider(start_x, start_y, end_x, end_y):
    log_and_print("Dragging slider.")
    move_mouse(start_x, start_y)
    subprocess.run(['xdotool', 'mousedown', '1'])  # Left mouse button down
    move_mouse(end_x, end_y)
    subprocess.run(['xdotool', 'mouseup', '1'])  # Left mouse button up

def click(x, y):
    move_mouse(x, y)
    log_and_print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

def shift_click(x, y):
    log_and_print("Performing shift click.")
    move_mouse(x, y)
    subprocess.run(['xdotool', 'keydown', 'shift', 'click', '1', 'keyup', 'shift'])  # Shift-click

def move_mouse(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y)])

def find_color_in_image(target_color, image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y))[:3] == target_color:
                return x, y
    return None, None

def focus_minecraft_window():
    log_and_print("Please click on the Minecraft window.")
    time.sleep(1)
    log_and_print("Starting in 3...")
    time.sleep(1)
    log_and_print("2...")
    time.sleep(1)
    log_and_print("1...")
    time.sleep(1)
    log_and_print("Script is now running.")
    return True

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
        for _ in range(5):  # Try up to five times
            for key, duration in adjustment_combinations:
                subprocess.run(['xdotool', 'keydown', key])
                time.sleep(duration)
                subprocess.run(['xdotool', 'keyup', key])
                time.sleep(0.1)
                subprocess.run(['xdotool', 'click', '3'])  # Right-click without moving the mouse
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
    log_and_print("Pressing 'Esc' key to ensure focus.")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(1)

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
        shift_click(2994, 1105)
        time.sleep(1)
        post_to_discord("Potion clicked.")

    log_and_print("Pressing 'Esc' key.")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(1)

    log_and_print("Holding 'D' key for a step.")
    subprocess.run(['xdotool', 'keydown', 'd'])
    time.sleep(0.45)  # Hold 'D' for 0.45 seconds
    subprocess.run(['xdotool', 'keyup', 'd'])
    time.sleep(1)

    return True  # Indicate that the trade action was successful

# Main script execution
if not focus_minecraft_window():
    log_and_print("Minecraft window not detected. Stopping script.")
else:
    for _ in range(40):  # Number of trades to perform
        result = trade_actions()
        if not result:
            break  # Stop the script if trade window is not detected
