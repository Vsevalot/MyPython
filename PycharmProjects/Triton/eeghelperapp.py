import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

import tkinter as tk
from tkinter import ttk

style.use("ggplot")
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Calibre", 12)


RESULTS_OK = 1


class EegClassificationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"EEG classification")
        main_frame = tk.Frame(self)
        #container.pack(side = "top", fill = "both", expand = True)
        main_frame.grid(row = 0, column = 0, sticky = (tk.N, tk.S, tk.E, tk.W))
        self.frames = {}

        for f in (StartPage, PageOne, PageTwo, PageThree):
            frame = f(main_frame, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        master_wiget = tk.Frame.__init__(self, parent)
        #master_wiget.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        introduction_txt = "This script will build pie charts of stage distribution for each classification" \
                       " group in a given csv or xlsx file"
        introduction = tk.Label(master_wiget, text=introduction_txt, font = LARGE_FONT ,width=60, height=1)
        introduction.grid(column=0, row=0, columnspan=4, sticky=(tk.N,tk.W))
        print(introduction.winfo_height())


        instructions_txt = "Please check that all eeg fragments are named like:\n" \
                       '"folder name_YYYYMMDD_hh.mm.ss(start seconds from beginning-finish seconds from beginning)"\n' \
                         'or "rec number_hh.mm.ss(start seconds from beginning-finish seconds from beginning)"' \
                         '\n\nExample:\n'
        instructions = tk.Label(master_wiget, text=instructions_txt, font = MEDIUM_FONT)
        instructions.grid(column=0, row=1, columnspan=4, sticky=(tk.N,tk.W))
        print(instructions.winfo_height())


        first_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\example.png")
        canvas_results = tk.Canvas(master_wiget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_results.create_image(0, 75, anchor=tk.W, image=first_example)
        canvas_results.image = first_example
        canvas_results.grid(column=0, row=2, columnspan=2, sticky=(tk.N,tk.W))

        second_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\example.png")
        canvas_reports = tk.Canvas(master_wiget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_reports.create_image(5, 75, anchor=tk.W, image=second_example)
        canvas_reports.image = second_example
        canvas_reports.grid(column=3, row=2, columnspan=2, sticky=(tk.N,tk.W))



        check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
        if RESULTS_OK:
            check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
        canvas_results_state = tk.Canvas(master_wiget, width=38, height=36)
        canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
        canvas_results_state.image = check_img
        canvas_results_state.grid(column=0, row=3, sticky=(tk.W))

        results_text = "No file found, give the way to the analysis file"
        if RESULTS_OK:
            results_text = "Results file selected"
        res_txt = tk.Label(master_wiget, text=results_text, font = MEDIUM_FONT)
        res_txt.grid(column=1, row=3, columnspan=2, sticky=(tk.W))





        def change():
            global RESULTS_OK
            RESULTS_OK = not RESULTS_OK
            check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
            if RESULTS_OK:
                check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
            canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
            canvas_results_state.image = check_img
            canvas_results_state.grid(column=0, row=3, sticky=(tk.W))



        continue_button = tk.Button(master_wiget, text="change", width=10, command=change)
        continue_button.grid(column=0, row=5, columnspan=2, sticky=(tk.W))
        exit_button = tk.Button(master_wiget, text="Continue", width=16, command=lambda: controller.show_frame(PageTwo))
        exit_button.grid(column=2, row=5, columnspan=2, sticky=(tk.W))


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


app = EegClassificationApp()
app.mainloop()