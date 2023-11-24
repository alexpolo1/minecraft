import cv2
import numpy as np
from PIL import ImageGrab
import subprocess
import time
import datetime
import os
import requests

# Ensure the temp screenshot directory exists
temp_screenshot_directory = '/tmp/mcscreens'
os.makedirs(temp_screenshot_directory, exist_ok=True)

# Your Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1171735460729606145/Fyls4_uD7it29TNo7LktQFynb3k1K-BHLx9Y4WqzDK806o1_bVTNz94JNc996kDi-jE6'

def send_discord_message(message, image_path=None):
    data = {
        "content": message,
        "username": "Minecraft Bot"
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

def handle_disconnect():
    print("Handling disconnect...")

    # Backup coordinates
    back_to_server_button_pos = (1170, 364)
    join_server_button_pos = (955, 457)

    # Click the "Back to Server List" button
    click_at_position(*back_to_server_button_pos)
    print("Clicked 'Back to Server List'.")
    time.sleep(2)  # Wait for the UI to respond

    # Click the "Join Server" button
    click_at_position(*join_server_button_pos)
    print("Clicked 'Join Server'.")
    time.sleep(10)  # Wait for the server to respond

    # Take a screenshot and send it to Discord
    capture_hourly_screenshot()
    print("Screenshot captured and sent to Discord.")

if __name__ == "__main__":
    print('Raid farm clicker started.')
    last_hourly_screenshot_time = None

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
