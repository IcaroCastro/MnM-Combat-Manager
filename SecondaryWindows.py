import PyQt5.QtWidgets as qtw
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import json
from pyautogui import alert
import os
import CombatLib as cl


# Window for the condiction dictionary function
class CondictWindow(qtw.QMainWindow):
    def __init__(self):
        super(CondictWindow, self).__init__()

        # Loading UI
        uic.loadUi('GUI/CondictWindow.ui', self)
        self.show()

        # Importing objects from UI
        self.combo = self.findChild(qtw.QComboBox, 'condition')
        self.textbox = self.findChild(qtw.QTextBrowser, 'conditDef')
        self.butt = self.findChild(qtw.QPushButton, 'defineButton')

        # Importing conditions and definitions from 'ConditDictionary.json' file
        js = open('ConditDictionary.json', 'r')
        self.conditions = json.load(js)
        js.close()
        for x in list(self.conditions.keys()):
            self.combo.addItem(x)

        # Connecting UI button object to method
        self.butt.clicked.connect(self.define)

    # Method for displaying the condition definition on screen
    def define(self):
        # Fetching selected condition and it's definition according to 'ConditDictionary.json'
        defin = self.conditions[self.combo.currentText()]
        # Displaying text on screen
        self.textbox.setText(defin)


# Window for List of Characters
class CharListWindow(qtw.QMainWindow):
    def __init__(self):
        super(CharListWindow, self).__init__()

        # Importing UI
        uic.loadUi('GUI/CharListWindow.ui', self)
        self.show()

        # Importing objects from UI
        self.new = self.findChild(qtw.QPushButton, 'createChar')
        self.lista = self.findChild(qtw.QListWidget, 'charList')
        self.refresh = self.findChild(qtw.QPushButton, 'refreshButton')
        self.opener = self.findChild(qtw.QPushButton, 'openChar')

        # Displaying already existant characters on screen
        self.update()

        # Connecting objects to methods
        self.refresh.clicked.connect(self.update)
        self.new.clicked.connect(lambda: self.win('new'))
        self.opener.clicked.connect(lambda: self.win('op', self.lista.currentItem()))

    # Method for updating list of characters on screen
    def update(self):
        self.lista.clear()  # Erasing list
        allsheets = os.listdir('Sheets')  # Fetching all files on directory 'Sheets/'
        form = [x.replace('.json', '') for x in allsheets]  # Removing file extension
        self.lista.addItems(form)  # Displaying filenames on screen

    # Method for opening other windows
    @classmethod
    def win(cls, typ, item=None):
        if typ == 'new':
            cls.newCharWin = CreateCharWindow()
        elif typ == 'op':
            if item:
                cls.opCharWin = OpenCharWindow(item.text())
            else:
                alert('Please select a character')


