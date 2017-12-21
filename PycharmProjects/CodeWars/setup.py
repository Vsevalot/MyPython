import cx_Freeze
import sys
import os
import matplotlib

base = None

os.environ['TCL_LIBRARY'] = r'C:\Python\anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python\anaconda3\tcl\tk8.6'

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("E:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\CodeWars\\TTTT.py", base=base)]
images = ["e:\\Users\\sevamunger\\Desktop\\ok.png","e:\\Users\\sevamunger\\Desktop\\no.png",
          "e:\\Users\\sevamunger\\Desktop\\exampl.png", "e:\\Users\\sevamunger\\Desktop\\report_examples.png",
          "e:\\Users\\sevamunger\\Desktop\\check.png", "e:\\Users\\sevamunger\\Desktop\\radio.png",
          "e:\\Users\\sevamunger\\Desktop\\err2.png",
          "E:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\CodeWars\\MyPyFuncs.py"]
cx_Freeze.setup(
    namme = "Classification viewer",
    options = {"build_exe":{"packages":["tkinter", "matplotlib"], "include_files":images}},
    version = "0.01",
    description = "Best app ever",
    executables = executables
)
