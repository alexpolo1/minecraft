import subprocess
import time
import pyautogui
from PIL import Image

def right_click(x, y):
    move_mouse(x, y)
    print("Performing right click.")
    subprocess.run(['xdotool', 'click', '3'])  # Right-click

def drag_slider(start_x, start_y, end_x, end_y):
    print("Dragging slider.")
    move_mouse(start_x, start_y)
    subprocess.run(['xdotool', 'mousedown', '1'])  # Left mouse button down
    move_mouse(end_x, end_y)
    subprocess.run(['xdotool', 'mouseup', '1'])  # Left mouse button up

def click(x, y):
    move_mouse(x, y)
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

def shift_click(x, y):
    print("Performing shift click.")
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

# finding minecraft window and exit menu screen
def focus_minecraft_window():
    print("Focusing Minecraft window...")
    subprocess.run(['xdotool', 'search', '--name', 'Minecraft*1.20.2 - Multiplayer (3rd-party-Server)', 'windowactivate', '--sync'])
    time.sleep(2)
    print("Pressing Esc...")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(2)

# starting trade with trader and going down in the trade list
def trade_actions():
    right_click(2725, 1203)
    time.sleep(3)
    drag_slider(2600, 1399, 2600, 1408)
    time.sleep(3)

    # Attempt to find the color
    print("Taking a screenshot for color search...")
    screenshot = pyautogui.screenshot()
    target_color = (222, 227, 114)  # The color to search for
    found_x, found_y = find_color_in_image(target_color, screenshot)

    # Click twice, using found coordinates or fallback if not found
    for _ in range(2):
        if found_x is not None and found_y is not None:
            print(f"Color found at ({found_x}, {found_y}). Clicking at this position.")
            click(found_x, found_y)
        else:
            print("Color not found on the screen. Using fallback coordinates.")
            click(2535, 1421)
        time.sleep(3)

    # Buy all XP with shift click - done twice
    for _ in range(2):
        click(found_x, found_y)
        shift_click(2994, 1105)
        time.sleep(3)

    # Exit trader
    print("Pressing 'Esc' key.")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(3)

    # Move to the next trader
    print("Holding 'D' key for a step.")
    subprocess.run(['xdotool', 'keydown', 'd'])
    time.sleep(0.45)  # Hold 'D' for 0.45 seconds
    subprocess.run(['xdotool', 'keyup', 'd'])
    time.sleep(3)


# Initial setup
focus_minecraft_window()

# Perform trading actions in a loop
for _ in range(40):  # Number of trades to perform
    trade_actions()