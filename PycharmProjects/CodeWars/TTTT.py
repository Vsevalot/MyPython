import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import mypyfunctions as myPy
import os
import copy

import tkinter as tk
from tkinter import ttk


style.use("ggplot")
LARGE_FONT = ("Verdana", 14)
MEDIUM_FONT = ("Calibre", 12)
STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
RESULTS = 0
RESULTS_PATH = ""
SAVE_PATH = ""
REPORTS = 0
EEG_FRAGMENTS = 0
EEG_STAT = 0
STAGE_SHOW = {stage: False for stage in STAGES}
STAGE_SHOW[0] = True
STAGE_SHOW[1] = True
STAGE_SHOW[2] = True
STAGE_SHOW[3] = True
LOG_DICT = {}






class StartPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"EEG classification")

        # master_widget - main widget where all others are located
        master_widget = tk.Frame(self)
        master_widget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Introduction
        introduction_txt = "This script will build pie charts of stage distribution for each classification " \
                           "group in a given csv or xlsx file. You will be able to choose which states you need " \
                           "to analyze and generate logs of file used for in each interested stage."
        introduction = tk.Message(master_widget, text=introduction_txt, font = LARGE_FONT, width=820)
        introduction.grid(column=0, row=0, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), pady = (15,5))


        # Instructions
        instructions_txt = "Script takes a file of results of classification where each group contain a column of " \
                           "eeg fragment's names. Please check that all eeg fragments are named like:\n" \
                           '"folder name_YYYYMMDD_hh.mm.ss(start seconds from beginning-finish seconds from beginning)"\n' \
                           'or "rec number_hh.mm.ss(start seconds from beginning-finish seconds from beginning)".\n\n' \
                           "Also script requires operational reports. Reports should be formed in csv or xlsx files. " \
                           "Report name should be to the same as record name (rec50). If an operational was with " \
                           "ketamine, add (K) to the name of a report. Each line of report should look like: time | " \
                           "anastasia stage | comment (optional) .\n\nNote: Reading files can take some time."' \
                           ''\n\nExample:\n'
        instructions = tk.Message(master_widget, text=instructions_txt, font = MEDIUM_FONT, width=820)
        instructions.grid(column=0, row=1, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)


        # Example of results
        first_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        canvas_results = tk.Canvas(master_widget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_results.create_image(0, 75, anchor=tk.W, image=first_example)
        canvas_results.image = first_example
        canvas_results.grid(column=0, row=2, columnspan=5, sticky=(tk.N,tk.W), padx = (10,0))

        # Example of report
        second_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        canvas_reports = tk.Canvas(master_widget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_reports.create_image(5, 75, anchor=tk.W, image=second_example)
        canvas_reports.image = second_example
        canvas_reports.grid(column=5, row=2, columnspan=5, sticky=(tk.N,tk.W))


        # No / Ok img
        no_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
        canvas_results_state = tk.Canvas(master_widget, width=38, height=36)
        canvas_results_state.create_image(0, 18, anchor=tk.W, image=no_img)
        canvas_results_state.image = no_img
        canvas_results_state.grid(column=0, row=3, sticky=(tk.E), pady = 10)

        # Result state
        results_text = "No file found, chose a way to the analysis file"
        res_txt = tk.Label(master_widget, text=results_text, font = MEDIUM_FONT)
        res_txt.grid(column=2, row=3, columnspan=7, sticky=(tk.W))


        # Add results button
        def resultReader(root):
            global RESULTS
            global RESULTS_PATH
            global SAVE_PATH
            path = tk.filedialog.askopenfilename(filetype=(("CSV File", "*.csv"), ("XLSX File", "*.xlsx")),
                                                 title="Choose a file with results of classification",
                                                 initialdir="Z:\\Tetervak")
            if (path == ''):
                return

            RESULTS_PATH = myPy.pathFromName(path)

            root.config(cursor="wait")
            root.update()

            if  path[-4:] == "xlsx":
                RESULTS = myPy.results2Dict(myPy.readXLSX(path))
                SAVE_PATH = path[:-5]
            elif path[-3:] == "csv":
                RESULTS = myPy.results2Dict(myPy.readCSV(path))
                SAVE_PATH = path[:-4]
            else:
                print("How did you get here?")
                root.config(cursor="")
                exit(0)

            check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
            results_text = "Results file selected"
            canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
            canvas_results_state.image = check_img
            res_txt.config(text = results_text)
            root.config(cursor="")

        add_results_button =  ttk.Button(master_widget, text="Add", width=10, command=lambda: resultReader(self))
        add_results_button.grid(column=9, row=3, sticky=(tk.W))


        # No / Ok img
        canvas_reports_state = tk.Canvas(master_widget, width=38, height=36)
        canvas_reports_state.create_image(0, 18, anchor=tk.W, image=no_img)
        canvas_reports_state.image = no_img
        canvas_reports_state.grid(column=0, row=4, sticky=(tk.E))

        # Report state
        reports_text = "No report folder detected found, give a way to the reports location"
        rep_txt = tk.Label(master_widget, text=reports_text, font = MEDIUM_FONT)
        rep_txt.grid(column=2, row=4, columnspan=7, sticky=(tk.W))

        # Add results button
        def reportReader(root):
            global REPORTS

            path = tk.filedialog.askdirectory(title="Choose a folder which contain reports",
                                              initialdir = "Z:\\Tetervak\\Reports\\complete")
            if (path == ''):
                return
            root.config(cursor="wait")
            root.update()
            REPORTS = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            REPORTS = [myPy.Report(report, myPy.readCSV(report)) for report in REPORTS]

            if REPORTS == []:
                rep_txt.config(text="An empty folder chosen")
                return

            check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
            report_text = "Report folder selected"
            canvas_reports_state.create_image(0, 18, anchor=tk.W, image=check_img)
            canvas_reports_state.image = check_img
            rep_txt.config(text = report_text)
            root.config(cursor="")

        add_results_button =  ttk.Button(master_widget, text="Add", width=10, command=lambda: reportReader(self))
        add_results_button.grid(column=9, row=4, sticky=(tk.W))


        def makeEegFragments(root):
            root.config(cursor="wait")
            root.update()
            global EEG_FRAGMENTS
            global EEG_STAT

            EEG_FRAGMENTS = myPy.matfiles2eegFragments(RESULTS, REPORTS)

            EEG_STAT = myPy.eegStat(EEG_FRAGMENTS)
            plots = PlotPage()
            plots.mainloop()
            root.config(cursor="")


        # Go to plot window button
        continue_button = ttk.Button(master_widget, text="Build plots", width=16, command=lambda: makeEegFragments(self))
        continue_button.grid(column=2, row=5, sticky=(tk.W), pady = (20, 20), padx = 5)

        # Exit app button
        exit_button = ttk.Button(master_widget, text="Exit", width=10, command=lambda: exit(0))
        exit_button.grid(column=7, row=5,  sticky=(tk.W))


class PlotPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Hist plots")
        master_widget = tk.Frame(self)
        master_widget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.figure = Figure(figsize=(14.76, 6.6), dpi=100)
        global LOG_DICT
        LOG_DICT = myPy.histPlotter(self.figure, EEG_STAT, STAGE_SHOW)
        canvas = FigureCanvasTkAgg(self.figure, master_widget)
        canvas.get_tk_widget().grid(column=0, row=1, columnspan=3, sticky=(tk.N, tk.W))
        canvas.show()


        stage_txt = "Stages:"
        stage_label = tk.Label(master_widget, text=stage_txt, font = MEDIUM_FONT)
        stage_label.grid(column=0, row=2, sticky=(tk.N, tk.W), padx = 10)


        class CheckBoxes(tk.Frame):
            def __init__(self, parent, check_dict):
                tk.Frame.__init__(self, parent )
                self.boxes = {}
                i=0
                for box in check_dict:
                    self.boxes[box] = ttk.Checkbutton(self, text=str(box))
                    self.boxes[box].state(['!alternate'])
                    self.boxes[box].grid(row = 0, column = i)
                    if (check_dict[box] == True):
                        self.boxes[box].state(['selected'])
                    i+=1


            def state(self):
                return {box: self.boxes[box].instate(['selected']) for box in self.boxes}

        stage_boxes = CheckBoxes(master_widget, STAGE_SHOW)
        stage_boxes.grid(column=0, row=3, sticky=(tk.N, tk.W), padx = 10)


        def applyButton(root):
            root.config(cursor="wait")
            root.update()
            global STAGE_SHOW
            current_state = stage_boxes.state()
            for stage in STAGE_SHOW:
                STAGE_SHOW[stage] = current_state[stage]

            global LOG_DICT
            LOG_DICT = myPy.histPlotter(self.figure, EEG_STAT, STAGE_SHOW)
            canvas.show()
            root.config(cursor="")
        # Apply new stages
        apply_button = ttk.Button(master_widget, text="Apply stages", width=22, command=lambda: applyButton(self))
        apply_button.grid(column=0, row=4, sticky=(tk.W), pady = (20, 20), padx = 5)


        def logButton(root):
            root.config(cursor="wait")
            root.update()
            myPy.writeLogs(LOG_DICT, EEG_FRAGMENTS, SAVE_PATH)
            root.config(cursor="")


        log_button = ttk.Button(master_widget, text="Files in groups", width=16, command=lambda: logButton(self))
        log_button.grid(column=1, row=4, sticky=(tk.W), pady = (20, 20), padx = 5)



        exit_button = ttk.Button(master_widget, text="Exit", width=10, command=lambda: exit(0))
        exit_button.grid(column=2, row=4,  sticky=(tk.W))


app = StartPage()
app.mainloop()