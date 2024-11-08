import subprocess
import time
import pyautogui
import requests

def log_and_print(message):
    print(message)
    # Add logging here if needed

def post_to_discord(message):
    webhook_url = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    log_and_print(f"Posted to Discord: {message}")

def focus_minecraft_window():
    log_and_print("Focusing Minecraft window...")
    # Replace with the exact window title of your Minecraft game
    subprocess.run(['xdotool', 'search', '--name', 'Minecraft*1.20.2 - Multiplayer (3rd-party Server)', 'windowactivate', '--sync'])
    time.sleep(1)
    log_and_print("Minecraft window focused.")
    pyautogui.click()  # Left-click to capture the game window


def shift_click(x, y):
    log_and_print(f"Performing shift click at ({x}, {y}).")
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.keyDown('shift')
    pyautogui.click()
    pyautogui.keyUp('shift')

# Coordinates for the inventory slots
inventory_coords = [
    (2511, 1243), (2561, 1247), (2619, 1246), (2668, 1246), (2721, 1247),
    (2776, 1248), (2832, 1248), (2887, 1248), (2943, 1246),
    (2940, 1294), (2886, 1299), (2833, 1303), (2775, 1302), (2720, 1305),
    (2666, 1309), (2617, 1304), (2553, 1304), (2506, 1305),
    (2503, 1350), (2556, 1350), (2620, 1350), (2673, 1352), (2734, 1354),
    (2772, 1354), (2830, 1353), (2885, 1351), (2939, 1353),
    (2942, 1422), (2886, 1422), (2833, 1423), (2771, 1419), (2717, 1421),
    (2663, 1421), (2608, 1421), (2557, 1422), (2503, 1419) ]

# Coordinate for the crafting window
crafting_window_coord = (2855, 1099)

def shift_click_inventory_slots():
    for i in range(0, len(inventory_coords), 9):
        for coord in inventory_coords[i:i+9]:
            shift_click(*coord)
            time.sleep(0.25)

        shift_click(*crafting_window_coord)
        time.sleep(0.25)

# Main execution
crafted_item = input("Enter the item being crafted: ")
focus_minecraft_window()
shift_click_inventory_slots()
final_message = f"Crafted 256 {crafted_item}(s)."
log_and_print(final_message)
post_to_discord(final_message)
