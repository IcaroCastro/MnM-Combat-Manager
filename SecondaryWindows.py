import PyQt5.QtWidgets as qtw
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import json
from pyautogui import alert
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
        self.lista = self.findChild(qtw.QListWidget, 'charList')
        self.refresh = self.findChild(qtw.QPushButton, 'refreshButton')
        self.opener = self.findChild(qtw.QPushButton, 'openChar')

        self.update()

        self.refresh.clicked.connect(self.update)
        self.new.clicked.connect(lambda: self.win('new'))
        self.opener.clicked.connect(lambda: self.win('op', self.lista.currentItem()))

    def update(self):
        self.lista.clear()
        allsheets = os.listdir('Sheets')
        form = [x.replace('.json', '') for x in allsheets]
        self.lista.addItems(form)

    @classmethod
    def win(cls, typ, item=None):
        if typ == 'new':
            cls.newCharWin = CreateCharWindow()
        elif typ == 'op':
            if item:
                cls.opCharWin = OpenCharWindow(item.text())
            else:
                alert('Please select a character')


class OpenCharWindow(qtw.QMainWindow):
    def __init__(self, charname):
        super(OpenCharWindow, self).__init__()

        uic.loadUi('GUI/CharWindow.ui', self)
        self.show()

        self.fname = ''
        self.myCondits = list()

        self.setupWidgets()

        self.wheel.valueChanged.connect(self.updateResMod)

        self.loadfile(charname)

        self.add.clicked.connect(lambda: self.addCon(self.condits.currentText()))
        self.removeConButt.clicked.connect(lambda: self.remCon(self.conditList.currentItem().text()))
        self.imageButton.clicked.connect(self.getImage)
        self.savButt.clicked.connect(self.save)

    def setupWidgets(self):
        self.name = self.findChild(qtw.QLineEdit, 'charName')
        self.token = self.findChild(qtw.QLabel, 'charImage')
        self.stats1 = self.findChild(qtw.QTableWidget, 'statsTable')
        self.stats2 = self.findChild(qtw.QTableWidget, 'statsTable_2')
        self.add = self.findChild(qtw.QPushButton, 'addCondit')
        self.conditList = self.findChild(qtw.QListWidget, 'conditList')
        self.imageButton = self.findChild(qtw.QPushButton, 'findFileButton')
        self.removeConButt = self.findChild(qtw.QPushButton, 'removeCondit')
        self.condits = self.findChild(qtw.QComboBox, 'conditions')
        self.savButt = self.findChild(qtw.QPushButton, 'saveButton')
        self.wheel = self.findChild(qtw.QDial, 'resModDial')
        self.resMod = self.findChild(qtw.QLabel, 'resModDisplay')

        js = open('ConditDictionary.json', 'r')
        conds = json.load(js)
        js.close()
        for x in list(conds.keys()):
            self.condits.addItem(x)

    def loadfile(self, charac):
        file = open(f'Sheets/{charac}.json', 'r')
        self.data = json.load(file)
        file.close()
        del file

        for x, y in enumerate(self.data['stats'].values()):
            if x < 8:
                self.stats1.item(x, 0).setText(str(y))
            else:
                self.stats2.item(x - 8, 0).setText(str(y))

        self.fname = self.data['token']
        pixmap = QPixmap(self.fname)
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.token.setPixmap(pixmap)

        self.name.setText(self.data['name'])
        self.wheel.setValue(self.data['conditions']['resMod'])

        for x in self.data['conditions']['conds']:
            self.addCon(x)

    def updateResMod(self):
        val = self.wheel.value()
        self.resMod.setText(str(val))

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

    def checkname(self):
        if self.name.text() == '':
            alert('Enter Character name.')
            return False
        else:
            return True

    def save(self):
        if self.checkname():
            if self.fname != self.data['token']:
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
                'resMod': int(self.resMod.text()),
                'conds': [self.conditList.item(x).text() for x in range(0, self.conditList.count())]
            }
        }

        sheet = open(f'Sheets/{self.name.text()}.json', 'w+')
        json.dump(self.data, fp=sheet, indent=2)
        sheet.close()

        alert('Saved successfully')


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
        self.wheel.valueChanged.connect(self.updateResMod)


    def setupWidgets(self):
        self.name = self.findChild(qtw.QLineEdit, 'charName')
        self.token = self.findChild(qtw.QLabel, 'charImage')
        self.stats1 = self.findChild(qtw.QTableWidget, 'statsTable')
        self.stats2 = self.findChild(qtw.QTableWidget, 'statsTable_2')
        self.add = self.findChild(qtw.QPushButton, 'addCondit')
        self.conditList = self.findChild(qtw.QListWidget, 'conditList')
        self.imageButton = self.findChild(qtw.QPushButton, 'findFileButton')
        self.removeConButt = self.findChild(qtw.QPushButton, 'removeCondit')
        self.condits = self.findChild(qtw.QComboBox, 'conditions')
        self.savButt = self.findChild(qtw.QPushButton, 'saveButton')
        self.wheel = self.findChild(qtw.QDial, 'resModDial')
        self.resMod = self.findChild(qtw.QLabel, 'resModDisplay')

        js = open('ConditDictionary.json', 'r')
        conds = json.load(js)
        js.close()
        for x in list(conds.keys()):
            self.condits.addItem(x)

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
                'resMod': int(self.resMod.text()),
                'conds': [self.conditList.item(x).text() for x in range(0, self.conditList.count())]
            }
        }

        sheet = open(f'Sheets/{self.name.text()}.json', 'w+')
        json.dump(self.data, fp=sheet, indent=2)
        sheet.close()

        alert('Saved successfully')

    def updateResMod(self):
        val = self.wheel.value()
        self.resMod.setText(str(val))

    def checkname(self):
        if self.name.text() == '':
            alert('Enter Character name.')
            return False
        else:
            return True