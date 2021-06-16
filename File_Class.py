class File:
    def __init__(self, nome):
        self.circ = 0
        self.comm = str()
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

        self.name = nome
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

    def heal(self, degs):
        try:
            degrs = int(degs)
        except ValueError:
            print('Only positive integer degrees of success are valid.')
            return None
        if degrs <= 0:
            print('Only positive integer degrees of success are valid.')
            return None
        if self.incapac == '*DYING*' and degrs > 0:
            self.incapac = '*INCAPACITATED*'
            degrs -= 1
        if self.incapac == '*INCAPACITATED*' and degrs > 0:
            self.incapac = ''
            degrs -= 1
        if '*Staggered' in self.conds and degrs > 0:
            self.conds.remove('*Staggered')
            degrs -= 1
        if 'Dazed' in self.conds and degrs > 0:
            self.conds.remove('Dazed')
            degrs -= 1
        self.dmgpe -= degrs
        if self.dmgpe < 0:
            self.dmgpe = 0

    def update(self):
        if 'Impaired' in self.conds and self.circ > -2:
            self.circ = -2
        else:
            self.circ = 0
        if 'Disabled' in self.conds and self.circ > -5:
            self.circ = -5
        else:
            self.circ = 0
