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
KETAMINE_STAT = 0
CURRENT_PLOT = "all"
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

        master_frame = tk.Frame(self)
        master_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.win_width = 350
        self.win_height = 130
        self.x = int(SCREEN_WIDTH / 2 - self.win_width / 2)
        self.y = int(SCREEN_HEIGHT / 2 - self.win_height / 2)

        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))


        self.message = tk.Message(master_frame, text=message, width = self.win_width-30, font = MEDIUM_FONT)
        self.message.grid(row=0, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W),padx = 10, pady = (15,5))

        self.ok_button = ttk.Button(master_frame, text="Ok", width=10, command=self.destroy)
        self.ok_button.grid( row=1 ,column=1, sticky= tk.N, padx = 10, pady = (15,5))


class StartPage(tk.Tk):

    def escapeExit(self, event):
        self.destroy()

    def resultButton(self, root):
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
        self.canvas_results_state.create_image(0, 18, anchor=tk.W, image=check_img)
        self.canvas_results_state.image = check_img
        self.result_state_msg.config(text = results_text)
        root.config(cursor="")

    def reportButton(self, root):
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
            self.report_state_msg.config(text="An empty folder chosen")
            return

        check_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\ok.png")
        report_text = "Report folder selected"
        self.canvas_reports_state.create_image(0, 18, anchor=tk.W, image=check_img)
        self.canvas_reports_state.image = check_img
        self.report_state_msg.config(text = report_text)
        root.config(cursor="")

    def buildPlotsButton(self, root):
        global EEG_FRAGMENTS
        global EEG_STAT
        global KETAMINE_STAT

        if RESULTS==0 or REPORTS==0:
            tk.messagebox.showwarning("Not enough files","You must choose a result file "
                                                "and report files to build plots")
            return
        root.config(cursor="wait")
        root.update()
        EEG_FRAGMENTS = myPy.matfiles2eegFragments(RESULTS, REPORTS)
        EEG_STAT, KETAMINE_STAT = myPy.eegStat(EEG_FRAGMENTS)
        root.config(cursor="")
        root.update()
        plots = PlotPage()
        plots.mainloop()

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

        # master_frame - main widget where all others are located
        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Introduction
        introduction_txt = "This script will build pie charts of stage distribution for each classification " \
                           "group in a given csv or xlsx file. You will be able to choose which states you need " \
                           "to analyze and generate logs of file used for in each interested stage."
        self.introduction = tk.Message(self.master_frame, text=introduction_txt, font = LARGE_FONT, width=900)
        self.introduction.grid(column=0, row=0, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), pady = (15,5))

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
        self.instructions = tk.Message(self.master_frame, text=instructions_txt, font = MEDIUM_FONT, width=900)
        self.instructions.grid(column=0, row=1, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)

        # Example of results
        self.result_example_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\exampl.png")
        self.canvas_results = tk.Canvas(self.master_frame, width=350, height=142, borderwidth=4, relief="groove")
        self.canvas_results.create_image(0, 75, anchor=tk.W, image=self.result_example_img)
        self.canvas_results.image = self.result_example_img
        self.canvas_results.grid(column=0, row=2, columnspan=5, sticky=(tk.N,tk.W), padx = (10,0))

        # Example of report
        self.report_example_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\report_examples.png")
        self.canvas_reports = tk.Canvas(self.master_frame, width=403, height=396, borderwidth=4, relief="groove")
        self.canvas_reports.create_image(5, 5, anchor=tk.NW,  image=self.report_example_img)
        self.canvas_reports.image = self.report_example_img
        self.canvas_reports.grid(column=5, row=2, columnspan=5, sticky=(tk.N,tk.W))

        # No / Ok img
        no_img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\no.png")
        self.canvas_results_state = tk.Canvas(self.master_frame, width=38, height=36)
        self.canvas_results_state.create_image(0, 18, anchor=tk.W, image=no_img)
        self.canvas_results_state.image = no_img
        self.canvas_results_state.grid(column=0, row=3, sticky=(tk.E), pady = 10)

        # Result state
        no_results_text = "No file found, chose a way to the analysis file"
        self.result_state_msg = tk.Label(self.master_frame, text=no_results_text, font = MEDIUM_FONT)
        self.result_state_msg.grid(column=2, row=3, columnspan=7, sticky=(tk.W))

        # Add results button
        self.choose_results_button =  ttk.Button(self.master_frame, text="Choose", width=10,
                                                 command=lambda: self.resultButton(self))
        self.choose_results_button.grid(column=9, row=3, sticky=(tk.W))

        # No / Ok img
        self.canvas_reports_state = tk.Canvas(self.master_frame, width=38, height=36)
        self.canvas_reports_state.create_image(0, 18, anchor=tk.W, image=no_img)
        self.canvas_reports_state.image = no_img
        self.canvas_reports_state.grid(column=0, row=4, sticky=(tk.E))

        # Report state
        no_reports_text = "No report folder detected found, give a way to the reports location"
        self.report_state_msg = tk.Label(self.master_frame, text=no_reports_text, font = MEDIUM_FONT)
        self.report_state_msg.grid(column=2, row=4, columnspan=7, sticky=(tk.W))

        # Add results button
        self.add_results_button =  ttk.Button(self.master_frame, text="Choose", width=10,
                                              command=lambda: self.reportButton(self))
        self.add_results_button.grid(column=9, row=4, sticky=(tk.W))

        # Go to plot window button
        self.build_plots_button = ttk.Button(self.master_frame, text="Build plots", width=16,
                                     command=lambda: self.buildPlotsButton(self))
        self.build_plots_button.grid(column=2, row=5, sticky=(tk.W), pady = (20, 20), padx = 5)

        # Exit app button
        self.exit_button = ttk.Button(self.master_frame, text="Exit", width=10, command=lambda: exit(0))
        self.exit_button.grid(column=7, row=5,  sticky=(tk.W))


