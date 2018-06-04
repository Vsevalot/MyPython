#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets, QtCore



class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(500, 400, 500, 300)
        self.setWindowTitle('Test')
        path_to_icon = "e:\\Users\\sevamunger\\Documents\\GitHub\\MyPython\\PycharmProjects\\qtDesigner\\favicon.png"
        self.setWindowIcon(QtGui.QIcon(path_to_icon))
        btn = QtWidgets.QPushButton("Quit", self)
        btn.setGeometry(150, 150, 50, 50)
        btn.clicked.connect(lambda: print(1))
        btn.setToolTip("<b>Formatted text</b> can also be displayed.")

        shaman_king_action = QtWidgets.QAction(QtGui.QIcon(path_to_icon), "&WANNA some sprit-fight?", self)
        shaman_king_action.setShortcut('Ctrl+S')
        shaman_king_action.setStatusTip('Be the shaman king')

        shaman_king_action.triggered.connect(self.ask_msg)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(shaman_king_action)

        toolbar = self.addToolBar("left")
        toolbar.addAction(shaman_king_action)
        toolbar.setOrientation(QtCore.Qt.Horizontal)
        toolbar.setMovable(False)

    def ask_msg(self):
        choice = QtWidgets.QMessageBox.question(self, "Title", "This is question",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes:
            print("AAA")
        else:
            print("BBB")



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())