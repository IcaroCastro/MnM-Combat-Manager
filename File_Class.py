class File:
    def __init__(self):
        self.circ = 0
        self.circ_comm = str()
        self.incapac = ''
        self.conds = list()
        self.dmgc = list()
        self.dmgpe = 0
        self.stabdice = [0, 0]
        self.stats = {'STR': '',
                      'AGI': '',
                      'FGT': '',
                      'AWA': '',
                      'STA': '',
                      'DEX': '',
                      'INT': '',
                      'PRE': '',
                      'DODGE': '',
                      'PARRY': '',
                      'FORTITUDE': '',
                      'TOUGHNESS': '',
                      'WILL': '',
                      'init': ''}

        self.name = input('Character Name: ')
        try:
            self.getstats(self.name)
        except FileNotFoundError:
            self.register(self.name)

    def getstats(self, name):
        file = open(f'Sheets/{name}.txt', 'r')
        data = file.read()
        treat = data.split('\n')
        file.close()
        del data, file
        for stat in treat:
            for key in self.stats.keys():
                if key in stat:
                    self.stats[key] = int(stat.split(' ')[1])

    def register(self, name):
        file = open(f'Sheets/{name}.txt', 'a+')
        while True:
            try:
                self.stats = {'STR': int(input('Strength: ')),
                              'AGI': int(input('Agility: ')),
                              'FGT': int(input('Fighting: ')),
                              'AWA': int(input('Awareness: ')),
                              'STA': int(input('Stamina: ')),
                              'DEX': int(input('Dexterity: ')),
                              'INT': int(input('Intellect: ')),
                              'PRE': int(input('Presence: ')),
                              'DODGE': int(input('Dodge: ')),
                              'PARRY': int(input('Parry: ')),
                              'FORTITUDE': int(input('Fortitude: ')),
                              'TOUGHNESS': int(input('Toughness: ')),
                              'WILL': int(input('Will: ')),
                              'init': int(input('Initiative: '))}
                break
            except ValueError:
                print('Only integers are supported.')
                continue
        file.write(f'{name}\n\n')
        for key in self.stats.keys():
            file.write(f'{key}: {self.stats[key]}\n')
        file.close()

    def damage(self):
        if self.incapac == '*INCAPACITATED*':
            self.incapac = '*[DYING]*'
            return None
        if self.incapac == '*[DYING]*':
            self.incapac = '((DEAD))'
            return None
        while True:
            try:
                dmg = int(input('Damage dealt: '))
                break
            except ValueError:
                print('Only integers are supported.')
                continue
        while True:
            try:
                dado = int(input('Resistance check result: '))
                break
            except ValueError:
                print('Only integers are supported.')
                continue
        condit = (dmg - dado + self.dmgpe) // 5
        if condit > 4:
            condit = 4
        self.dmgc.append(condit)
        self.dmgpe = 0
        for _ in self.dmgc:
            self.dmgpe += 1
        if 2 in self.dmgc and 'Dazed' not in self.conds:
            self.conds.append('Dazed')
        if 3 in self.dmgc and '*Staggered' not in self.conds:
            self.conds.append('*Staggered')
        if 4 in self.dmgc or self.dmgc.count(3) > 1:
            self.incapac = '*INCAPACITATED*'
