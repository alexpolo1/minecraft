import cv2
import numpy as np
from PIL import ImageGrab, Image
import subprocess
import time
import datetime
import os
import requests
import base64
from io import BytesIO
import pyautogui

# Ensure the temp screenshot directory exists
temp_screenshot_directory = '/tmp/mcscreens'
os.makedirs(temp_screenshot_directory, exist_ok=True)

# Your Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1171735460729606145/Fyls4_uD7it29TNo7LktQFynb3k1K-BHLx9Y4WqzDK806o1_bVTNz94JNc996kDi-jE6'

# Base64 encoded images for both buttons
encoded_images = {
    "back_to_server_list": b'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',
    "join": b'iVBORw0KGgoAAAANSUhEUgAAASkAAAA4CAYAAAChZA4IAAAAwnpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBBDgMhCLz7ij5BGFbxOba7TfqDPr+4YLK2nYQBIYxAOt6vZ7oNMEmSrWpppWSDNGncLdDs6CdTlpNPcIuI1nzCbGJLwTz8qcU9zXw0TE/dou0ipI8o3NdCk9DXLyF2hzHRiPcQaiEE9gKFQPe1cmlaryvcj7xC3dIg0XXsn3e16+2b/QPmA4RsDIgPgGFI6FYg4wxlT3cIijGjhpgd5N+dJtIH9HBZIU+CbosAAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1OlRSsO7SDikKE62UWlONYqFKFCqBVadTC59AuatCQpLo6Ca8HBj8Wqg4uzrg6ugiD4AeLq4qToIiX+Lym0iPHguB/v7j3u3gFCq8o0sy8BaLplZFJJMZdfFQOvGEQQYcQQl5lZn5OkNDzH1z18fL2L8Szvc3+OIbVgMsAnEidY3bCIN4jjm1ad8z5xhJVllficeNKgCxI/cl1x+Y1zyWGBZ0aMbGaeOEIslnpY6WFWNjTiGeKoqumUL+RcVjlvcdaqDda5J39hqKCvLHOd5hhSWMQSJIhQ0EAFVVjUVwU6KSYytJ/08I86folcCrkqYORYQA0aZMcP/ge/uzWL01NuUigJ9L/Y9sc4ENgF2k3b/j627fYJ4H8GrvSuv9YCZj9Jb3a16BEwvA1cXHc1ZQ+43AFGnuqyITuSn6ZQLALvZ/RNeSB8Cwysub119nH6AGSpq/QNcHAITJQoe93j3cHe3v490+nvB/E3ctlpr7KMAAANeGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDpkMjJlN2QyMi00NGVjLTRiMDktOTU2Zi0yMDYwZWIxMGRkOTEiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NjgyZGM2ODUtZmM1Zi00MGY0LTljNTQtNmY2ZTk0N2MwZGVlIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODhhMjYxMTMtZGE2NC00MGM3LTk1NmYtNDYxYzkyMTQyNjI3IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iTGludXgiCiAgIEdJTVA6VGltZVN0YW1wPSIxNjk5NDcyNzg5MDU1MzU1IgogICBHSU1QOlZlcnNpb249IjIuMTAuMzQiCiAgIHRpZmY6T3JpZW50YXRpb249IjEiCiAgIHhtcDpDcmVhdG9yVG9vbD0iR0lNUCAyLjEwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDIzOjExOjA4VDIwOjQ2OjI3KzAxOjAwIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyMzoxMTowOFQyMDo0NjoyNyswMTowMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjkyZmU1YjYzLTRlOTgtNDFmMi1iNThiLTlmNTc5OGU3OTYyNyIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51eCkiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMTEtMDhUMjA6NDY6MjkrMDE6MDAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+gMYcMQAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+cLCBMuHQOQ4LgAAAk+SURBVHja7Z3JihRLFIa7tZ3fw42zC8GdDyROIOITiBtHfIl6CjciIjiibyCKS+1uZ/vu8n4X8iPPqUrlLv5vFRaZUSeGas8fJ+LE+mKx2Flbkl+/fo1+vnv37rW5WV9fH8o7OzuzvGuf//79e/J5smvXrtHPWY89s8rzFaxOfl5py5+gYk9l7nXHpVJnZQ6vYn93/tA2zkm+y7L1T6VPKn1b6Ydu/z969Ggo371799961kII4X9M/kiFEP7XbJi7tQomnfbs2TOUf/z4MYs87LrcJlH5+cbGxqQk5DOk2y7WQ/tZj7nNJk/MRaf9fJffS3vmkqjWh2bPwYMHh/LPnz8nx5f1036+a99r89OWFMxmG+tK/1QkOdvC72J7aT/5/v37pJRju2wu8V2WabP1g7Xr27dvQ/njx4/xpEIIkXshhPDn5J65siZtzGU1ucRnzC00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'
}

