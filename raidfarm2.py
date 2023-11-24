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
temp_screenshot_directory = '/temp/mcscreens'

# Ensure the temp screenshot directory exists
os.makedirs(temp_screenshot_directory, exist_ok=True)

# Define paths to your template images
template_paths = {
    'connection_lost': os.path.join(screenshots_directory, 'connection_lost3.png'),
    'back_to_server': os.path.join(screenshots_directory, 'back_to_server.png'),
    'join_server': os.path.join(screenshots_directory, 'join_button.png')
}

# Your Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/your_webhook_id/your_webhook_token'

def send_discord_message(message, image_path=None):
    data = {
        "content": message,
        "username": "Minecraft Bot"
    }
    files = None
    if image_path:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/png')}
        result = requests.post(discord_webhook_url, data=data, files=files)
    else:
        result = requests.post(discord_webhook_url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def capture_hourly_screenshot():
    current_hour = datetime.datetime.now().strftime("%H")
    screenshot = ImageGrab.grab()
    file_path = os.path.join(temp_screenshot_directory, f"{current_hour}.png")
    screenshot.save(file_path, 'PNG')
    send_discord_message("Hourly status screenshot:", file_path)

def find_template_on_screen(template_path, threshold=0.8):
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        return (max_loc[0] + w//2, max_loc[1] + h//2)
    return None

def click_at_position(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])

def raid_farm_clicking():
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

def handle_disconnect():
    print("Handling disconnect...")
    if find_template_on_screen(template_paths['connection_lost']):
        print("Connection lost detected.")
        time.sleep(1)
        back_to_server_pos = find_template_on_screen(template_paths['back_to_server'])
        if back_to_server_pos:
            click_at_position(*back_to_server_pos)
            print("Clicked 'Back to Server List'.")
            time.sleep(1)
            join_server_pos = find_template_on_screen(template_paths['join_server'])
            if join_server_pos:
                click_at_position(*join_server_pos)
                print("Clicked 'Join Server'.")
                send_discord_message("The bot has clicked 'Join Server' and is attempting to recover.")
                time.sleep(10)

if __name__ == "__main__":
    print('Raid farm clicker started.')
    time.sleep(10)
    restart_times = [datetime.time(hour=6), datetime.time(hour=12), datetime.time(hour=18), datetime.time(hour=0)]
    last_screenshot_hour = None

    while True:
        current_time = datetime.datetime.now()
        raid_farm_clicking()

        if current_time.minute == 0 and (last_screenshot_hour is None or last_screenshot_hour != current_time.hour):
            capture_hourly_screenshot()
            last_screenshot_hour = current_time.hour

        if any(current_time.time() >= restart_time and current_time.time() < (datetime.datetime.combine(datetime.date.today(), restart_time) + datetime.timedelta(minutes=5)).time() for restart_time in restart_times) or current_time.minute == 0:
            handle_disconnect()
            time.sleep(65)

        time.sleep(0.645)