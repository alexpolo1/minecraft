import cv2
import numpy as np
from PIL import ImageGrab
import subprocess
import time
import datetime
import os
import requests

# Define the directory for screenshots
screenshots_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autologin_screenshots')

# Define paths to your template images
template_paths = {
    'connection_lost': os.path.join(screenshots_directory, 'connection_lost3.png'),
    'back_to_server': os.path.join(screenshots_directory, 'back_to_server.png'),
    'join_server': os.path.join(screenshots_directory, 'join_button.png')
}

# Your Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1171735460729606145/Fyls4_uD7it29TNo7LktQFynb3k1K-BHLx9Y4WqzDK806o1_bVTNz94JNc996kDi-jE6'

def send_discord_message(message):
    data = {
        "content": message,
        "username": "Raidfarm bot"
    }
    result = requests.post(discord_webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def find_template_on_screen(template_path, threshold=0.8):
    # Convert the screen capture to a format OpenCV can understand
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # Load the template and get its dimensions
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    # Perform template matching
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return (max_loc[0] + w//2, max_loc[1] + h//2)
    return None

def click_at_position(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])

def raid_farm_clicking():
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])

def handle_disconnect():
    print("Handling disconnect...")
    if find_template_on_screen(template_paths['connection_lost']):
        print("Connection lost detected.")
        time.sleep(1)  # Small delay to ensure the screen is updated
        back_to_server_pos = find_template_on_screen(template_paths['back_to_server'])
        if back_to_server_pos:
            click_at_position(*back_to_server_pos)
            print("Clicked 'Back to Server List'.")
            time.sleep(1)  # Small delay to ensure the click is registered
            join_server_pos = find_template_on_screen(template_paths['join_server'])
            if join_server_pos:
                click_at_position(*join_server_pos)
                print("Clicked 'Join Server'.")
                send_discord_message("The bot has clicked 'Join Server' and is attempting to recover.")
                time.sleep(10)  # Wait for 10 seconds before restarting the raid farm clicker

if __name__ == "__main__":
    print('Raid farm clicker started.')
    time.sleep(10)  # Initial wait before starting the clicking loop
    restart_times = [datetime.time(hour=6), datetime.time(hour=12), datetime.time(hour=18), datetime.time(hour=0)]

    while True:
        current_time = datetime.datetime.now()
        raid_farm_clicking()  # Perform a left click
        
        if any(current_time.time() >= restart_time and current_time.time() < (datetime.datetime.combine(datetime.date.today(), restart_time) + datetime.timedelta(minutes=5)).time() for restart_time in restart_times) or current_time.minute == 0:
            handle_disconnect()  # Check for disconnects at known restart times or every hour
            time.sleep(65)  # Offset the disconnect check cycle after handling a disconnect
        
        time.sleep(0.645)  # Wait for 0.645 seconds before the next click
