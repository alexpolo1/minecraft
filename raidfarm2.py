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
    disconnected = find_template_on_screen(template_paths['connection_lost'])
    if disconnected:
        print("Connection lost detected.")
    else:
        # If template matching fails, use the backup coordinates for 'Back to Server List'
        disconnected = (1170, 364)  # Backup coordinates

    click_at_position(*disconnected)
    print("Clicked 'Back to Server List'.")
    time.sleep(2)  # Wait for UI response

    # Attempt to find the 'Join Server' button via template matching
    join_server = find_template_on_screen(template_paths['join_server'])
    if join_server:
        print("Join Server button detected.")
    else:
        # If template matching fails, use the backup coordinates for 'Join Server'
        join_server = (955, 457)  # Backup coordinates

    click_at_position(*join_server)
    print("Clicked 'Join Server'.")
    time.sleep(2)  # Wait for UI response

    # Send a message and screenshot to Discord
    send_discord_message("Attempting to reconnect to the server.")
    capture_hourly_screenshot()
    print("Screenshot captured and sent to Discord.")

if __name__ == "__main__":
    print('Raid farm clicker started.')
    time.sleep(10)  # Initial wait before starting the clicking loop

    last_screenshot_time = datetime.datetime.now() - datetime.timedelta(minutes=5)

    while True:
        current_time = datetime.datetime.now()
        raid_farm_clicking()

        # Take a screenshot and send it to Discord 5 minutes past every hour
