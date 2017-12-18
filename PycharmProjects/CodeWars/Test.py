import tkinter as tk
from tkinter import ttk
root = tk.Tk()

v = tk.StringVar()
v.set("all")

current_plot = [
    ("All stages" , "all"),
    ("Ketamine only" , "ketamine"),
]

def ShowChoice():
    print(v.get())

tk.Label(root,
         text="""Choose your favourite 
programming language:""",
         justify = tk.LEFT,
         padx = 20).pack()

for plot, text in current_plot:
    tk.Radiobutton(root,
                  text=plot,
                  padx = 20,
                  variable=v,
                  command=ShowChoice,
                  value=text, indicatoron= 0).pack(anchor=tk.W)


root.mainloop()