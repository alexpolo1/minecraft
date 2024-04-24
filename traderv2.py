import requests
import subprocess
import time
from PIL import Image, ImageGrab
import logging
print("")
# Setup logging
logging.basicConfig(filename='minecraft_automation_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

left_side_trade_window_area = (2314, 992, 2616, 1465)  # Defined area for trader's side
screenshot = ImageGrab.grab(left_side_trade_window_area)
xp_potion_color = (238, 231, 153)  # XP potion color
red_x_color = (186, 55, 15)  # Red 'X' color
red_x_areas = [(2505, 1424), (2898, 1122)]  # Coordinates where the red 'X' can appear
# Number of attempts to retry starting a new trade if a trader is blocked
max_retry_attempts = 5
successful_trades = 0


def log_and_print(message):
    print(message)
    logging.info(message)

def post_to_discord(message):
    webhook_url = 'https://discord.com/api/webhooks/1191486208895877150/-pxqBZs6RSUOBFFhPH8SwelQoaU5MEU9XX28fmp90EqNM0G98qkkZxsXfRxu7nN2Ze1X'
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

def shift_click():
    x, y = 2990, 1121  # Hardcoded coordinates for the shift-click action
    subprocess.run(['xdotool', 'keyup', 'Super_L', 'Super_R'])
    log_and_print("Performing shift click.")
    move_mouse(x, y)  # Ensure the mouse moves to the right coordinates before clicking
    time.sleep(1)  # Added delay before pressing shift
    subprocess.run(['xdotool', 'keydown', 'shift'])
    time.sleep(1)  # Added delay to ensure shift is held down
    log_and_print("Clicking at ({}, {})".format(x, y))
    subprocess.run(['xdotool', 'click', '1'])  # Perform the click
    time.sleep(1)  # Added delay before releasing shift
    subprocess.run(['xdotool', 'keyup', 'shift'])

def trade_fallback():
    log_and_print("Initiating fallback trading sequence.")
    # First fallback potion
    log_and_print("Buying fallback potion at first preset coordinates.")
    click(2552, 1433)  # Click on the fallback potion position
    time.sleep(2)  # Allow time for the GUI to respond
    shift_click()  # Confirm the purchase
    log_and_print("First fallback potion transaction attempted.")
    # Second fallback potion (if needed)
    log_and_print("Buying fallback potion at second preset coordinates.")
    click(2551, 1365)  # Click on the second fallback potion position
    time.sleep(2)  # Allow time for the GUI to respond
    shift_click()  # Confirm the purchase
    log_and_print("Second fallback potion transaction attempted.")
    log_and_print("Fallback trading actions completed.")


def finish_trading():
    # Exiting the trade window by sending the 'Escape' key
    log_and_print("Exiting trade window.")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(1)  # Brief delay to ensure the action has been processed
    # Logging and updating trade success count
    log_and_print("Trade completed. Moving to the next trader, good trade +1.")
    global successful_trades
    successful_trades += 1  # Increment success count
    # Move slightly to prepare for interaction with the next trader
    log_and_print("Adjusting position to face the next trader.")
    subprocess.run(['xdotool', 'keydown', 'a'])  # Simulate pressing 'a' to move left
    time.sleep(0.35)  # Hold the key briefly to simulate a slight move
    subprocess.run(['xdotool', 'keyup', 'a'])  # Release the key
    time.sleep(1)  # Wait a moment before the next action


def hold_key_for_duration(key, duration):
    log_and_print(f"Waiting 5 seconds before holding '{key}' key for {duration} seconds.")
    time.sleep(5)  # Delay for 5 seconds
    log_and_print(f"Holding '{key}' key.")
    subprocess.run(['xdotool', 'keydown', key])
    time.sleep(duration)
    subprocess.run(['xdotool', 'keyup', key])
    log_and_print(f"Released '{key}' key.")

def move_mouse(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y)])

def shift_double_click(x, y):
    move_mouse(x, y)
    subprocess.run(['xdotool', 'keydown', 'shift'])
    subprocess.run(['xdotool', 'click', '--repeat', '2', '--delay', '100', '1'])
    subprocess.run(['xdotool', 'keyup', 'shift'])

def fill_inventory_with_emeralds():
    log_and_print("Opening emerald chest...")
    right_click(1168, 306)
    time.sleep(2)  # Wait a moment for the chest to open
    cord1 = (2507, 977)
    cord2 = (2561, 975)
    log_and_print("Selecting emeralds...")
    click(cord1[0], cord1[1])  # Move to cord1 and left-click to select emeralds
    log_and_print("Transferring emeralds to inventory...")
    shift_double_click(cord2[0], cord2[1])  # Move to cord2 and shift-left-click to transfer emeralds
    time.sleep(1)
    log_and_print("Closing emmerald chest...")
    subprocess.run(['xdotool', 'key', 'Escape'])  # Press Esc to exit the chest
    time.sleep(1)

def move_first_trade():
    log_and_print("Moveing to first trade")
    # Prepare for the first trade
    subprocess.run(['xdotool', 'keydown', 'a'])
    time.sleep(0.25)
    subprocess.run(['xdotool', 'keyup', 'a'])
    time.sleep(1)

