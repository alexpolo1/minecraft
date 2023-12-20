import pyautogui
import time
import threading
from Xlib import display

def is_minecraft_focused():
    current_display = display.Display()
    window_id = current_display.get_input_focus().focus.get_full_property(current_display.intern_atom('_NET_WM_NAME'), 0)
    if window_id:
        window_name = window_id.value
        if "Minecraft" in window_name:
            return True
    return False

def hold_key():
    time.sleep(5)  # Wait for 5 seconds before starting
    print("Starting to hold 'W' key. Press 'E' to stop.")
    while not stop_thread:
        if is_minecraft_focused():
            pyautogui.keyDown('w')
        else:
            pyautogui.keyUp('w')
        time.sleep(0.1)
    pyautogui.keyUp('w')

# This flag will control the thread execution
stop_thread = False

# Starting the thread that holds down the 'W' key
thread = threading.Thread(target=hold_key)
thread.start()

# Waiting for the user to press 'E' to stop
try:
    while True:
        time.sleep(0.1)  # Small delay to reduce CPU usage
        if is_minecraft_focused() and pyautogui.press('x'):
            stop_thread = True
            break
except KeyboardInterrupt:
    stop_thread = True

thread.join()
print("Stopped.")
