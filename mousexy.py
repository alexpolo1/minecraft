import pyautogui
import keyboard

print("Press 'c' to capture the mouse position. Press 'Esc' to exit.")

captured_positions = []
key_pressed = False

while True:
    try:
        if keyboard.is_pressed('c'):
            if not key_pressed:
                x, y = pyautogui.position()
                captured_positions.append((x, y))
                print(f"Position captured: {x}, {y}")
                key_pressed = True
        else:
            key_pressed = False

        if keyboard.is_pressed('Esc'):
            print("Exiting.")
            break
    except RuntimeError:
        continue

print("\nAll captured positions:")
for position in captured_positions:
    print(position)