class PlotCheckBoxes(tk.Frame):
    def __init__(self, plot_page, check_dict):
        tk.Frame.__init__(self, plot_page.stage_show_frame)
        self.boxes = {}
        self.names = {}
        row = 0

        for box in check_dict:
            self.boxes[box] = ttk.Checkbutton(self, command=lambda: plot_page.applyStages(plot_page))
            self.boxes[box].state(['!alternate'])
            self.boxes[box].grid(row=row, column=0, padx= (10,0))
            if (check_dict[box] == True):
                self.boxes[box].state(['selected'])

            self.names[box] = tk.Message(self, text = myPy.STAGE_NAMES[box], width = 120,  font=("Verdana", 10))
            self.names[box].grid(row=row, column=1, sticky=(tk.N, tk.W))

            row += 1

    def state(self):
        return {box: self.boxes[box].instate(['selected']) for box in self.boxes}


class PlotRadiobuttons(tk.Frame):
    def __init__(self, plot_page):
        tk.Frame.__init__(self,  plot_page.master_frame)
        self.variants = [("All data", "all"), ("Ketamine only", "ketamine")]

        self.label = tk.Label(self, text="Current plot:")
        self.label.grid(row = 0, column= 0, sticky = (tk.N, tk.W), padx = 10, pady = 10)

        self.buttons = []
        i=1
        for plot, text in self.variants:
            self.buttons.append(ttk.Radiobutton(self, text=plot,  value=text, variable=plot_page.current_plot,
                                               command =lambda: self.choosePlot(plot_page)))
            self.buttons[-1].grid(row = i, column = 0,  sticky = (tk.N, tk.W), padx = 10, pady = 10)
            i+=1

    def choosePlot(self, plot_page):
        global CURRENT_PLOT
        CURRENT_PLOT = plot_page.current_plot.get()
        plot_page.applyStages(plot_page)



