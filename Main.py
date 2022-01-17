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
        self.condictbutton.clicked.connect(lambda: self.wind('condict'))

    @classmethod
    def wind(cls, typ):
        if typ == 'condict':
            cls.condictWin = sw.CondictWindow()




app = qtw.QApplication(sys.argv)
UIWindow = MainWindo()
sys.exit(app.exec_())