#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())