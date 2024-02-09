#autoclick
import os
os.environ['DISPLAY'] = ':0'
import pyautogui
import tkinter as tk
from threading import Thread
from Xlib import display


def automate_clicking():
    while True:
        pyautogui.click(x1, y1)
        pyautogui.click(x2, y2)

def start_clicking():
    global x1, y1, x2, y2
    x1, y1 = map(int, point1_entry.get().split(','))
    x2, y2 = map(int, point2_entry.get().split(','))
    t = Thread(target=automate_clicking)
    t.daemon = True
    t.start()

app = tk.Tk()
app.title("Simple Mouse Clicker")

tk.Label(app, text="Point 1 (x,y):").pack()
point1_entry = tk.Entry(app)
point1_entry.pack()

tk.Label(app, text="Point 2 (x,y):").pack()
point2_entry = tk.Entry(app)
point2_entry.pack()

start_button = tk.Button(app, text="Start Clicking", command=start_clicking)
start_button.pack()

app.mainloop()
