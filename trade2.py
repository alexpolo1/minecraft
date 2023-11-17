import subprocess
import time

def right_click(x, y):
    move_mouse(x, y)
    print("Performing right click.")
    subprocess.run(['xdotool', 'click', '3'])  # Right-click

def drag_slider(start_x, start_y, end_x, end_y):
    print("Dragging slider.")
    move_mouse(start_x, start_y)
    subprocess.run(['xdotool', 'mousedown', '1'])  # Left mouse button down
    move_mouse(end_x, end_y)
    subprocess.run(['xdotool', 'mouseup', '1'])  # Left mouse button up

def click(x, y):
    move_mouse(x, y)
    print("Performing left click.")
    subprocess.run(['xdotool', 'click', '1'])  # Left-click

def shift_click(x, y):
    print("Performing shift click.")
    move_mouse(x, y)
    subprocess.run(['xdotool', 'keydown', 'shift', 'click', '1', 'keyup', 'shift'])  # Shift-click

def move_mouse(x, y):
    subprocess.run(['xdotool', 'mousemove', str(x), str(y)])

def focus_minecraft_window():
    print("Focusing Minecraft window...")
    # Replace 'MinecraftWindowName' with the actual window name
    subprocess.run(['xdotool', 'search', '--name', 'MinecraftWindowName', 'windowactivate', '--sync'])
    time.sleep(2)
    print("Pressing Esc...")
    subprocess.run(['xdotool', 'key', 'Escape'])
    time.sleep(2)

# Initial setup
focus_minecraft_window()

# Perform actions
right_click(2725, 1203)
time.sleep(3)

drag_slider(2600, 1399, 2600, 1408)
time.sleep(3)

click(2450, 1408)
time.sleep(3)

shift_click(2994, 1105)
time.sleep(3)

# Press 'Esc' key to possibly exit a menu or screen
print("Pressing 'Esc' key.")
subprocess.run(['xdotool', 'key', 'Escape'])
time.sleep(3)

# Press and hold 'D' key for a duration to simulate a step
print("Holding 'D' key for a step.")
subprocess.run(['xdotool', 'keydown', 'd'])
time.sleep(0.4)  # Hold 'D' for 0.4 second; adjust this duration as needed
subprocess.run(['xdotool', 'keyup', 'd'])
time.sleep(10)  # Wait after the step
