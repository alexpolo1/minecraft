import pyautogui
import keyboard
import time

print("Hover over a position and press 'x' to capture the mouse coordinates. Press 'Esc' to exit.")

captured_positions = []

while True:
    try:
        if keyboard.is_pressed('x'):
            x, y = pyautogui.position()
            if (x, y) not in captured_positions:  # Prevent capturing the same position if the key is held down
                captured_positions.append((x, y))
                print(f"Position captured: {x}, {y}")
            time.sleep(0.2)  # Add a slight delay to prevent multiple captures for a single press

        if keyboard.is_pressed('esc'):
            print("Exiting.")
            break
    except RuntimeError as e:
        print(e)
        continue

print("\nAll captured positions:")
for position in captured_positions:
    print(position)
