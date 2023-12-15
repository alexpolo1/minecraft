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
    webhook_url = 'https://discord.com/api/webhooks/1185180105287422052/Abdomr4QNsegWAg6so4vpdW8ohn6Y9Pnpk2debQRHCIeYsc8BSP3jKrDGM74Lxn7dTvF'
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
    trade_window_area = (835, 372, 836, 712)
    screenshot = ImageGrab.grab(bbox=trade_window_area)

    relative_x, relative_y = (0, 10)  # Adjust these values as needed
    try:
        r, g, b = screenshot.getpixel((relative_x, relative_y))[:3]
        if (r, g, b) == (137, 51, 24):  
            log_and_print("Trade window detected.")
            return True
        else:
            log_and_print("Trade window not detected.")
            return False
    except IndexError as e:
        log_and_print(f"Error in getting pixel data: {e}")
        return False

def trade_actions():
    middle_x, middle_y = 960, 531
    slider_top_x, slider_top_y = 835, 372
    slider_bottom_x, slider_bottom_y = 836, 712
    xp_x, xp_y = 787, 721

    right_click(middle_x, middle_y)
    time.sleep(1)

    if not check_trade_window():
        log_and_print("Trade window not detected. Stopping script.")
        return False

    drag_slider(slider_top_x, slider_top_y, slider_bottom_x, slider_bottom_y)
    time.sleep(3)

    # Add any additional actions needed here

    return True  # Indicate that the trade action was successful

print("Running this on Windows. Ensure Minecraft window is focused before continuing.")

for _ in range(40):  # Number of trades to perform
    result = trade_actions()
    if not result:
        break  # Stop the script if trade window is not detected
