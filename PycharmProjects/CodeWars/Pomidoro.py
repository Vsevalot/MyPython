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
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row = 0, column = 0, sticky = "nsew")

        # container for all frames (pages)
        self.frames = {}

        # fill the container
        for f in (StartPage, PomidoroPage):
            frame = f(self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        # show start page first
        self.show_frame(StartPage)



    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if page == PomidoroPage:
            frame.test()


class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)
        app_info = ttk.Label(self, text="Pomidoro app version 0.1")
        app_info.grid(row=0, column=0, padx=30, pady=30)

        time_info = ttk.Label(self, text="Print your pomidoro step\n"
                                           "default value is 25 minutes")
        time_info.grid(row=1, column=0)

        self.time_step = tk.StringVar()
        ask_time = ttk.Entry(self, textvariable=self.time_step, width=5)
        ask_time.insert(tk.END, "25")
        ask_time.bind('<Return>', self.enter)
        ask_time.grid(row=1, column=2)

    def enter(self, event = None):
        self.master.master.show_frame(PomidoroPage)


def timer(pomidoro_frame):
    while True:
        time.sleep(1)
        remaining_time = int(pomidoro_frame.finish_time - time.time())
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_txt = "{}m {}s".format(minutes, seconds)
        pomidoro_frame.time_info.config(text = time_txt)


class PomidoroPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        start_time = time.time()
        self.finish_time = start_time + int(parent.frames[StartPage].time_step.get()) * 60

        pomidoro_txt = "{} pomidoro".format(POMIDORO)
        pomidoro_info = ttk.Label(self, text=pomidoro_txt)
        pomidoro_info.grid(row=0, column=0, padx=30, pady=30)


        time_txt = "{}m {}s".format(int(parent.frames[StartPage].time_step.get()), 0)
        self.time_info = ttk.Label(self, text=time_txt)
        self.time_info.grid(row=1, column=0, padx=30, pady=30)


    def test(self):
        time.sleep(10)
        self.time_info.config(text="AAAAAAAAAAA")


    def updater(self):
        procces = multiprocessing.Process(target=timer, args=(self,))
        procces.start()







if __name__ == "__main__":
    app = PomidoroApp()
    app.mainloop()


