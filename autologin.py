import cv2
import numpy as np
import pyautogui
import requests
import json
from PIL import ImageGrab
from datetime import datetime, timedelta
import time
import random

# Define the paths to your screenshots
red_hearts_image_path = '/home/alex/minecraft/screenshots/red_hearts.png'
one_heart_image_path = '/home/alex/minecraft/screenshots/one_heart.png'
back_to_server_image_path = '/home/alex/minecraft/screenshots/back_to_server_list3.png'
join_button_image_path = '/home/alex/minecraft/screenshots/join_button.png'
menu_screen_image_path = '/home/alex/minecraft/screenshots/menu_screen.png'
log_file_path = '/home/alex/minecraft/autologin.log'

# Set up the Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1171735460729606145/Fyls4_uD7it29TNo7LktQFynb3k1K-BHLx9Y4WqzDK806o1_bVTNz94JNc996kDi-jE6'

# Global variable to track the last Discord notification time
last_discord_notification = datetime.now() - timedelta(minutes=5)

# Function to send logs to both the local file and the Discord webhook
def log(message, discord_notify=True):
    global last_discord_notification
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {message}"

    # Print to console
    print(log_message)

    # Save to log file
    with open(log_file_path, 'a') as file:
        file.write(log_message + '\n')

    # Send to Discord webhook
    if discord_notify and (datetime.now() - last_discord_notification >= timedelta(minutes=5)):
        data = {
            "content": log_message,
            "username": "AutoLoginBot"
        }
        result = requests.post(webhook_url, json=data)
        if result.status_code != 204:
            print(f"Failed to send message to Discord, status code: {result.status_code}")
        last_discord_notification = datetime.now()

# Function to find the image on the screen and click it
def find_and_click_image(image_path, threshold=0.8, click=True):
    # Take a screenshot of the primary monitor
    screen = np.array(ImageGrab.grab(bbox=None))
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Read the image with the button
    template = cv2.imread(image_path, 0)
    if template is None:
        log(f"Template image at path {image_path} not found.", False)
        return False
    w, h = template.shape[::-1]

    # Match the template image (button) on the screen
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # If the button is found on the screen, click it
    for pt in zip(*loc[::-1]):
        if click:
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2)
        return True
    return False

# ... (Other functions here)
# ... (Continuation of other functions here)

# Main script execution
if __name__ == "__main__":
    log('AutoLoginBot started.')
    last_heartbeat = datetime.now()

    while True:
        now = datetime.now()
        if now - last_heartbeat >= timedelta(minutes=5):
            in_game = find_and_click_image(one_heart_image_path, threshold=0.8, click=False)
            in_menu = find_and_click_image(menu_screen_image_path, threshold=0.8, click=False)
            if in_game:
                log("In-game, red hearts visible.")
            elif in_menu:
                log("In-game, menu screen visible.")
            else:
                log("Status unknown. Checking for disconnect.")
                handle_disconnect()
            last_heartbeat = now
