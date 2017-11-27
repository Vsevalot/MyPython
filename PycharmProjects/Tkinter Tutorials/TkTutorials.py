import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class ClassificationApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"EEG classification")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage, PageOne, PageTwo):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



def call_leroy(caller):
    print("{} calls Leroy Jinkins!".format(caller))

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Start page", font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)

        go_1_button = ttk.Button(self, text = "Go to the first page",
                                command = lambda: controller.show_frame(PageOne))
        go_1_button.pack()

        go_2_button = ttk.Button(self, text = "Go to the second page",
                                command = lambda: controller.show_frame(PageTwo))
        go_2_button.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "First page", font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)

        go_2_button = ttk.Button(self, text = "Go the 2 page",
                                command = lambda: controller.show_frame(PageTwo))
        go_2_button.pack()

        home_button = ttk.Button(self, text = "Go home, you're drunk",
                                command = lambda: controller.show_frame(StartPage))
        home_button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Second page", font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)

        go_1_button = ttk.Button(self, text = "Go the 1 page",
                                command = lambda: controller.show_frame(PageOne))
        go_1_button.pack()

        home_button = ttk.Button(self, text = "Go home, you're drunk",
                                command = lambda: controller.show_frame(StartPage))
        home_button.pack()


app = ClassificationApp()
app.mainloop()