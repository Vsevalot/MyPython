from tkinter import Tk
from tkinter import IntVar


root = Tk()


stage_ignore = [-1,4,5,6,7]
STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
local_stages=[v for v in STAGES if v not in stage_ignore]
groups=["group "+str(i) for i in range(10)]
groups={g:{str(s):IntVar() for s in local_stages} for g in groups}
grid_high=len(groups)+1
grid_width=len(local_stages)+1
print('a')

root.mainloop()