# TRADE ACTIONS !!  main function doing the trades and looking for red x as blocked trades
def trade_actions():
    global successful_trades
    trader_blocked = False  # Initialize as False
    attempts = 0
    found_x, found_y = None, None  # Initialize coordinates for XP potion
    time.sleep(1)
    if not check_trade_window():
        log_and_print("Trade window not detected after adjustments. Stopping script.")
        return False
    drag_slider(2599, 1071, 2598, 1419)
    time.sleep(3)
    log_and_print("Looking for XP potion")
    potion_bought = False  # Flag to check if potion is bought
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y))[:3] == xp_potion_color:
                found_x, found_y = x, y
                log_and_print(f"XP potion found at ({found_x}, {found_y}). Initiating purchase.")
                global_x = found_x + 2317  # Adjust for global positioning
                global_y = found_y + 994
                click(global_x, global_y)
                time.sleep(2)
                shift_click()
                log_and_print("XP potion bought.")
                potion_bought = True
                successful_trades += 1  # Increment the successful trades count
                finish_trading() 
                break
        if potion_bought:
            break
    # Use fallback if XP potion is not found
    if not potion_bought:
        trade_fallback()
        finish_trading()
        return False
    return True  # Indicates the trade actions completed successfully


def check_trade_window():
    log_and_print("Checking for trade window...")
    trade_window_area = (2317, 994, 3126, 1472)  # Defined area
    screenshot = ImageGrab.grab(trade_window_area)
    target_color = (178, 67, 32)  # Target color for trade window
    #use right click to check for trade window
    log_and_print("useing right click to check for trade window")
    right_click(1168, 306)
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if screenshot.getpixel((x, y))[:3] == target_color:
                log_and_print("Trade window detected.")
                return True
    log_and_print("Trade window not detected. Adjusting position.")
    adjustment_combinations = [('a', 0.1), ('d', 0.1), ('a', 0.2), ('d', 0.2)]
    for _ in range(5):
        for key, duration in adjustment_combinations:
            subprocess.run(['xdotool', 'keydown', key])
            time.sleep(duration)
            subprocess.run(['xdotool', 'keyup', key])
            time.sleep(0.1)
            subprocess.run(['xdotool', 'click', '3'])
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

def dump_xp_potions():
    log_and_print("Dumping XP potions into dump chest...")
    right_click(1168, 306)
    time.sleep(2)  # Wait a moment for the chest to open
    cord1 = (2508, 1342)
    cord2 = (2558, 1342)
    log_and_print("Selecting xp potions...")
    click(cord1[0], cord1[1])  # Move to cord1 and left-click to select emeralds
    log_and_print("Transferring xp potions to dump chest...")
    shift_double_click(cord2[0], cord2[1])  # Move to cord2 and shift-left-click to transfer emeralds
    log_and_print("Closing chest...")
    subprocess.run(['xdotool', 'key', 'Escape'])  # Press Esc to exit the chest
    time.sleep(1)


first_run = True  # Flag to check if it's the first run
def focus_minecraft_window():
    global first_run
    log_and_print("Focusing Minecraft window...")
    subprocess.run(['xdotool', 'search', '--name', 'Minecraft*3.20.2 - Multiplayer (3rd-party-Server)', 'windowactivate', '--sync'])
    time.sleep(2)

    if first_run:
        log_and_print("Pressing Esc (first run only)...")
        subprocess.run(['xdotool', 'key', 'Escape'])
        time.sleep(2)
        first_run = False  # Set the flag to False after the first run

def perform_trading_cycle():
    global successful_trades
    successful_trades = 0  # Reset count at the start of each cycle
    focus_minecraft_window()
    fill_inventory_with_emeralds()  # Fill up on emeralds before starting trades
    move_first_trade()

    # Define the number of trade attempts
    trade_attempts = 50

    for _ in range(trade_attempts):  # Loop for defined number of trades
        trade_successful = trade_actions()
        if not trade_successful:
            log_and_print(f"Trade attempt failed or blocked, continuing to next. Attempt {_ + 1} of {trade_attempts}")
        else:
            log_and_print(f"Trade attempt successful. Attempt {_ + 1} of {trade_attempts}")

        # Check if the number of successful trades reached the desired trades before moving to dump chest
        if successful_trades >= trade_attempts:
            break

    log_and_print("Moving to dump chest after trade attempts.")
    hold_key_for_duration('a', 25)  # Adjust the key and duration as needed
    dump_xp_potions()  # Dump XP potions after completing trades
    trade_summary = f"Trading session completed. Trades performed: {successful_trades}"
    post_to_discord(trade_summary)
    log_and_print("Cycle done, moving back to start.")
    hold_key_for_duration('d', 25)  # Adjust the key and duration as needed



# Main loop to run trading cycles and reset position
def main_loop():
    while True:
        log_and_print("starting trade cycle")
        perform_trading_cycle()
        log_and_print("cycle done waiting 5")
        time.sleep(5)  # Delay before next cycle starts

# Run the main loop
main_loop()
