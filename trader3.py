import requests
import subprocess
import time
from PIL import Image
import logging
from wayland_screenshot import take_screenshot  # This will be a custom function you need to implement

# Setup logging
logging.basicConfig(filename='minecraft_automation_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def log_and_print(message):
    print(message)
    logging.info(message)

def post_to_discord(message):
    webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    log_and_print(f"Posted to Discord: {message}")

def right_click(x, y):
    move_mouse(x, y)
    log_and_print("Performing right click.")
    subprocess.run(['ydotool', 'click', '3'])  # Right-click

def drag_slider(start_x, start_y, end_x, end_y):
    log_and_print("Dragging slider.")
    move_mouse(start_x, start_y)
    subprocess.run(['ydotool', 'mousedown', '1'])  # Left mouse button down
    move_mouse(end_x, end_y)
    subprocess.run(['ydotool', 'mouseup', '1'])  # Left mouse button up

def click(x, y):
    move_mouse(x, y)
    log_and_print("Performing left click.")
    subprocess.run(['ydotool', 'click', '1'])  # Left-click

def shift_click(x, y):
    log_and_print("Performing shift click.")
    move_mouse(x, y)
    subprocess.run(['ydotool', 'keydown', 'Shift', 'click', '1', 'keyup', 'Shift'])  # Shift-click

def move_mouse(x, y):
    subprocess.run(['ydotool', 'mousemove', str(x), str(y)])

def find_color_in_image(target_color, image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y))[:3] == target_color:
                return x, y
    return None, None

def focus_minecraft_window():
    log_and_print("Focusing Minecraft window...")
    # Note: Focusing a specific window might not work in Wayland as it does in X11
    subprocess.run(['ydotool', 'search', '--name', 'Minecraft*3.20.2 - Multiplayer (3rd-party-Server)', 'windowactivate', '--sync'])
    time.sleep(2)
    log_and_print("Pressing Esc...")
    subprocess.run(['ydotool', 'key', 'Escape'])
    time.sleep(2)

def check_trade_window():
    log_and_print("Checking for trade window...")
    trade_window_area = (2314, 974, 3124, 1455)
    screenshot = take_screenshot(trade_window_area)  # This needs a custom implementation for Wayland
    r, g, b = screenshot.getpixel((51, 69))[:3]
    if (r, g, b) == (137, 51, 24):
        log_and_print("Trade window detected.")
        return True
    else:
        log_and_print("Trade window not detected. Adjusting position.")
        # Adjusting position might not work as expected in Wayland
        # This part needs to be tested and potentially adjusted
        # ...

def trade_actions():
    right_click(2725, 1203)
    time.sleep(1)

    if not check_trade_window():
        log_and_print("Trade window not detected after right click. Stopping script.")
        return False

    drag_slider(2600, 1399, 2600, 1408)
    time.sleep(3)

    log_and_print("Taking a screenshot for color search...")
    screenshot = take_screenshot()  # This needs a custom implementation for Wayland
    target_color = (222, 227, 114)  # The color to search for
    found_x, found_y = find_color_in_image(target_color, screenshot)

    if found_x is not None and found_y is not None:
        log_and_print(f"Color found at ({found_x}, {found_y}). Clicking at this position.")
        click(found_x, found_y)
    else:
        log_and_print("Color not found on the screen. Using fallback coordinates.")
        click(2535, 1421)
    time.sleep(1)

    for _ in range(2):
        shift_click(2994, 1105)
        time.sleep(1)
        post_to_discord("Potion clicked.")

    log_and_print("Pressing 'Esc' key.")
    subprocess.run(['ydotool', 'key', 'Escape'])
    time.sleep(1)

    log_and_print("Holding 'D' key for a step.")
    subprocess.run(['ydotool', 'keydown', 'd'])
    time.sleep(0.45)  # Hold 'D' for 0.45 seconds
    subprocess.run(['ydotool', 'keyup', 'd'])
    time.sleep(1)

    return True  # Indicate that the trade action was successful


focus_minecraft_window()

for _ in range(40):  # Number of trades to perform
    result = trade_actions()
    if not result:
        break  # Stop the script if trade window is not detected
