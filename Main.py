import PyQt5.QtWidgets as qtw
from PyQt5 import uic
import sys


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('GUI/MainWindow.ui', self)
        self.show()


app = qtw.QApplication(sys.argv)
UIWindow = MainWindow()
sys.exit(app.exec_())