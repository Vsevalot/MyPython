#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets, QtCore
import time


class Window(QtWidgets.QMainWindow):

    def buttonAction(self):
        progress_value = 0
        while progress_value < 100:
            progress_value += 1
            self.progressbar.setValue(progress_value)
            time.sleep(0.01)

        QtWidgets.QMessageBox.information(self,"Title", "Text")



    def askingWindow(self):
        choice = QtWidgets.QMessageBox.question(self, "Title", "This is question",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes:
            print("AAA")
        else:
            print("BBB")

    def checkboxChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Checked")
        else:
            print("Unchecked")

    def comboboxChanged(self, state):
        self.lbl.setText(state)
        self.lbl.adjustSize()


    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(500, 400, 500, 300) # window settings
        self.setWindowTitle('Test')
        path_to_icon = "e:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\qtDesigner\\favicon.png"
        self.setWindowIcon(QtGui.QIcon(path_to_icon))

        # Menu
        self.statusBar()
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')

        self.first_menu_action = QtWidgets.QAction(QtGui.QIcon(path_to_icon), "&menu action 1", self)
        self.first_menu_action.triggered.connect(self.askingWindow)
        self.fileMenu.addAction(self.first_menu_action)
        self.second_menu_action = QtWidgets.QAction(QtGui.QIcon(path_to_icon), "&menu action 2", self)
        self.second_menu_action.triggered.connect(lambda: print("Second menu action pressed"))
        self.fileMenu.addAction(self.second_menu_action)


        # Toolbar
        self.toolbar = self.addToolBar("down") # creates toolbar

        self.toolbar_action = QtWidgets.QAction(QtGui.QIcon(path_to_icon), "&action name", self)
        self.toolbar_action.setShortcut('Ctrl+S')
        self.toolbar_action.setStatusTip('Toolbar action status tip')
        self.toolbar.addAction(self.toolbar_action)

        self.toolbar.setOrientation(QtCore.Qt.Horizontal)
        self.toolbar.setMovable(False)


        # Button
        self.btn = QtWidgets.QPushButton("Button\nname", self)
        self.btn.setGeometry(150, 60, 50, 50)
        self.btn.clicked.connect(self.buttonAction)
        self.btn.setToolTip("<b>Formatted text</b> can also be displayed.")


        # Progress bar
        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setGeometry(250, 60, 250, 20)


        # Checkbox
        self.checkbox = QtWidgets.QCheckBox("Checkbox name", self)
        self.checkbox.move(10, 55)
        self.checkbox.toggle()
        self.checkbox.stateChanged.connect(self.checkboxChanged)


        # Label
        self.lbl = QtWidgets.QLabel("Label text", self)
        self.lbl.move(20, 80)


        # Combobox
        self.combobox = QtWidgets.QComboBox(self)
        for i in range(10):
            self.combobox.addItem("{} item".format(i))
        self.combobox.move(20, 120)
        self.combobox.activated[str].connect(self.comboboxChanged)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())