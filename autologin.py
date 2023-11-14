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
back_to_server_image_path = '/home/alex/minecraft/screenshots/back_to_server.png'
join_button_image_path = '/home/alex/minecraft/screenshots/join_button.png'
log_file_path = '/home/alex/minecraft/autologin.log'

# Set up the Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/your_webhook_url_here'

def log(message, discord_notify=True):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {message}"
    print(log_message)
    with open(log_file_path, 'a') as file:
        file.write(log_message + '\n')
    if discord_notify:
        data = {"content": log_message, "username": "AutoLoginBot"}
        try:
            result = requests.post(webhook_url, json=data)
            if result.status_code != 204:
                print(f"Failed to send message to Discord, status code: {result.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Discord notification failed: {e}")

def find_and_click_image(image_path, threshold=0.8, click=True):
    screen = np.array(ImageGrab.grab(bbox=None))
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, 0)
    if template is None:
        log(f"Template image at path {image_path} not found.", False)
        return False
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        if click:
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2)
        return True
    return False

def handle_disconnect():
    log("Checking for disconnect.", False)
    # Check for 'Back to Server' button
    if find_and_click_image(back_to_server_image_path):
        log("Clicked on the Back to Server button.", False)
        time.sleep(random.randint(5, 10))  # Wait for a few seconds
        # Try to click on 'Join Server' button
        if find_and_click_image(join_button_image_path):
            log("Clicked on the Join Server button.", False)
        else:
            log("Join Server button not found.", False)
    else:
        log("Back to Server button not found.", False)

if __name__ == "__main__":
    log('AutoLoginBot started.')
    while True:
        time.sleep(60)  # Check every 60 seconds
        handle_disconnect()
