import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageTk
import numpy as np

LARGE_FONT = ("Verdana", 14)
NORMAL_FONT = ("Verdana", 12)


class PomidoroApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Epic pomidoro app")

        # configure window
        self.win_width = 400
        self.win_height = 280
        self.x = 330
        self.y = 200
        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))
        self.resizable(False, False)

        # main_frame will
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand = True, fill = 'both')
        #self.main_frame.grid(row = 0, column = 0, sticky = 1)

        # Pomidoro counter
        self.pomidoro = 0

        # container for all frames (pages)
        self.frames = {}

        # fill the container
        for f in (StartPage, PomidoroPage, TimeBreakPage):
            frame = f(self)
            self.frames[f] = frame
            #frame.pack(expand = True, fill = 'both')
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # show start page first
        self.show_frame(StartPage)

    # Function which raises needed frame up
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        frame.updates()
        if page == PomidoroPage:
            frame.after(1, lambda: frame.timer(time.time()+int(self.frames[StartPage].time_step.get())*10))
        if page == StartPage:
            self.pomidoro = 0


class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        # App info
        app_info = ttk.Label(self, text="Pomidoro app version 0.1", font = LARGE_FONT)
        app_info.grid(row=0, column=0, columnspan = 2, sticky = "nswe", padx = (70, 0), pady = (30, 20))

        # Instructions to set own pomidoro time
        time_info = ttk.Label(self, text="Type your pomidoro step,\n"
                                           "default value is 25 minutes", font = NORMAL_FONT)
        time_info.grid(row=1, column=0, padx = (20, 0), pady = (10, 20), sticky = tk.W)

        # Pomidoro entry field
        self.time_step = tk.StringVar()
        ask_time = ttk.Entry(self, textvariable=self.time_step, width = 2, font = LARGE_FONT)
        ask_time.insert(tk.END, "25")
        ask_time.bind('<Return>', self.enter)
        ask_time.grid(row=1, column=1, ipady = 2)

        minuntes_txt =  ttk.Label(self, text = "minutes", font = NORMAL_FONT)
        minuntes_txt.grid(row = 1, column = 3)

        # Instruction to set own time break time
        time_break_info = ttk.Label(self, text="Type your time break step,\ndefault value is 5 minutes",
                                    font = NORMAL_FONT)
        time_break_info.grid(row=2, column=0, padx = (20, 10), pady = (0, 20), sticky = tk.W)

        # Time break entry field
        self.time_break_step = tk.StringVar()
        ask_time_break = ttk.Entry(self, textvariable=self.time_break_step, width = 2, font = LARGE_FONT)
        ask_time_break.insert(tk.END, "5")
        ask_time_break.bind('<Return>', self.enter)
        ask_time_break.grid(row=2, column=1, ipady = 2)

        seconds_txt =  ttk.Label(self, text = "minutes", font = NORMAL_FONT)
        seconds_txt.grid(row = 2, column = 3)

        # Start button
        self.start_button =  ttk.Button(self, text = "Start", command = self.enter, width = 15)
        self.start_button.grid(row = 3, column = 0, columnspan = 2, padx = (60, 0), pady = (20, 0), sticky = tk.S)

    # enter processing
    def enter(self, event = None):
        self.master.master.show_frame(PomidoroPage)

    # Updates frame content when it updates
    def updates(self):
        pass # Start page does not have anything to update


class PomidoroPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        # Pomidoro information
        pomidoro_txt = "{} pomidoro".format(parent.pomidoro + 1)
        self.pomidoro_info = ttk.Label(self, text=pomidoro_txt)
        self.pomidoro_info.grid(row=0, column=0, pady=30)

        # Pomidoro canvas
        self.silhouette_img = Image.open("images\\222.png")
        self.pomidoro_img  = Image.open("images\\111.png")
        self.canvas_silhouette = tk.Canvas(self, width = 200, height = 190)
        self.canvas_silhouette.create_image(0, 0, anchor=tk.NW)
        self.canvas_silhouette.grid(row = 0, column = 1, rowspan = 2, sticky=(tk.N,tk.W))

        # left time
        time_txt = "{}m {}s".format(int(parent.frames[StartPage].time_step.get()), 0)
        self.time_info = ttk.Label(self, text=time_txt, width = 30)
        self.time_info.grid(row=1, column=0, sticky = tk.E)

        # Stop button
        self.stop_button =  ttk.Button(self, text = "Stop", width = 10, command = self.stop)
        self.stop_button.grid(row = 3, column = 0, sticky = (tk.W))

        self.after_id = None

    # Stop current session, drop pomidoro counter to 0 and rise the start page
    def stop(self):
        self.master.master.pomidoro = 0
        self.after_cancel(self.after_id)
        self.master.master.show_frame(StartPage)

    # Converts seconds to time like 07:33
    def timesting(self, remaining_time):
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        if minutes < 10:
            minutes = "0{}".format(minutes)
        if seconds < 10:
            seconds = "0{}".format(seconds)
        return "{}:{}".format(minutes, seconds)

    # Shows current pomidoro time
    def timer(self, finish):
        remaining_time = finish - time.time() # calculate remaining time in unix seconds
        if remaining_time<=0:
            self.master.master.pomidoro += 1
            self.master.master.show_frame(TimeBreakPage)
            return
        self.time_info.config(text = self.timesting(remaining_time))

        # calculating images ratio
        time_step = int(self.master.master.frames[StartPage].time_step.get())*10
        height = int(190*(remaining_time/time_step))
        pomidoro_part = self.pomidoro_img.crop((0, height, 200, 190))
        silhouette_part = self.silhouette_img.crop((0, 0, 200, height))

        # makes arrays no execute vertical stack of images
        pomidoro_arr = np.asarray(pomidoro_part)
        silhouette_arr = np.asarray(silhouette_part)

        # stacking arrays
        if pomidoro_part.height == 0:
            stacked_arr = silhouette_arr
        elif silhouette_part.height == 0:
            stacked_arr = pomidoro_arr
        else:
            stacked_arr = np.vstack((silhouette_arr, pomidoro_arr))

        # converting arr to img
        final_img = ImageTk.PhotoImage(Image.fromarray(stacked_arr))

        # updating img
        self.canvas_silhouette.create_image(0, 0, anchor=tk.NW, image = final_img )
        self.canvas_silhouette.image = final_img
        self.canvas_silhouette.update()

        self.after_id = self.time_info.after(1000, lambda: self.timer(finish))

    # Updates frame content when it updates
    def updates(self):
        pomidoro_info = "{} pomidoro".format(self.master.master.pomidoro + 1)
        self.pomidoro_info.config(text = pomidoro_info)


class TimeBreakPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.main_frame)

        # Pomidoro info
        pause_txt = "{} of 4 pomidoros complete".format(parent.pomidoro)
        self.pause_info = ttk.Label(self, text=pause_txt)
        self.pause_info.grid(row=0, column=0, columnspan = 4, pady=30)

        # Pause info
        time_break_txt = "Take a {} minutes break. Press the button when you will be ready to start the next " \
                         "pomidoro".format(int(parent.frames[StartPage].time_break_step.get()))
        self.time_break_info = ttk.Label(self, text=time_break_txt, width = 30)
        self.time_break_info.grid(row=1, column=0, sticky = tk.E)

        # Pomidoros
        self.pomidoro_img = Image.open("images\\111.png")
        self.pomidoros = tk.Canvas(self, width=50, height=47)
        self.pomidoros.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.W))

        # Next pomidoro button
        self.stop_button =  ttk.Button(self, text = "Go next", width = 10, command = self.next_pomidoro)
        self.stop_button.grid(row = 3, column = 0, columnspan = 4, sticky = (tk.W))

    # Rises the next pomidoro frame
    def next_pomidoro(self):
        self.master.master.show_frame(PomidoroPage)

    # Rises the start frame
    def start_frame(self):
        self.master.master.show_frame(StartPage)

    # Updates frame content when it updates
    def updates(self):
        self.stop_button.config(text='Go next', command=self.next_pomidoro)
        pomidoro_count = self.master.master.pomidoro
        pomidoro_info = "{} of 4 pomidoros are completed".format(pomidoro_count)
        if pomidoro_count >= 4:
            self.master.master.pomidoro = 0
            pomidoro_info = "All pomidoros are completed\ntake a 15 minutes brake"
            self.stop_button.config(text = 'Finish', command = self.start_frame)
        self.pause_info.config(text = pomidoro_info)


if __name__ == "__main__":
    app = PomidoroApp()
    app.mainloop()


