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


    def test(self, finish):
        remaining_time = finish - time.time()
        if remaining_time<=0:
            self.app_info.config(text = "Hey!")
        minutes = remaining_time // 60
        seconds = int(remaining_time % 60)
        time_txt = "{}m {}s".format(minutes, seconds)
        self.app_info.config(text = time_txt)
        self.app_info.after(1000, lambda: self.test(finish))



def idk(app):
    app.test()

if __name__ == "__main__":
    app = PomidoroApp()
    app.after(2000, lambda: app.test(time.time()+30))
    app.mainloop()


