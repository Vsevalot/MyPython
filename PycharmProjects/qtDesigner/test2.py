#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows text which
is entered in a QLineEdit
in a QLabel widget.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QFileDialog)





class Example(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle("File picker")
        btn = QPushButton("Choose a file", self)
        btn.clicked.connect(self.openFile)
        btn.setGeometry(100, 50, 100, 40)

        self.show()


    def openFile(self):
        name = QFileDialog.getOpenFileName(self, "Choose file")
        print(name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())