def send_discord_message(message, image_path=None):
    data = {
        "content": message,
        "username": "Raid farm bot"
    }
    files = None
    if image_path:
        image_data = open(image_path, 'rb').read()
        files = {'file': (os.path.basename(image_path), image_data, 'image/png')}
    result = requests.post(discord_webhook_url, data=data, files=files if files is not None else None)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def capture_hourly_screenshot():
    current_time = datetime.datetime.now()
    file_name = f"{current_time.strftime('%Y%m%d%H%M')}.png"
    file_path = os.path.join(temp_screenshot_directory, file_name)
    screenshot = ImageGrab.grab()
    screenshot.save(file_path, 'PNG')
    send_discord_message("Hourly status screenshot:", file_path)

def click_at_position(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])

def raid_farm_clicking():
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

def decode_and_save_image(encoded_image, filename):
    decoded_image = base64.b64decode(encoded_image)
    image_data = BytesIO(decoded_image)
    image = Image.open(image_data)
    image.save(filename)
    return filename

def find_and_click_button(image_file):
    button_image = cv2.imread(image_file, 0)
    w, h = button_image.shape[::-1]

    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Template matching
    res = cv2.matchTemplate(screenshot_gray, button_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Click if a good match is found
    if max_val > 0.8:  # Adjust this threshold as needed
        click_x, click_y = max_loc[0] + w // 2, max_loc[1] + h // 2
        pyautogui.click(click_x, click_y)
        print(f"Clicked on the {image_file} button.")
        return True
    else:
        print(f"No suitable match found for {image_file}.")
        return False

def handle_disconnect():
    print("Handling disconnect...")

    # Try clicking with image recognition
    clicked = False
    for key, value in encoded_images.items():
        filename = f'/tmp/{key}_button.png'
        decode_and_save_image(value, filename)
        time.sleep(1)  # Wait for UI response
        if find_and_click_button(filename):
            clicked = True
            break

    if not clicked:
        # Fallback to coordinate-based clicking
        back_to_server_button_pos = (1170, 364)
        join_server_button_pos = (955, 457)

        click_at_position(*back_to_server_button_pos)
        print("Clicked 'Back to Server List' using coordinates.")
        time.sleep(2)

        click_at_position(*join_server_button_pos)
        print("Clicked 'Join Server' using coordinates.")
        time.sleep(10)

    capture_hourly_screenshot()
    print("Screenshot captured and sent to Discord.")

if __name__ == "__main__":
    print('Raid farm clicker started.')
    last_hourly_screenshot_time = None

#wait before starting
    time.sleep(10)

    while True:
        current_time = datetime.datetime.now()

        # Perform the raid farm clicking
        raid_farm_clicking()

        # Every hour at 5 minutes past the hour, take and send a status screenshot
        if current_time.minute == 5 and (last_hourly_screenshot_time is None or current_time.hour != last_hourly_screenshot_time.hour):
            capture_hourly_screenshot()
            last_hourly_screenshot_time = current_time

        # Check for disconnects every minute to handle reconnections more promptly
        if current_time.minute % 1 == 0 and current_time.second < 10:  # Check within the first 10 seconds of every minute
            handle_disconnect()

        time.sleep(0.645)  # Time interval between clicks