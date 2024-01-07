import requests
import subprocess
import time
from PIL import Image, ImageGrab
import logging

def log_and_print(message):
    print(message)
    # Assuming you want to log to the same file as your main script
    with open('minecraft_automation_log.txt', 'a') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}: {message}\n')


def hold_key_for_duration(key, duration):
    log_and_print(f"Waiting 5 seconds before holding '{key}' key for {duration} seconds.")
    time.sleep(5)  # Delay for 5 seconds
    log_and_print(f"Holding '{key}' key.")
    subprocess.run(['xdotool', 'keydown', key])
    time.sleep(duration)
    subprocess.run(['xdotool', 'keyup', key])
    log_and_print(f"Released '{key}' key.")


# Example usage
hold_key_for_duration('a', 11)  # This will hold the 'a' key for 11 seconds
