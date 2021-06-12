class File:
    def __init__(self):
        self.circ = 0
        self.incapac = False
        self.conds = list()
        self.dmgc = list()
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
                              'Defs': {'DODGE': int(input('Dodge: ')),
                                       'PARRY': int(input('Parry: ')),
                                       'FORTITUDE': int(input('Fortitude: ')),
                                       'TOUGHNESS': int(input('Toughness: ')),
                                       'WILL': int(input('Will: '))}}
                break
            except ValueError:
                print('Only integers are supported.')
                continue

    def damage(self):
        penal_dmg = 0
        for _ in self.dmgc:
            penal_dmg += 1
        if 2 in self.dmgc and 'Dazed' not in self.conds:
            self.conds.append('Dazed')
        if 3 in self.dmgc and 'Staggered' not in self.conds:
            self.conds.append('Staggered')
        while True:
            try:
                dmg = int(input('Damage dealt: '))
                break
            except ValueError:
                print('Only integers are supported.')
                continue
        while True:
            res = input('Resistance type [Toughness, Fortitude, Will]: ').upper()
            if res != 'TOUGHNESS' and res != 'FORTITUDE' and res != 'WILL':
                print('Only Toughness, Fortitude and Will are valid resistance types.')
                continue
            else:
                try:
                    dado = int(input('Resistance check result: '))
                    break
                except ValueError:
                    print('Only integers are supported.')
                    continue
        condit = (dmg - dado + penal_dmg) // 5
        self.dmgc.append(condit)
        if 4 in self.dmgc or self.dmgc.count(3) > 1:
            self.incapac = True
