import pyautogui
import time
from PIL import Image

def find_color_in_image(target_color, image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y))[:3] == target_color:
                return x, y
    return None, None

print("Move the mouse to the start position. Waiting for 10 seconds...")
time.sleep(10)

mouse_x, mouse_y = pyautogui.position()
initial_color = pyautogui.pixel(mouse_x, mouse_y)
print(f"Initial Color at ({mouse_x}, {mouse_y}): {initial_color}")

print("Taking a screenshot for color search...")
screenshot = pyautogui.screenshot()
print("waiting 5 seconds before looking")
time.sleep(5)

found_x, found_y = find_color_in_image(initial_color, screenshot)
if found_x is not None:
    print(f"Color found at ({found_x}, {found_y}). Moving mouse to this position.")
    pyautogui.moveTo(found_x, found_y)
else:
    print("Color not found on the screen.")
