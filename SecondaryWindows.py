import PyQt5.QtWidgets as qtw
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import json


class CondictWindow(qtw.QMainWindow):
    def __init__(self):
        super(CondictWindow, self).__init__()

        uic.loadUi('GUI/CondictWindow.ui', self)
        self.show()

        self.combo = self.findChild(qtw.QComboBox, 'condition')
        js = open('ConditDictionary.json', 'r')
        self.conditions = json.load(js)
        js.close()
        for x in list(self.conditions.keys()):
            self.combo.addItem(x)

        self.textbox = self.findChild(qtw.QTextBrowser, 'conditDef')

        self.butt = self.findChild(qtw.QPushButton, 'defineButton')
        self.butt.clicked.connect(self.define)

    def define(self):
        defin = self.conditions[self.combo.currentText()]
        self.textbox.setText(defin)


class CharListWindow(qtw.QMainWindow):
    def __init__(self):
        super(CharListWindow, self).__init__()

        uic.loadUi('GUI/CharListWindow.ui', self)
        self.show()

        self.new = self.findChild(qtw.QPushButton, 'createChar')
        self.new.clicked.connect(lambda: self.win('new'))

    @classmethod
    def win(cls, typ):
        if typ == 'new':
            cls.charWin = CreateCharWindow()


class CreateCharWindow(qtw.QMainWindow):
    def __init__(self):
        super(CreateCharWindow, self).__init__()

        uic.loadUi('GUI/CharWindow.ui', self)
        self.show()

        self.token = self.findChild(qtw.QLabel, 'charImage')

        self.imageButton = self.findChild(qtw.QPushButton, 'findFileButton')
        self.imageButton.clicked.connect(self.getImage)

    def getImage(self):
        fname = qtw.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        self.pixmap = QPixmap(fname[0])
        self.token.setPixmap(self.pixmap)
