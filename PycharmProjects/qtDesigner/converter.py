import os

if __name__ == "__main__":
    converter = "C:\\Python\\anaconda3\\Library\\bin\\pyuic5"
    path_to_ui = "C:\\Qt\\Qt5.10.0.1\\5.10.0\\mingw53_32\\bin"
    ui_name = "AI.ui"
    path_to_save = "E:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\qtDesigner"
    py_ui_name = "desing.py"


    os.system("{} {}\\{} -o {}\\{}".format(converter, path_to_ui, ui_name, path_to_save, py_ui_name))
    print("Complete")