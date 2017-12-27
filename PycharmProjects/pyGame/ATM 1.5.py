import win32gui
import time
import keyboard


def atmLabel(root):
    import tkinter, win32api, win32con, pywintypes

    label = tkinter.Label(root, text='ATM 1.5 - On', font=('Calibre', '40'), fg='red', bg='black')
    label.master.overrideredirect(True)
    label.master.geometry("+20+15")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "black")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    root.mainloop()

ATM_ACTIVE = False
SENSITIVITY = 10

if __name__ == "__main__":
    x_prev = 0
    y_prev = 0
    while(1):
        if keyboard.is_pressed('Ctrl+q'):  # if key 'q'
            ATM_ACTIVE = not ATM_ACTIVE
        if ATM_ACTIVE:
            atmLabel()
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
        else:
            print(1)
        time.sleep(0.05)

