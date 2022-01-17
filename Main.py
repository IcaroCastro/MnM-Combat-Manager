import PyQt5.QtWidgets as qtw
from PyQt5 import uic
import sys
import SecondaryWindows as sw


class MainWindo(qtw.QMainWindow):
    def __init__(self):
        super(MainWindo, self).__init__()

        uic.loadUi('GUI/MainWin.ui', self)
        self.show()

        self.condictbutton = self.findChild(qtw.QPushButton, 'openDict')
        self.charsbutton = self.findChild(qtw.QPushButton, 'openChars')
        self.initbutton = self.findChild(qtw.QPushButton, 'openInit')

        self.condictbutton.clicked.connect(lambda: self.wind('condict'))
        self.charsbutton.clicked.connect(lambda: self.wind('chars'))
        self.initbutton.clicked.connect(lambda: self.wind('init'))

    @classmethod
    def wind(cls, typ):
        if typ == 'condict':
            cls.condictWin = sw.CondictWindow()
        elif typ == 'chars':
            cls.charsWin = sw.CharListWindow()




app = qtw.QApplication(sys.argv)
UIWindow = MainWindo()
sys.exit(app.exec_())