# Window for loading already existent character sheet
class OpenCharWindow(qtw.QMainWindow):
    def __init__(self, charname):
        super(OpenCharWindow, self).__init__()

        # Importing UI
        uic.loadUi('GUI/CharWindow.ui', self)
        self.show()

        # Setting important attributes
        self.fname = ''
        self.myCondits = list()

        # Method for importing and setting up objects from UI
        self.setupWidgets()

        # Connecting object from UI to method
        self.wheel.valueChanged.connect(self.updateResMod)

        # Method for loading information from character file
        self.loadfile(charname)

        # Connecing objects from UI to methods
        self.add.clicked.connect(lambda: self.addCon(self.condits.currentText()))
        self.removeConButt.clicked.connect(lambda: self.remCon(self.conditList.currentItem().text()))
        self.imageButton.clicked.connect(self.getImage)
        self.savButt.clicked.connect(self.save)

    # Method for importing and setting up Objects from UI
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

        # Extracting condition names from 'ConditDictionary.json' and displaying in combo box
        js = open('ConditDictionary.json', 'r')
        conds = json.load(js)
        js.close()
        for x in list(conds.keys()):
            self.condits.addItem(x)

    # Method for loading information from character file
    def loadfile(self, charac):
        # Importing information from json file
        file = open(f'Sheets/{charac}.json', 'r')
        self.data = json.load(file)
        file.close()
        del file

        # Setting up stats table from information in self.data
        for x, y in enumerate(self.data['stats'].values()):
            if x < 8:
                self.stats1.item(x, 0).setText(str(y))
            else:
                self.stats2.item(x - 8, 0).setText(str(y))

        # Displaying image on screen
        self.fname = self.data['token']
        pixmap = QPixmap(self.fname)
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.token.setPixmap(pixmap)

        # Displaying name and adjusting dial position
        self.name.setText(self.data['name'])
        self.wheel.setValue(self.data['conditions']['resMod'])

        # Displaying conditions
        for x in self.data['conditions']['conds']:
            self.addCon(x)

    # Method for updating Resistance Modifier live
    def updateResMod(self):
        val = self.wheel.value()
        self.resMod.setText(str(val))

    # Method for adding conditions to condition list
    def addCon(self, condition):
        if condition not in self.myCondits:
            self.conditList.addItem(condition)
            self.myCondits.append(condition) # 'self.myCondits' exist to avoid multiple entries of the same condition

    # Method for removing conditions from condition list
    def remCon(self, condition):
        if condition:
            i = self.myCondits.index(condition)
            self.conditList.takeItem(i)
            del self.myCondits[i]

    # Method for importing image file from any directory and displaying on screen
    def getImage(self):
        self.fname = qtw.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        pixmap = QPixmap(self.fname[0])
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        self.token.setPixmap(pixmap)

    # Method for checking if client has entered character name before saving
    def checkname(self):
        if self.name.text() == '':
            alert('Enter Character name.')
            return False
        else:
            return True

    # Method for saving information from UI into json file for storage
    def save(self):
        if self.checkname():  # Checking if client has entered character name for file and image name
            if self.fname != self.data['token']:  # If client has choses another picture from saved, override
                originalImage = open(self.fname[0], 'rb')  # Copying data from original file
                imageData = originalImage.read()
                newImage = open(f'Images/{self.name.text()}.png', 'wb+')
                newImage.write(imageData)  # Pasting data in 'Images/' directory
                originalImage.close()
                newImage.close()
                del originalImage, newImage
        else:
            return

        statData = list()

        # Importing data from QTableWidget's in UI
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

        # Dictionary containing all data from UI
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

        # Saving data to json file
        sheet = open(f'Sheets/{self.name.text()}.json', 'w+')
        json.dump(self.data, fp=sheet, indent=2)
        sheet.close()

        alert('Saved successfully')


# Window for creating character (almost equal to OpenCharWindow)
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


