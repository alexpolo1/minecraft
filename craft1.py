import pyautogui
import keyboard

centerX = 0
centerY = 0
deluje = False
gledam = 0
premik = 150
delay = 100

class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

guiPoss = {}
guiBarva = {}

def obrniSeNa(pozicija):
    global gledam, centerX, centerY, premik
    if pozicija != gledam:
        posX = centerX + (pozicija - gledam) * premik
        posY = centerY
        pyautogui.moveTo(posX, posY, duration=0.05)
        gledam = pozicija

def cakajNaGui(kateri, mode):
    global guiPoss, guiBarva
    while True:
        pixel = pyautogui.pixel(guiPoss[kateri - 1].X, guiPoss[kateri - 1].Y)
        if (mode == 1 and pixel == guiBarva[kateri - 1]) or (mode == 2 and pixel != guiBarva[kateri - 1]):
            return

def cakajNaItem(mode, posX, posY, auto=True):
    global guiBarvaOzadjaItema, guiBarvaOzadjaItemaHighlight
    isOk = False
    while not isOk:
        y = -2
        while y < 3:
            x = -2
            while x < 3:
                if auto:
                    preveriAliKonca()
                pixel = pyautogui.pixel(posX + x, posY + y)
                if mode == 1:  # cakaj da pride na slot
                    if pixel != guiBarvaOzadjaItema and pixel != guiBarvaOzadjaItemaHighlight:
                        return
                elif mode == 2:  # cakaj da gre stran
                    if pixel == guiBarvaOzadjaItema or pixel == guiBarvaOzadjaItemaHighlight:
                        isOk = True
                        if isOk >= 9:
                            return
                x += 2
            y += 2
        isOk = False

def preveriAliKonca():
    if not keyboard.is_pressed('Minecraft'):
        prekini()
    if not deluje:
        keyboard.release('Shift')
        exit()

def craft(pozicija):
    global guiPoss, guiBarva, centerX, centerY
    if not pozicija:
        pozicija = 10
    C_recepti = {}
    I_recepti = {}
    if pozicija < 6:
        y = 0
        x = 0
        while y < 3:
            while x < 5:
                C_recepti[(y, x)] = Point(guiPoss[0].X + x * C_korakX, guiPoss[0].Y + y * C_korakY)
                I_recepti[(y, x)] = Point(guiPoss[4].X + x * I_korakX, guiPoss[4].Y + y * I_korakY)
                x += 1
            y += 1
    pixelCraftingTable = pyautogui.pixel(guiPoss[0].X, guiPoss[0].Y)
    pixelReceptiCraftingT = pyautogui.pixel(guiPoss[2].X, guiPoss[2].Y)
    pixelReceptiInventory = pyautogui.pixel(guiPoss[3].X, guiPoss[3].Y)
    pixelInventory = pyautogui.pixel(guiPoss[4].X, guiPoss[4].Y)
    if pixelCraftingTable == guiBarva[0] and pixelReceptiCraftingT == guiBarva[2]:  # odprt crafting tabla in recepti
        y = 0
        x = 0
        while y < 3:
            while x < 5:
                # Perform the desired crafting action...
                x += 1
            y += 1

def prekini():
    global deluje
    deluje = False

def hotkey_start():
    global deluje, gledam, centerX, centerY
    deluje = True
    gledam = 0
    centerX, centerY = pyautogui.position()
    while deluje:
        preveriAliKonca()
        zanka()

def hotkey_stop():
    global deluje
    deluje = False

keyboard.add_hotkey('windows+j', hotkey_start, suppress=False)
keyboard.add_hotkey('windows-j', hotkey_stop, suppress=False)
keyboard.add_hotkey('e', prekini)
keyboard.add_hotkey('esc', prekini)

# Register hotkeys for crafting
for i in range(10):
    keyboard.add_hotkey('shift+'+str(i), lambda x=i: craft(x))


# Define GUI positions and colors
guiPoss[0] = Point(956, 403)
guiPoss[1] = Point(802, 402)
guiPoss[2] = Point(658, 402)
guiPoss[3] = Point(657, 403)
guiPoss[4] = Point(954, 403)

guiBarva[0] = 0xC3C3C3
guiBarva[1] = 0xC4C4C4
guiBarva[2] = 0xC5C5C5
guiBarva[3] = 0xC5C5C5
guiBarva[4] = 0xC2C2C2

# Other variables for crafting logic
C_korakX = (1094 - 1023) / 4
C_korakY = (516 - 443) / 3
I_korakX = (897 - 692) / 4
I_korakY = (631 - 478) / 3
guiBarvaOzadjaItema = 0x8B8B8B
guiBarvaOzadjaItemaHighlight = 0xC5C5C5

# Start the keyboard listener
keyboard.wait()