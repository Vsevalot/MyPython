import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import desing  # Это наш конвертированный файл дизайна
import os

class ExampleApp(QtWidgets.QMainWindow, desing.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()