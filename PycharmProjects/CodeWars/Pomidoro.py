import tkinter as tk
from tkinter import ttk
import time
import multiprocessing


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
        for f in (StartPage, PomidoroPage, TimeBreakPage):
            frame = f(self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        # show start page first
        self.show_frame(StartPage)

        # Pomidoro counter
        self.pomidoro = 0

    # Function which raises needed frame up
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if page == PomidoroPage:
            frame.after(1, lambda: frame.timer(time.time()+int(self.frames[StartPage].time_step.get())*10))
        if page == TimeBreakPage:
            page.update()


class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)
        app_info = ttk.Label(self, text="Pomidoro app version 0.1")
        app_info.grid(row=0, column=0, padx=30, pady=30)

        #
        time_info = ttk.Label(self, text="Type your pomidoro step\n"
                                           "default value is 25 minutes")
        time_info.grid(row=1, column=0)

        self.time_step = tk.StringVar()
        ask_time = ttk.Entry(self, textvariable=self.time_step, width=5)
        ask_time.insert(tk.END, "25")
        ask_time.bind('<Return>', self.enter)
        ask_time.grid(row=1, column=1)


        time_break_info = ttk.Label(self, text="Type your time break step\n"
                                           "default value is 5 minutes")
        time_break_info.grid(row=2, column=0)

        self.time_break_step = tk.StringVar()
        ask_time_break = ttk.Entry(self, textvariable=self.time_break_step, width=5)
        ask_time_break.insert(tk.END, "5")
        ask_time_break.bind('<Return>', self.enter)
        ask_time_break.grid(row=2, column=1)

        # Start button
        self.start_button =  ttk.Button(self, text = "Start", width = 10,
                                              command = self.enter)
        self.start_button.grid(row = 3, column = 0, sticky = (tk.W))


    def enter(self, event = None):
        self.master.master.show_frame(PomidoroPage)


class PomidoroPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        # Pomidoro information
        pomidoro_txt = "{} pomidoro".format(parent.pomidoro)
        pomidoro_info = ttk.Label(self, text=pomidoro_txt)
        pomidoro_info.grid(row=0, column=0, pady=30)

        # left time
        time_txt = "{}m {}s".format(int(parent.frames[StartPage].time_step.get()), 0)
        self.time_info = ttk.Label(self, text=time_txt, width = 30)
        self.time_info.grid(row=1, column=0, sticky = tk.E)

        # Stop button
        self.stop_button =  ttk.Button(self, text = "Start", width = 10,
                                              command = self.stop)
        self.stop_button.grid(row = 3, column = 0, sticky = (tk.W))

    def stop(self):
        self.master.master.pomidoro = 0
        self.master.master.show_frame(StartPage)


    def timer(self, finish):
        remaining_time = finish - time.time()
        if remaining_time<=0:
            self.master.master.pomidoro += 1
            self.master.master.show_frame(TimeBreakPage)
            return
        minutes = remaining_time // 60
        seconds = int(remaining_time % 60)
        time_txt = "{}m {}s".format(minutes, seconds)
        self.time_info.config(text = time_txt)
        self.time_info.after(1000, lambda: self.timer(finish))


class TimeBreakPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        pause_txt = "{} of 4 pomidoros complete".format(self.master.master.pomidoro)
        pause_info = ttk.Label(self, text=pause_txt)
        pause_info.grid(row=0, column=0, pady=30)


        time_break_txt = "Take a {} minutes break. Press the button when you will be ready to start the next " \
                         "pomidoro".format(int(parent.frames[StartPage].time_break_step.get()))
        self.time_break_info = ttk.Label(self, text=time_break_txt, width = 30)
        self.time_break_info.grid(row=1, column=0, sticky = tk.E)


    def next_pomidoro(self):
        self.master.master.show_frame(PomidoroPage)




if __name__ == "__main__":
    app = PomidoroApp()
    app.mainloop()


