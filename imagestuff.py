import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import time
import cv2
import pyautogui
from screeninfo import get_monitors
from mss import mss  

def get_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            return m
    return None

class ScreenshotSelector:
    def __init__(self, root):
        self.root = root
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.temp_screenshot_path = '/tmp/temp_screenshot.png'
        self.button_image_path = None

        # Delay and capture
        time.sleep(5)
        self.capture_primary_display()

        # Load the screenshot for display
        self.image = Image.open(self.temp_screenshot_path)
        self.tkimage = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.tkimage)

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Bind key events
        self.root.bind("<d>", self.on_d_press)

    def capture_primary_display(self):
        # Command to capture the primary display
        cmd = ["gnome-screenshot", "-f", self.temp_screenshot_path]

        # Execute the command
        subprocess.run(cmd, check=True)

    def on_press(self, event):
        self.start_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        self.start_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        curX = self.root.winfo_pointerx() - self.root.winfo_rootx()
        curY = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_release(self, event):
        end_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        end_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.capture_region(self.start_x, self.start_y, end_x, end_y)
        self.root.destroy()

    def capture_region(self, x1, y1, x2, y2):
        region_screenshot = self.image.crop((x1, y1, x2, y2))
        self.button_image_path = '/tmp/button_image.png'
        region_screenshot.save(self.button_image_path)
        print(f"Button image saved to {self.button_image_path}")

    def on_d_press(self, event):
        if self.button_image_path:
            self.find_button_and_click(self.button_image_path)

    def find_button_and_click(self, button_image_path):
        # Take a current screenshot of the primary display
        self.capture_primary_display()

        # Load the current screenshot and button image
        current_screenshot = cv2.imread(self.temp_screenshot_path, 0)
        button_image = cv2.imread(button_image_path, 0)
        w, h = button_image.shape[::-1]

        # Template matching
        res = cv2.matchTemplate(current_screenshot, button_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(f"Match percentage: {max_val * 100:.2f}%")

        # Click if a good match is found
        if max_val > 0.8:  # Adjust this threshold as needed
            click_x, click_y = max_loc[0] + w//2, max_loc[1] + h//2
            pyautogui.click(click_x, click_y)
            print("Clicked on the button.")
        else:
            print("No suitable match found.")

if __name__ == "__main__":
    root = tk.Tk()
    ScreenshotSelector(root)
    root.mainloop()
