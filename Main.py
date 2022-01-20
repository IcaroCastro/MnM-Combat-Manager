import PyQt5.QtWidgets as qtw
from PyQt5 import uic
import sys
import SecondaryWindows as sw


# Main Window hub for access to all other windows and funcionalities

class MainWindo(qtw.QMainWindow):
    def __init__(self):
        super(MainWindo, self).__init__()

        # Loading UI
        uic.loadUi('GUI/MainWin.ui', self)
        self.show()

        # Importing objects from UI
        self.condictbutton = self.findChild(qtw.QPushButton, 'openDict')
        self.charsbutton = self.findChild(qtw.QPushButton, 'openChars')
        self.initbutton = self.findChild(qtw.QPushButton, 'openInit')

        # Connecting objects from UI to funcions
        self.condictbutton.clicked.connect(lambda: self.wind('condict'))
        self.charsbutton.clicked.connect(lambda: self.wind('chars'))
        self.initbutton.clicked.connect(lambda: self.wind('init'))

    # Function for opening other Windows
    @classmethod
    def wind(cls, typ):
        if typ == 'condict':
            cls.condictWin = sw.CondictWindow()
        elif typ == 'chars':
            cls.charsWin = sw.CharListWindow()
        else:
            cls.initWin = sw.InitWindow()


# Code for running the class above
app = qtw.QApplication(sys.argv)
UIWindow = MainWindo()
sys.exit(app.exec_())