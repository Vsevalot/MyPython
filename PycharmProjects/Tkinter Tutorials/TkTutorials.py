import tkinter as tk

def idk(root):
    root.master.destroy

root = tk.Tk()

introduction = "This script will build histograms of stage distribution for each column in a given csv or xlsx file."
intr = tk.Message(root, width=750, text = introduction)
intr.config(font=(12))
intr.grid(row = 0, ipadx = 15, ipady = 15, sticky=tk.W)


instructions = "Please check that all eeg fragments are named like:\n" \
               "folder name_YYYYMMDD_hh.mm.ss(start seconds from beginning-finish seconds from beginning)\n\n" \
               "Example:"
inst = tk.Message(root, width=750, text = instructions)
inst.config(font=("times", 14))
inst.grid(row=1, ipadx = 15,sticky=tk.W)


canvas_width = 770
canvas_height = 142
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, borderwidth=4, relief="groove")
canvas.grid(row=2, padx = 10)
img = tk.PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\example.png")
canvas.create_image(5,75, anchor=tk.W, image=img)

continue_button = tk.Button(root, text="Exit", width=10, command=root.destroy, borderwidth=3)
continue_button.grid(row=3, column = 0, sticky=tk.E, padx=20, pady=10)
exit_button = tk.Button(root, text="Continue", width=16, command=idk(root) ,borderwidth=3)
exit_button.grid(row=3, column = 0, sticky=tk.W, padx=40, pady=10)

root.title("EEG fragments analysis helper")
root.mainloop()