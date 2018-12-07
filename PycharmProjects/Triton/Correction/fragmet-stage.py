import sys
import os
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QFileDialog)
from reportlib import Fragment, ReportAI


class CorrectionApp(QWidget):


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
        path_to_errors = QFileDialog.getExistingDirectory(self, "Choose file", "Z:/Tetervak/skipped")
        print(path_to_errors)
        if path_to_errors == '':  # if no file selected
            return
        exit(33)
        path_to_folder = '/'.join(path_to_errors.split('/')[:-1])  # drop file from path










        path_to_reports = "Z:/Tetervak/Reports/reports 2.0/todo"
        reports = [ReportAI(os.path.join(path_to_reports, f)) for f in os.listdir(path_to_reports)]
        reports = {r.name: r for r in reports}

        path_to_fragments = "Z:/Tetervak/fragments/All_fragments_15_sec.csv"
        fragment_names = []
        with open(path_to_fragments, 'r') as f:
            for line in f:
                fragment_names.append(line[:-1])
            f.close()

        fragments = [Fragment(f) for f in fragment_names]

        path_to_save = "Z:/Tetervak/file - stage/File-stage_AI_15sec.csv"
        with open(path_to_save, 'w') as f:
            f.write("fragment;ai\n")
            for fragment in fragments:
                record = fragment.name.split('_')[0]
                if record in reports:
                    fragment.ai = reports[record].fragmentAI(fragment.start, fragment.end)
                    f.write("{};{}\n".format(fragment.name, fragment.ai))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CorrectionApp()
    sys.exit(app.exec_())


