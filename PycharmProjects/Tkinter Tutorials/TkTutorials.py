from tkinter import Tk, Frame, LEFT, RIGHT, W, Checkbutton, Message, Button, IntVar, Canvas, PhotoImage, E, BooleanVar
STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]

stage_ignore = {s:True for s in STAGES}
stage_ignore[0]=False
stage_ignore[1]=False
stage_ignore[2]=False
stage_ignore[3]=False




def askForStageIgnore():
    root = Tk()
    root.title("Stage ignore")
    ignore_list = {s:BooleanVar() for s in STAGES}

    def initiation():
        for s in ignore_list:
            ignore_list[s].set(not stage_ignore[s])

    initiation()

    class Checkbar(Frame):
        def __init__(self, parent, check_buttons, side=LEFT, anchor=W):
            Frame.__init__(self, parent)
            self.vars = []
            for button in check_buttons:
                chk = Checkbutton(self, text=str(button), variable=check_buttons[button])
                chk.pack(side=side, anchor=anchor)
                if (check_buttons[button].get()==True):
                    chk.select()
                self.vars.append(check_buttons[button])

        def state(self):
            return list(map(lambda var: var.get(), self.vars))


    instructions = "Select the stages that should not be taken into account in statistics." \
                   " Stage -1 is an artefacts stage which means that an eeg record was corrupted by artifacts," \
                   " stage 0 is wakefulness."
    Message(root, text=instructions, width=300).pack(anchor=W, expand=True)

    Message(root, text="Stage: ").pack(anchor=W)
    ignored_stages=Checkbar(root, ignore_list)
    ignored_stages.pack()


    def cancelAndReset():
        initiation()
        root.destroy()

    def okClick():
        for s in stage_ignore:
            stage_ignore[s]=ignore_list[s].get()
        root.destroy()

    Button(root, text="Cancel", command=cancelAndReset).pack(side=RIGHT)

    Button(root, text="Ok", command=okClick).pack(side=LEFT)

    root.mainloop()



askForStageIgnore()
print(stage_ignore)
