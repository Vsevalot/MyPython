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




class WindowMsg(tk.Tk):
    def __init__(self, label, message, *args, **kwargs,):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, label)

        master_widget = tk.Frame(self)
        master_widget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.win_width = 350
        self.win_height = 130
        self.x = int(SCREEN_WIDTH / 2 - self.win_width / 2)
        self.y = int(SCREEN_HEIGHT / 2 - self.win_height / 2)

        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))


        self.message = tk.Message(master_widget, text=message, width = self.win_width-30, font = MEDIUM_FONT)
        self.message.grid(row=0, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W),padx = 10, pady = (15,5))

        self.ok_button = ttk.Button(master_widget, text="Ok", width=10, command=self.destroy)
        self.ok_button.grid( row=1 ,column=1, sticky= tk.N, padx = 10, pady = (15,5))



class StartPage(tk.Tk):
    def escapeExit(self, event):
        self.destroy()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"EEG classification")

        self.win_width = 950
        self.win_height = 900
        self.x = 100
        self.y = 50
        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))
        self.bind('<Escape>', self.escapeExit)

        # master_widget - main widget where all others are located
        master_widget = tk.Frame(self)
        master_widget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Introduction
        introduction_txt = "This script will build pie charts of stage distribution for each classification " \
                           "group in a given csv or xlsx file. You will be able to choose which states you need " \
                           "to analyze and generate logs of file used for in each interested stage."
        introduction = tk.Message(master_widget, text=introduction_txt, font = LARGE_FONT, width=900)
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
        instructions = tk.Message(master_widget, text=instructions_txt, font = MEDIUM_FONT, width=900)
        instructions.grid(column=0, row=1, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)


        # Example of results
        first_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        canvas_results = tk.Canvas(master_widget, width=350, height=142, borderwidth=4, relief="groove")
        canvas_results.create_image(0, 75, anchor=tk.W, image=first_example)
        canvas_results.image = first_example
        canvas_results.grid(column=0, row=2, columnspan=5, sticky=(tk.N,tk.W), padx = (10,0))

        # Example of report
        second_example = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\report_examples.png")
        canvas_reports = tk.Canvas(master_widget, width=403, height=396, borderwidth=4, relief="groove")
        canvas_reports.create_image(5, 5, anchor=tk.NW,  image=second_example)
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

        add_results_button =  ttk.Button(master_widget, text="Choose", width=10, command=lambda: resultReader(self))
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

        add_results_button =  ttk.Button(master_widget, text="Choose", width=10, command=lambda: reportReader(self))
        add_results_button.grid(column=9, row=4, sticky=(tk.W))


        def buildPlotsButton(root):
            global EEG_FRAGMENTS
            global EEG_STAT

            if RESULTS==0 or REPORTS==0:
                tk.messagebox.showwarning("Not enough files","You must choose a result file "
                                                    "and report files to build plots")
                return
            root.config(cursor="wait")
            root.update()
            EEG_FRAGMENTS = myPy.matfiles2eegFragments(RESULTS, REPORTS)
            EEG_STAT = myPy.eegStat(EEG_FRAGMENTS)
            root.config(cursor="")
            root.update()
            plots = PlotPage()
            plots.mainloop()
        # Go to plot window button
        build_plots_button = ttk.Button(master_widget, text="Build plots", width=16,
                                     command=lambda: buildPlotsButton(self))
        build_plots_button.grid(column=2, row=5, sticky=(tk.W), pady = (20, 20), padx = 5)

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
        canvas.get_tk_widget().grid(column=0, row=1, columnspan=4, sticky=(tk.N, tk.W))
        canvas.show()


        stage_txt = "Stages:"
        stage_label = tk.Label(master_widget, text=stage_txt, font = MEDIUM_FONT)
        stage_label.grid(column=0, row=2, sticky=(tk.N, tk.W), padx = 10)


        stage_boxes = myPy.CheckBoxes(master_widget, STAGE_SHOW)
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


        def logButton():
            logs = LogPage()
            logs.mainloop()
        # Log window button
        log_button = ttk.Button(master_widget, text="Files in groups", width=16, command=lambda: logButton())
        log_button.grid(column=1, row=4, sticky=(tk.W), pady = (20, 20), padx = 5)


        def saveImg(self):
            if not os.path.exists(SAVE_PATH):
                os.makedirs(SAVE_PATH)
            self.figure.savefig(SAVE_PATH+"\\HIST.jpg", dpi=300)

            tk.messagebox.showinfo(parent = self, title = "Complete",
                                   message = 'Figure have been successfully saved to:\n"{}"'.format(SAVE_PATH))
        # Save img button
        save_img_button = ttk.Button(master_widget, text="Save plot", width=16, command=lambda: saveImg(self))
        save_img_button.grid(column=2, row=4,  sticky=(tk.W))

        exit_button = ttk.Button(master_widget, text="Exit", width=10, command=self.destroy)
        exit_button.grid(column=3, row=4,  sticky=(tk.W))


class LogPage(tk.Tk):
    def drawCheckButtons(self):
        i = 0
        for group in LOG_DICT:
            group_name = ttk.Label(self.check_buttons_frame, text=group, font=LARGE_FONT)
            group_name.grid(row=i, column=0, padx=10, pady=5)
            self.check_buttons[group] = (myPy.CheckBoxes(self.check_buttons_frame, LOG_DICT[group]))
            self.check_buttons[group].grid(row=i + 1, column=0, padx=5, pady=5)
            i += 2

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Log files")
        master_widget = tk.Frame(self)
        master_widget.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.instruction_text = "The script can generate logs, which will show which fragments are included to a " \
                                "stage of interest to you in different groups. By default, all stages are selected in "\
                                "groups except one with the biggest percentage in a group. All logs will be saved to: "\
                                "{}".format(SAVE_PATH)
        self.instruction = tk.Message(master_widget, text=self.instruction_text, font = MEDIUM_FONT, width=500)
        self.instruction.grid( row=0, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)

        self.check_buttons_frame = tk.Frame(master_widget)
        self.check_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.check_buttons = {}
        self.drawCheckButtons()


        def writeLogsButton(self):
            log_dict = {}
            for group in self.check_buttons:
                log_dict[group] = self.check_buttons[group].state()
            myPy.writeLogs(log_dict, EEG_FRAGMENTS, SAVE_PATH)

            tk.messagebox.showinfo(parent = self, title = "Complete",
                                   message = 'Logs have been successfully saved to:\n"{}"'.format(SAVE_PATH))
        # Save logs to SAVE PATH
        log_button = ttk.Button(master_widget, text="Write logs", width=10,
                                   command=lambda: writeLogsButton(self))
        log_button.grid(row=2, column=0, sticky=(tk.W))


        cancel_button = ttk.Button(master_widget, text="Cancel", width=10,
                                   command=self.destroy)
        cancel_button.grid(row=2, column=1, sticky=(tk.E))

        self.group_list = []


if __name__ == "__main__":
    app = StartPage()

    # get screen width and height
    SCREEN_WIDTH = app.winfo_screenwidth()
    SCREEN_HEIGHT = app.winfo_screenheight()

    app.mainloop()