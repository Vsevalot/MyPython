from tkinter import *
from tkinter.constants import *

master= Tk()
master.resizable(width=False, height=False)

#for erasing displayed text when not needed anymore
wordsShowing = 0


#for testing button function with map movement
#url for image is http://files.softicons.com/download/game-icons/minecraft-avatars-icons-by-stefan-kroeber/png/50x50/slime.png if you want to see exactly what im seeing
pic = PhotoImage(file="C:\\Users\\Bill\\Desktop\\Python\\Final\\slime.png")
image = Label(master, image=pic)
image.grid(row=0, column=3, columnspan=1, rowspan=1, padx=0, pady=0)


#button functions (im not sure which buttons we will actually be using but im trying to cover all our bases)
def left():
    while wordsShowing == 1:
        varLabel.grid_remove()
        wordsShowing = 0
    info = image.grid_info()
    move = info["column"]
    stay = info["row"]
    if move > 0:
        image.grid_remove()
        image.grid(row=stay, column=move-1, columnspan=1, rowspan=1, padx=0, pady=0)
    else:
        varLabel = Label(master, text='Sorry, you can not go that direction.')
        varLabel.grid(row=1, column=2, rowspan=4)
        wordsShowing = 1
    global wordsShowing
    global varLabel

def right():
    while wordsShowing == 1:
        varLabel.grid_remove()
        wordsShowing = 0
    info = image.grid_info()
    move = info["column"]
    stay = info["row"]
    if move < 4:
        image.grid_remove()
        image.grid(row=stay, column=move+1, columnspan=1, rowspan=1, padx=0, pady=0)
    else:
        varLabel = Label(master, text='Sorry, you can not go that direction.')
        varLabel.grid(row=1, column=2, rowspan=4)
        wordsShowing = 1
    global wordsShowing
    global varLabel


def down():
    while wordsShowing == 1:
        varLabel.grid_remove()
        wordsShowing = 0
    info = image.grid_info()
    move = info["row"]
    stay = info["column"]
    if move < 5:
        image.grid_remove()
        image.grid(row=move+1, column=stay, columnspan=1, rowspan=1, padx=0, pady=0)
    else:
        varLabel = Label(master, text='Sorry, you can not go that direction.')
        varLabel.grid(row=1, column=2, rowspan=4)
        wordsShowing = 1
    global wordsShowing
    global varLabel


def up():
    while wordsShowing == 1:
        varLabel.grid_remove()
    wordsShowing = 0
    info = image.grid_info()
    move = info["row"]
    stay = info["column"]
    if move > 0:
        image.grid_remove()
        image.grid(row=move-1, column=stay, columnspan=1, rowspan=1, padx=0, pady=0)
    else:
        varLabel = Label(master, text='Sorry, you can not go that direction.')
        varLabel.grid(row=1, column=2, rowspan=4)
        wordsShowing = 1
    global wordsShowing
    global varLabel


def submit():
    var = command.get()
    varLabel = Label(master, text=var)
    varLabel.grid(row=1, column=2, rowspan=4)
    wordsShowing = 1
    global wordsShowing
    global varLabel


#created widgets
label1 = Label(master, text="Enter a command:")
command = Entry(master, width=80)
leftButton = Button(master, text="<", command=left)
rightButton = Button(master, text=">", command=right)
downButton = Button(master, text="v", command=down)
upButton = Button(master, text="^", command=up)
submitButton = Button(master, text="SUBMIT", command=submit)

#display widgets
label1.grid(row=5, column=1, sticky=E)
command.grid(row=5, column=2)
leftButton.grid(row=2, column=2, sticky=E, padx=3)
rightButton.grid(row=2, column=3)
downButton.grid(row=3, column=3, sticky=W)
upButton.grid(row=1, column=3, sticky=W)
submitButton.grid(row=5, column=3, pady=5, padx=5)