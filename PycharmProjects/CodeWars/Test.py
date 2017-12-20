import win32gui
# flags, hcursor, (x,y) = win32gui.GetCursorInfo()
import time
import keyboard
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
# shell.SendKeys("^a") # CTRL+A may "select all" depending on which window's focused
# shell.SendKeys("{DELETE}") # Delete selected text?  Depends on context. :P
# shell.SendKeys("{TAB}") #Press tab... to change focus or whatever

if __name__ == "__main__":
    x_prev = 0
    y_prev = 0
    while(1):
        if keyboard.is_pressed('q'):  # if key 'q'
            #print('You Pressed A Key!')
            keyboard.press('z')
        flags, hcursor, (x, y) = win32gui.GetCursorInfo()
        dx = x-x_prev
        dy = y-y_prev
        if abs(dx)>10:
            if dx>0:
                shell.SendKeys('d')
            else:
                shell.SendKeys('a')
        if abs(dy)>10:
            if dy>0:
                shell.SendKeys('s')
            else:
                shell.SendKeys('w')
        x_prev = x
        y_prev = y
        time.sleep(0.05)

