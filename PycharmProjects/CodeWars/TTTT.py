import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

import tkinter as tk
from tkinter import ttk

style.use("ggplot")
LARGE_FONT = ("Verdana", 14)
MEDIUM_FONT = ("Calibre", 12)


RESULTS_OK = 1

class StartPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"EEG classification")
        master_wiget = tk.Frame(self)
        master_wiget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        #master_wiget.columnconfigure(1, minsize=1)

        introduction_txt = "This script will build pie charts of stage distribution for each classification " \
                           "group in a given csv or xlsx file. You will be able to choose which states you need " \
                           "to analyze and generate logs of file used for in each interested stage."
        introduction = tk.Message(master_wiget, text=introduction_txt, font = LARGE_FONT, width=820)
        introduction.grid(column=0, row=0, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), pady = (15,5))



        instructions_txt = "Script takes a file of results of classification where each group contain a column of " \
                           "eeg fragment's names. Please check that all eeg fragments are named like:\n" \
                           '"folder name_YYYYMMDD_hh.mm.ss(start seconds from beginning-finish seconds from beginning)"\n' \
                           'or "rec number_hh.mm.ss(start seconds from beginning-finish seconds from beginning)".\n\n' \
                           "Also script requires operational reports. Reports should be formed in csv or xlsx files. " \
                           "Report name should be to the same as record name (rec50). If an operational was with " \
                           "ketamine, add (K) to the name of a report. Each line of report should look like: time | " \
                           "anastasia stage | comment (optional) ."' \
                           ''\n\nExample:\n'
        instructions = tk.Message(master_wiget, text=instructions_txt, font = MEDIUM_FONT, width=820)
        instructions.grid(column=0, row=1, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)



        first_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        canvas_results = tk.Canvas(master_wiget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_results.create_image(0, 75, anchor=tk.W, image=first_example)
        canvas_results.image = first_example
        canvas_results.grid(column=0, row=2, columnspan=5, sticky=(tk.N,tk.W), padx = (10,0))

        second_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        canvas_reports = tk.Canvas(master_wiget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_reports.create_image(5, 75, anchor=tk.W, image=second_example)
        canvas_reports.image = second_example
        canvas_reports.grid(column=5, row=2, columnspan=5, sticky=(tk.N,tk.W))



        check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
        canvas_results_state = tk.Canvas(master_wiget, width=38, height=36)
        canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
        canvas_results_state.image = check_img
        canvas_results_state.grid(column=0, row=3, sticky=(tk.E))

        results_text = "No file found, give the way to the analysis file"
        res_txt = tk.Label(master_wiget, text=results_text, font = MEDIUM_FONT)
        res_txt.grid(column=1, row=3, columnspan=7, sticky=(tk.W))



        canvas_reports_state = tk.Canvas(master_wiget, width=38, height=36)
        canvas_reports_state.create_image(0, 18, anchor=tk.W, image=check_img)
        canvas_reports_state.image = check_img
        canvas_reports_state.grid(column=0, row=4, sticky=(tk.N, tk.S, tk.E, tk.W))

        reports_text = "No report folder detected found, give the way to the reports location"
        if RESULTS_OK:
            reports_text = "Report folder selected"
        rep_txt = tk.Label(master_wiget, text=reports_text, font = MEDIUM_FONT)
        rep_txt.grid(column=1, row=4, columnspan=7, sticky=(tk.W))



        def change_results():
            global RESULTS_OK
            RESULTS_OK = not RESULTS_OK
            check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
            results_text = "No file found, give the way to the analysis file"
            if RESULTS_OK:
                check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
                results_text = "Results file selected                                               "
            canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
            canvas_results_state.image = check_img
            canvas_results_state.grid(column=0, row=3, sticky=(tk.E), padx = (0,10))

            res_txt = tk.Label(master_wiget, text=results_text, font=MEDIUM_FONT)
            res_txt.grid(column=1, row=3, columnspan=7, sticky=(tk.W))



        continue_button = ttk.Button(master_wiget, text="change", width=10, command=change_results)
        continue_button.grid(column=2, row=5, sticky=(tk.W))
        exit_button = ttk.Button(master_wiget, text="Continue", width=16, command=lambda: print("Do it"))
        exit_button.grid(column=7, row=5,  sticky=(tk.W))


app = StartPage()
app.mainloop()