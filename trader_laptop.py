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
    webhook_url = 'https://discord.com/api/webhooks/1191486208895877150/-pxqBZs6RSUOBFFhPH8SwelQoaU5MEU9XX28fmp90EqNM0G98qkkZxsXfRxu7nN2Ze1Xe'
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
    subprocess.run(['xdotool', 'keyup', 'Super_L', 'Super_R'])
    log_and_print("Performing shift click.")
    move_mouse(x, y)
    time.sleep(0.5)  # Added delay before pressing shift
    subprocess.run(['xdotool', 'keydown', 'shift'])
    time.sleep(0.5)  # Added delay to ensure shift is held down
    subprocess.run(['xdotool', 'click', '1'])  # Left-click
    time.sleep(0.5)  # Added delay before releasing shift
    subprocess.run(['xdotool', 'keyup', 'shift'])


def move_mouse(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y)])

def focus_minecraft_window():
    log_and_print("Focusing Minecraft window...")
    subprocess.run(['xdotool', 'search', '--name', 'Minecraft*3.20.2 - Multiplayer (3rd-party-Server)', 'windowactivate', '--sync'])
    time.sleep(2)
    log_and_print("Pressing Esc...")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(2)


def check_trade_window():
    log_and_print("Checking for trade window...")
    trade_window_area = (896, 145, 11434, 460)  # Your defined area
    screenshot = ImageGrab.grab(trade_window_area)
    target_color = (195, 100, 64)  # Your target color

    # Iterate over each pixel in the trade window area
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y))[:3] == target_color:
                log_and_print("Trade window detected.")
                return True

    log_and_print("Trade window not detected. Adjusting position.")
    adjustment_combinations = [('a', 0.1), ('d', 0.1), ('a', 0.2), ('d', 0.2)]
    for _ in range(5):  # Try up to three times
        for key, duration in adjustment_combinations:
            subprocess.run(['xdotool', 'keydown', key])
            time.sleep(duration)
            subprocess.run(['xdotool', 'keyup', key])
            time.sleep(0.1)
            subprocess.run(['xdotool', 'click', '3'])  # Right-click without moving the mouse
            time.sleep(3)
            screenshot = ImageGrab.grab(trade_window_area)
            for x in range(screenshot.width):
                for y in range(screenshot.height):
                    if screenshot.getpixel((x, y))[:3] == target_color:
                        log_and_print("Trade window detected after adjustment.")
                        return True

    log_and_print("Trade window not found after adjustments.")
    post_to_discord("Trade window not found.")
    return False

trades_info = []  # List to store trade information

def trade_actions():
    global trades_info
    right_click(1168, 306)
    time.sleep(1)

    if not check_trade_window():
        log_and_print("Trade window not detected after adjustments. Stopping script.")
        return False

    drag_slider(1084, 199, 1084, 423)
    time.sleep(3)

    log_and_print("Taking a screenshot for color search...")
    screenshot = ImageGrab.grab()
    target_color = (103, 177, 125)  # The color to search for
    found_x, found_y = None, None

    # Iterate over each pixel to find the target color
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y))[:3] == target_color:
                found_x, found_y = x, y
                break
        if found_x is not None:
            break

    for _ in range(2):
        if found_x is not None and found_y is not None:
            log_and_print(f"Color found at ({found_x}, {found_y}). Clicking at this position.")
            click(found_x, found_y)
        else:
            log_and_print("Color not found on the screen. Using fallback coordinates.")
            click(1052, 436)
        time.sleep(1)

    for _ in range(2):
        click(found_x, found_y)
        shift_click(1346, 225)
        time.sleep(1)
        # Collect trade info
        trades_info.append("Potion clicked at position ({}, {})".format(found_x, found_y))

    log_and_print("Pressing 'Esc' key.")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(1)

    log_and_print("Holding 'D' key for a step.")
    subprocess.run(['xdotool', 'keydown', 'd'])
    time.sleep(0.45)  # Hold 'D' for 0.45 seconds
    subprocess.run(['xdotool', 'keyup', 'd'])
    time.sleep(1)

    return True  # Indicate that the trade action was successful

focus_minecraft_window()

for _ in range(25):  # Number of trades to perform
    result = trade_actions()
    if not result:
        break  # Stop the script if trade window is not detected

# Post the collection of trades to Discord
trade_summary = "\n".join(trades_info)
post_to_discord(f"Trading session completed. Summary:\n{trade_summary}")

