import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

import tkinter as tk
from tkinter import ttk

style.use("ggplot")
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

        for f in (StartPage, PageOne, PageTwo, PageThree):
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

        text = tk.Message()

        go_1_button = ttk.Button(self, text = "Go to the first page",
                                command = lambda: controller.show_frame(PageOne))
        go_1_button.pack()

        go_2_button = ttk.Button(self, text = "Go to the second page",
                                command = lambda: controller.show_frame(PageTwo))
        go_2_button.pack()

        go_3_button = ttk.Button(self, text = "Go to the third page",
                                command = lambda: controller.show_frame(PageThree))
        go_3_button.pack()


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


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Graph page", font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)



        home_button = ttk.Button(self, text = "Go home, you're drunk",
                                command = lambda: controller.show_frame(StartPage))
        home_button.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        x = [0,1,2,3,4,5,6,7,8]
        y = [1,24,56,33,43,1,23,2,45]

        a.plot(x, y)



        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.BOTTOM, expand = True)

        def upDate():
            x.append(x[-1] + 1)
            y.append(int(y[-1] * 1.3))
            a.clear()
            a.plot(x, y)
            canvas.show()

        update_button = ttk.Button(self, text="Update",
                                   command=upDate)
        update_button.pack()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)


app = ClassificationApp()
app.mainloop()