import win32gui
import time
import keyboard

ATM_ACTIVE = False
SENSITIVITY = 10

if __name__ == "__main__":
    x_prev = 0
    y_prev = 0
    while(1):
        if keyboard.is_pressed('Ctrl+q'):  # if key 'q'
            ATM_ACTIVE = not ATM_ACTIVE
        if ATM_ACTIVE:
            flags, hcursor, (x, y) = win32gui.GetCursorInfo()
            dx = x-x_prev
            dy = y-y_prev
            if abs(dx)>SENSITIVITY:
                if dx>0:
                    keyboard.press('d')
                else:
                    keyboard.press('a')
            if abs(dy)>SENSITIVITY:
                if dy>0:
                    keyboard.press('s')
                else:
                    keyboard.press('w')
            x_prev = x
            y_prev = y
        time.sleep(0.05)

