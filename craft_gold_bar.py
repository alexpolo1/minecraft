import pyautogui
import time
from PIL import ImageGrab
import logging

# Setup logging
logging.basicConfig(filename='gold_bar_crafting_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def log_and_print(message):
    print(message)
    logging.info(message)

def click(x, y):
    pyautogui.moveTo(x, y, duration=0.2)
    log_and_print(f"Performing left click at ({x}, {y}).")
    pyautogui.click()

def find_color_in_image(target_color, search_area):
    screenshot = ImageGrab.grab(search_area)
    width, height = screenshot.size
    for x in range(width):
        for y in range(height):
            if screenshot.getpixel((x, y))[:3] == target_color:
                # Adjusting coordinates relative to the whole screen
                return x + search_area[0], y + search_area[1]
    return None, None

def craft_gold_bars():
    log_and_print("Looking for yellow gold bars to craft...")
    gold_bar_color = (255, 204, 0)  # This color might need adjustment
    crafting_area = (100, 100, 800, 600)  # Define your game's crafting area
    
    gold_bar_x, gold_bar_y = find_color_in_image(gold_bar_color, crafting_area)
    if gold_bar_x is not None and gold_bar_y is not None:
        log_and_print(f"Gold bar found at ({gold_bar_x}, {gold_bar_y}). Initiating crafting sequence.")
        click(gold_bar_x, gold_bar_y)  # Click on the gold bar
        # Add more actions here to perform the crafting, such as clicking on a crafting tool or station
    else:
        log_and_print("Gold bar not found within the specified area.")

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Starting in {i} seconds...", end="\r")
        time.sleep(1)
    print("Starting now!")

# 5-second countdown before the script starts
countdown(5)

# Define the number of attempts or use a condition to keep crafting
for _ in range(10):  # Adjust based on how many times you want to attempt crafting
    craft_gold_bars()
    time.sleep(5)  # Wait time between crafting attempts
