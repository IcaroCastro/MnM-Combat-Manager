import PyQt5.QtWidgets as qtw
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import json
import pyautogui as pag
import os

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
        self.lista = self.findChild(qtw.QListWidget, 'charList')
        self.refresh = self.findChild(qtw.QPushButton, 'refreshButton')

        self.update()

        self.refresh.clicked.connect(self.update)

    def update(self):
        self.lista.clear()
        allsheets = os.listdir('Sheets')
        form = [x.replace('.json', '') for x in allsheets]
        self.lista.addItems(form)

    @classmethod
    def win(cls, typ):
        if typ == 'new':
            cls.charWin = CreateCharWindow()


class CreateCharWindow(qtw.QMainWindow):
    def __init__(self):
        super(CreateCharWindow, self).__init__()

        uic.loadUi('GUI/CharWindow.ui', self)
        self.show()

        self.data = dict()

        self.setupWidgets()

        self.myCondits = list()

        self.add.clicked.connect(lambda: self.addCon(self.condits.currentText()))
        self.removeConButt.clicked.connect(lambda: self.remCon(self.conditList.currentItem().text()))
        self.imageButton.clicked.connect(self.getImage)
        self.savButt.clicked.connect(self.save)

        js = open('ConditDictionary.json', 'r')
        conds = json.load(js)
        js.close()
        for x in list(conds.keys()):
            self.condits.addItem(x)

    def setupWidgets(self):
        self.name = self.findChild(qtw.QLineEdit, 'charName')
        self.token = self.findChild(qtw.QLabel, 'charImage')
        self.stats1 = self.findChild(qtw.QTableWidget, 'statsTable')
        self.stats2 = self.findChild(qtw.QTableWidget, 'statsTable_2')
        self.add = self.findChild(qtw.QPushButton, 'addCondit')
        self.resMod = self.findChild(qtw.QLineEdit, 'resModVal')
        self.conditList = self.findChild(qtw.QListWidget, 'conditList')
        self.imageButton = self.findChild(qtw.QPushButton, 'findFileButton')
        self.removeConButt = self.findChild(qtw.QPushButton, 'removeCondit')
        self.condits = self.findChild(qtw.QComboBox, 'conditions')
        self.savButt = self.findChild(qtw.QPushButton, 'saveButton')

    def addCon(self, condition):
        if condition not in self.myCondits:
            self.conditList.addItem(condition)
            self.myCondits.append(condition)

    def remCon(self, condition):
        if condition:
            i = self.myCondits.index(condition)
            self.conditList.takeItem(i)
            del self.myCondits[i]

    def getImage(self):
        self.fname = qtw.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        pixmap = QPixmap(self.fname[0])
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.token.setPixmap(pixmap)

    def save(self):
        if self.checkname():
            originalImage = open(self.fname[0], 'rb')
            imageData = originalImage.read()
            newImage = open(f'Images/{self.name.text()}.png', 'wb+')
            newImage.write(imageData)
            originalImage.close()
            newImage.close()
            del originalImage, newImage
        else:
            return

        statData = list()

        for x in range(0, 8):
            tex = self.stats1.item(x, 0).text()
            if tex == '':
                tex = 0
            statData.append(int(tex))
        for y in range(0, 6):
            tex = self.stats2.item(y, 0).text()
            if tex == '':
                tex = 0
            statData.append(int(tex))

        self.data = {
            'name': self.name.text(),
            'token': f'Images/{self.name.text()}.png',
            'stats': {
                'STR': statData[0],
                'AGI': statData[1],
                'FGT': statData[2],
                'AWA': statData[3],
                'STA': statData[4],
                'DEX': statData[5],
                'INT': statData[6],
                'PRE': statData[7],
                'Dodge': statData[8],
                'Parry': statData[9],
                'Will': statData[10],
                'Fortitude': statData[11],
                'Toughness': statData[12],
                'Initiative': statData[13]
            },
            'conditions': {
                'resMod': self.resMod.text(),
                'conds': [self.conditList.item(x).text() for x in range(0, self.conditList.count())]
            }
        }

        sheet = open(f'Sheets/{self.name.text()}.json', 'w+')
        json.dump(self.data, fp=sheet, indent=1)
        sheet.close()

        pag.alert('Saved successfully')

    def checkname(self):
        if self.name.text() == '':
            pag.alert('Enter Character name.')
            return False
        else:
            return True