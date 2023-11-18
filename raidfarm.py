import time
import subprocess

def click():
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

# Wait for 10 seconds before starting
time.sleep(10)

# Continuously perform left clicks every 0.645 seconds
while True:
    click()
    time.sleep(0.645)  # Wait for 0.645 seconds before the next click