# Window for initiative list
class InitWindow(qtw.QMainWindow):
    def __init__(self):
        super(InitWindow, self).__init__()

        # Loading Ui
        uic.loadUi('GUI/InitWindow.ui', self)
        self.show()

        # Importing objects from UI
        self.adder = self.findChild(qtw.QPushButton, 'addChar')
        self.lista = self.findChild(qtw.QListWidget, 'charList')
        self.combo = self.findChild(qtw.QComboBox, 'charCombo')
        self.refresh = self.findChild(qtw.QPushButton, 'refresh')
        self.remove = self.findChild(qtw.QPushButton, 'removeChar')
        self.delayer = self.findChild(qtw.QPushButton, 'delay')
        self.delayIndex = self.findChild(qtw.QLineEdit, 'delayIndex')
        self.hc = self.findChild(qtw.QLineEdit, 'healCheck')
        self.dr = self.findChild(qtw.QLineEdit, 'dmgRank')
        self.rc = self.findChild(qtw.QLineEdit, 'resCheck')
        self.damager = self.findChild(qtw.QPushButton, 'damage')
        self.healer = self.findChild(qtw.QPushButton, 'heal')

        # Method for displaying character names in combo box
        self.setupBox()

        # Connecting objects from UI to methods
        self.adder.clicked.connect(self.add)
        self.refresh.clicked.connect(self.setupBox)
        self.remove.clicked.connect(self.remover)
        self.delayer.clicked.connect(self.dela)
        self.damager.clicked.connect(self.dmg)
        self.healer.clicked.connect(self.hp)

    # Method for displaying character names in combo box
    def setupBox(self):
        self.combo.clear()  # Erasing all items in combo box
        # Adding all files form 'Sheets/' directory without file extension
        self.combo.addItems([x.replace('.json', '') for x in os.listdir('Sheets')])

    # Method for including character in initiative list
    def add(self):
        char = self.combo.currentText()  # Fetching selected character
        item = qtw.QListWidgetItem()  # Creating item for QListWidget (self.lista)
        item.setText(char)  # Setting item text to selected character name

        # Method for determining and setting item icon
        self.checkIcon(item)

        # Adding item to initiative list
        self.lista.addItem(item)

    # Method for removing character from initiative list
    def remover(self):
        char = self.lista.currentRow()  # Fetching selected row
        if char or char == 0:  # Avoiding ValueErrors for deleting 'None' and bug where program can't delete 0th item
            return self.lista.takeItem(char)  # Removing selected row from list

    # Method for determining and setting item icon
    def checkIcon(self, item):
        name = item.text()  # Fetching character name

        # Importing character sheet from 'Sheets/' direcotry
        js = open(f'Sheets/{name}.json', 'r')
        data = json.load(js)
        js.close()

        condits = data['conditions']['conds']

        # Determining character worst condition and assigning corresponding icon from directory 'ConditIcons/'
        if 'DEAD' in condits:
            item.setIcon(QIcon('ConditIcons/7.png'))
        elif 'Dying' in condits:
            item.setIcon(QIcon('ConditIcons/6.png'))
        elif 'Incapacitated' in condits:
            item.setIcon(QIcon('ConditIcons/5.png'))
        elif 'Staggered(DMG)' in condits:
            item.setIcon(QIcon('ConditIcons/4.png'))
        elif 'Dazed(DMG)' in condits:
            item.setIcon(QIcon('ConditIcons/3.png'))
        elif data['conditions']['resMod'] != 0:
            item.setIcon(QIcon('ConditIcons/2.png'))
        else:
            item.setIcon(QIcon('ConditIcons/1.png'))

        del data, js

    # Method for changing itiative order
    def dela(self):
        row = self.lista.currentRow()  # Fetching selected row in list
        try:
            newplace = int(self.delayIndex.text())  # Fetching desired new position in list
        except ValueError:
            alert('Please insert a non-negative integer.')
            return
        if row:  # Avoiding errors caused by interacting with 'None' object
            item = self.lista.takeItem(row)  # Removing item from list and importing to 'item' variable
            # Placing item in desired index, correting for 0-indexing of list
            self.lista.insertItem(newplace - 1, item)

    # Method for appling damage
    def dmg(self):
        try:
            dmgrnk = int(self.dr.text())  # Fetching damage rank from UI
            rescheck = int(self.rc.text())  # Fetching resistance check result from UI
        except ValueError:
            alert('Please insert integer values')
            return
        char = self.lista.currentItem()  # Fetching character to be damaged
        if char:  # Avoiding errors caused for interacting with 'None' object
            cl.damage(dmgrnk, rescheck, char.text())  # Appling function from 'CombatLib.py'
            self.checkIcon(char)  # Method for determining and setting item icon

    # Method for healing
    def hp(self):
        try:
            hel = int(self.hc.text())  # Fetching healing check result from UI
        except ValueError:
            alert('Please insert integer value')
            return
        char = self.lista.currentItem()  # Fetching character to be healed
        if char:  # Avoiding errors caused by interacting with 'None' object
            cl.heal(hel, char.text())  # Appling function from 'CombatLib.py'
            self.checkIcon(char)  # Method for determining and setting item icon