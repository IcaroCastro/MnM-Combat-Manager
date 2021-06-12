class File:
    def __init__(self):
        self.penal_dmg = 0
        self.circ = 0
        self.incapac = False
        self.conds = list()
        while True:
            try:
                self.stats = {'Stts': {'STR': int(input('Strength: ')),
                                       'AGI': int(input('Agility: ')),
                                       'FGT': int(input('Fighting: ')),
                                       'AWA': int(input('Awareness: ')),
                                       'STA': int(input('Stamina: ')),
                                       'DEX': int(input('Dexterity: ')),
                                       'INT': int(input('Intellect: ')),
                                       'PRE': int(input('Presence: '))},
                              'Defs': {'Dodge': int(input('Dodge: ')),
                                       'Parry': int(input('Parry: ')),
                                       'Fortitude': int(input('Fortitude: ')),
                                       'Toughness': int(input('Toughness: ')),
                                       'Will': int(input('Will: '))}}
            except ValueError:
                print('Only integers are supported.')
                continue
        self.dmgc = list()

    def damage(self):
        for _ in self.dmgc:
            self.penal_dmg += 1
        if 2 in self.dmgc and 'Dazed' not in self.conds:
            self.conds.append('Dazed')
        if 3 in self.dmgc and 'Staggered' not in self.conds:
            self.conds.append('Staggered')
        