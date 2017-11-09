import tkinter as tk

root = tk.Tk()
introduction = "This script will build histograms of stage distribution for each column in given csv or " \
               "xlsx file."
intr = tk.Message(root,width=450, text = introduction)
intr.config(font=("times", 12))
intr.pack()
instructions = "Please check that eeg fragments named like: folderName_YYYYMMDD_hh.mm.ss(startSecondsFromBeginning-" \
               "finishSecondsFromBeginning), example: tritonRecs_19991231_23.15.40(127-183)"
inst = tk.Message(root,width=450, text = instructions)
inst.config(font=("times", 12))
inst.pack()


canvas_width = 900
canvas_height =300


canvas = tk.Canvas(root,
           width=canvas_width,
           height=canvas_height)
canvas.pack()

img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\example.png")
canvas.create_image(20,100, anchor=tk.W, image=img)


root.title("EEG fragments analysis helper")
label = tk.Label(root, fg="darkgreen")
label.pack()
button = tk.Button(root, text="Ok", width=25, command=root.destroy)
button.pack()
root.mainloop()