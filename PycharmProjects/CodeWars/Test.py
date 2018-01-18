import tkinter as tk
from tkinter import ttk
import time
import multiprocessing

POMIDORO = 1



def pomidoro(start_time:float, time_step: float = 25.0):
    finish_time = start_time+time_step*60
    while True:
        if time.time() < finish_time:
            time.sleep(5)
            continue
        break
    return True


class PomidoroApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Epic pomidoro app")

        # configure window
        self.win_width = 400
        self.win_height = 300
        self.x = 330
        self.y = 200
        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))

        # main_frame will
        self.frame1 = tk.Frame(self)
        self.frame1.grid(row = 0, column = 0, sticky = "nsew")
        self.app_info = ttk.Label(self.frame1, text="Pomidoro app version 0.1")
        self.app_info.grid(row=0, column=0, padx=30, pady=30)\

    def delay(self):
        self.after(100, self.test)

    def test(self):
        time.sleep(3)
        self.app_info.config(text = "BBBBBBBBBB")



def idk(app):
    app.test()

if __name__ == "__main__":
    app = PomidoroApp()
    app.delay()
    app.mainloop()