class PlotPage(tk.Tk):

    def drawUsedFiles(self):
        plot = self.used_files_figure.add_subplot(111)
        used_files = 0
        unused_files = 0
        for group in EEG_FRAGMENTS:
            for fragment in EEG_FRAGMENTS[group]:
                if fragment.stage is None:
                    unused_files+=1
                else:
                    used_files+=1
        values = [used_files, unused_files]
        names = ["Used", "Unused"]
        plot.pie(values, labels = names)
        title = "Used files ratio"
        plot.set_title(title, fontsize=10)

    def applyStages(self, root):
        root.config(cursor="wait")
        root.update()
        global STAGE_SHOW
        current_state = self.stage_boxes.state()
        for stage in STAGE_SHOW:
            STAGE_SHOW[stage] = current_state[stage]

        global LOG_DICT
        if self.current_plot.get() == "all":
            LOG_DICT = myPy.histPlotter(self.figure, EEG_STAT, KETAMINE_STAT, STAGE_SHOW)
        elif self.current_plot.get() == "ketamine":
            LOG_DICT = myPy.histPlotter(self.figure, KETAMINE_STAT, KETAMINE_STAT, STAGE_SHOW, ketamine = True)
        self.figure_canvas.show()
        root.config(cursor="")

    def saveImg(self):
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
        self.figure.savefig(SAVE_PATH + "\\HIST.jpg", dpi=300)

        tk.messagebox.showinfo(parent=self, title="Complete",
                               message='Figure have been successfully saved to:\n"{}"'.format(SAVE_PATH))

    def logButton(self):
        logs = LogPage()
        logs.mainloop()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Plots")

        self.current_plot = tk.StringVar(master=self)
        self.current_plot.set("all")
        self.win_width = SCREEN_WIDTH
        self.win_height = 1010
        self.x = -10
        self.y = 0
        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height, self.x, self.y))

        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Stage show frame
        self.stage_show_frame = tk.Frame(self.master_frame, width = 200)
        self.stage_show_frame.grid(row=0, column=0, sticky=(tk.N, tk.W))
        self.stage_show_label = ttk.Label(self.stage_show_frame, text = "Stages", font = LARGE_FONT)
        self.stage_show_label.grid(row=0, column=0, sticky=(tk.N, tk.W), padx = 10, pady = (15,10))

        # Stage chekboxes
        self.stage_boxes = PlotCheckBoxes(self, STAGE_SHOW)
        self.stage_boxes.grid(row=1, column=0, sticky=(tk.N, tk.W), padx = 10)


        # Bar subplots
        self.figure = Figure(figsize=(13.92, 7.83), dpi=100)
        global LOG_DICT
        LOG_DICT = myPy.histPlotter(self.figure, EEG_STAT, KETAMINE_STAT, STAGE_SHOW) # Which files should be logged
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.master_frame)
        self.figure_canvas.get_tk_widget().grid(row=0, column=1, rowspan = 3, columnspan=3, sticky=(tk.N, tk.W))
        self.figure_canvas.show()

        # Ketamine swapper
        self.radiobuttons = PlotRadiobuttons(self)
        self.radiobuttons.grid(row=2, column=0, sticky=(tk.N, tk.W))


        # Used files pie plot
        self.used_files_figure = Figure(figsize=(1.9, 1.9), dpi=100)
        self.drawUsedFiles()
        self.used_files_canvas = FigureCanvasTkAgg(self.used_files_figure, self.master_frame)
        self.used_files_canvas.get_tk_widget().grid(row=3, column=0, sticky=(tk.N, tk.W))
        self.used_files_canvas.show()

        # Log window button
        self.log_button = ttk.Button(self.master_frame, text="Files in groups", width=16,
                                     command=self.logButton)
        self.log_button.grid(row=3, column=1, pady = (20, 20), padx = 5)

        # Save img button
        self.save_img_button = ttk.Button(self.master_frame, text="Save plot", width=16,
                                          command=self.saveImg)
        self.save_img_button.grid(row=3, column=2, pady = (20, 20), padx = 5)

        # Close button
        self.close_button = ttk.Button(self.master_frame, text="Close", width=10, command=self.destroy)
        self.close_button.grid(row=3, column=3)


class LogPage(tk.Tk):

    def drawCheckButtons(self):
        row = 0
        column = 0
        for group in LOG_DICT:
            self.check_buttons_frame.columnconfigure(column, minsize=300)
            self.group_name = ttk.Label(self.check_buttons_frame, text=group, font=LARGE_FONT)
            self.group_name.grid(row=row, column=column,sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=5)
            self.check_buttons[group] = (myPy.CheckBoxes(self.check_buttons_frame, LOG_DICT[group]))
            self.check_buttons[group].grid(row=row + 1, column=column,sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
            column+=1
            if column==3:
                column=0
                row+=2

    def writeLogsButton(self):
        log_dict = {}
        for group in self.check_buttons:
            log_dict[group] = self.check_buttons[group].state()
        myPy.writeLogs(log_dict, EEG_FRAGMENTS, SAVE_PATH)

        tk.messagebox.showinfo(parent=self, title="Complete",
                               message='Logs have been successfully saved to:\n"{}"'.format(SAVE_PATH))

    def resetButton(self):
        for group in self.check_buttons:
            self.check_buttons[group].reset()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self,"Log files")
        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Instructions
        instruction_text = "The script can generate logs, which will show which fragments are included to a " \
                                "stage of interest to you in different groups. By default, all stages are selected in "\
                                "groups except one with the biggest percentage in a group. All logs will be saved to: "\
                                "{}".format(SAVE_PATH)
        self.instruction = tk.Message(self.master_frame, text=instruction_text, font = MEDIUM_FONT, width=930)
        self.instruction.grid( row=0, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W), padx = 10)

        # Frame for all check buttons
        self.check_buttons_frame = tk.Frame(self.master_frame, width=930)
        self.check_buttons_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Draw check buttons
        self.check_buttons = {}
        self.drawCheckButtons()

        # Save logs to result's folder button
        self.log_button = ttk.Button(self.master_frame, text="Write logs", width=10,
                               command=self.writeLogsButton)
        self.log_button.grid(row=2, column=0, sticky=(tk.N), padx=10, pady=(15,5))

        # Reset check boxes button
        self.reset_button = ttk.Button(self.master_frame, text="Reset", width=10,
                                   command=self.resetButton)
        self.reset_button.grid(row=2, column=1, sticky=(tk.N), padx=10, pady=(15,5))

        # Cancel log window button
        self.cancel_button = ttk.Button(self.master_frame, text="Cancel", width=10,
                                   command=self.destroy)
        self.cancel_button.grid(row=2, column=2, sticky=(tk.N), padx=10, pady=(15,5))


if __name__ == "__main__":
    app = StartPage()

    # get screen width and height
    SCREEN_WIDTH = app.winfo_screenwidth()
    SCREEN_HEIGHT = app.winfo_screenheight()

    app.mainloop()