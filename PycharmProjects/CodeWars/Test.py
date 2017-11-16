from tkinter import Tk, Frame, LEFT, RIGHT, W, Checkbutton, Message, Button, BooleanVar
import copy


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]

local_stages = [0,1,2,3]

def checkBarWindow():
    if local_stages == []:
        return
    class Checkbar(Frame):
       def __init__(self, parent, check_buttons, side=LEFT, anchor=W):
           Frame.__init__(self, parent)
           self.vars = []
           for button in check_buttons:
               chk = Checkbutton(self, text=button, variable=check_buttons[button])
               chk.pack(side=side, anchor=anchor)
               if (check_buttons[button].get()==True):
                   chk.select()
               self.vars.append(check_buttons[button])

       def state(self):
           return list(map(lambda var: var.get(), self.vars))


    root = Tk()
    root.title("Reports generating")


    instructions = "Select the elements in the groups for which you want to generate reports with the names of the files"
    Message(root, text=instructions).pack(anchor=W)



    groups=["group "+str(i) for i in range(4)]
    groups={group:{str(stage):BooleanVar() for stage in local_stages} for group in groups}
    groups["group 1"]['0'].set(True)


    interested_stages=[]
    for group in groups:
        Message(root, text=group).pack(anchor=W)
        interested_stages.append(Checkbar(root, groups[group]))
        interested_stages[-1].pack()


    def cancelAndReset():
        for g in groups:
            for s in groups[g]:
                groups[g][s].set(False)
        root.destroy()

    Button(root, text="Cancel", command=cancelAndReset).pack(side=RIGHT)

    Button(root, text="Ok", command=root.destroy).pack(side=LEFT)


    root.mainloop()

    for g in groups:
        for s in groups[g]:
            groups[g][s]=groups[g][s].get()

    return groups


x=checkBarWindow()
print(x)