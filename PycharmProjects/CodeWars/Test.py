from tkinter import *

credit = 0
choice = 0

credit1 = 0
coins = 0
prices = [200,150,160,50,90]
item = 0
i = 0
temp=0
n=0
choice1 = 0
choice2 = 0

credit1 = 0
coins = 0
prices = [200,150,160,50,90]
item = 0
i = 0
temp=0
n=0
choice1 = 0
choice2 = 0


def main():
    frame = Tk()
    frame.geometry("480x360")

    Label(frame, text="Enter coins.[Press Buttons]").grid(row=1, column=1)
    display = Label(frame, text="") # we need this Label as a variable!
    display.grid(row=2, column=1)

    def add(amount):
        global credit
        credit += amount
        display.configure(text="%.2f" % credit)

    Button(frame, text="10p", command=lambda: add(.1)).grid(row=3, column=1)
    Button(frame, text="20p", command=lambda: add(.2)).grid(row=4, column=1)
    Button(frame, text="50p", command=lambda: add(.5)).grid(row=5, column=1)
    Button(frame, text="P1",  command=lambda: add(1.)).grid(row=6, column=1)
    frame.mainloop()

main()