from File_Class import File


class Master:
    def __init__(self):
        self.char_list = dict()
        self.init = list()
        self.condict = dict()
        self.cond_dic()
        done = False
        while not done:
            self.chars()
            while True:
                d = input('Do you wish to add more characters? Yes(1) No(2). ')
                if d == '1':
                    print('-' * 30)
                    break
                elif d == '2':
                    print('-' * 30)
                    done = True
                    break
                else:
                    print('Invalid answer.')
                    print('-'*30)
                    continue
        self.init_list()
        print('=-' * 30 + '=\n' +
              '         Starting Combat       \n' +
              '=-' * 30 + '=\n')
        while True:
            for pers in self.char_list.values():
                pers.update()
            print('=='*30)
            self.display()
            print('')
            act = input('What do you want to do? Damage (1), Heal (2), Grant Condition (3), Remove Condition (4)\n'
                        'Change Initative Order (5), Define Condition (6), Add Comentary (7), End Combat (8).  ')
            if act == '1':
                self.damage(input('Character being damaged: '))
            elif act == '2':
                self.healc(input('Character being healed: '))
            elif act == '3':
                self.grantcond(input('Character Name: '), input('Condition: '))
            elif act == '4':
                self.removcond(input('Character Name: '), input('Condition: '))
            elif act == '5':
                self.initswp(input('Character Name: '), input('Position in the initiative list: '))
            elif act == '6':
                definit = self.defcondit(input('Which condition you want me to define?  '))
                if definit == 'not0':
                    print('Unknown condition')
                else:
                    print(definit)
            elif act == '7':
                self.comm(input('Character Name: '))
            elif act == '8':
                if input('Are you shure? Yes(1) No(2) ') == '1':
                    exit()
                else:
                    continue
            else:
                print('Not a valid action.')
                continue

    def chars(self):  # Add characters to combat
        char = File(input('Character name: '))
        if char.name in self.char_list.keys():
            print('This character is already in battle.')
            print('=-'*30+'=\n'+'-='*30+'-')
        else:
            self.char_list[char.name] = char

    def init_list(self):  # Defining the list of initiative
        while True:
            print('Insert the characters in initiative order:')
            for _ in range(0, len(self.char_list.keys())):
                while True:
                    char = input('Character name: ')
                    if char not in self.char_list.keys():
                        print('Character not in character list.')
                        print('-' * 30)
                        continue
                    else:
                        self.init.append(char)
                        break
            for elem in self.init:
                print(elem)
            correct = input('Is this correct? Yes(1) No(2). ')
            if correct == '1':
                print('=-' * 30 + '=')
                break
            else:
                print('-' * 30)
                self.init.clear()
                continue

    def display(self):  # Displaying the characters in initative order with extra info
        for chars in self.init:
            print(f'{chars} {self.char_list[chars].incapac} // {self.char_list[chars].conds} '
                  f'-{self.char_list[chars].dmgpe} (tgh/fort/will) // {self.char_list[chars].circ} '
                  f'({self.char_list[chars].comm}) ')

    def cond_dic(self):  # Get all condition definitions from ConditDictionary file
        file = open('ConditDictionary', 'r')
        data = file.read()
        file.close()
        treat1 = data.split('\n')
        treat2 = list()
        for elem in treat1:
            treat2.append(elem.split('---'))
        for item in treat2:
            self.condict[item[0]] = item[1]

    def defcondit(self, x):  # Get specific condition definition
        if x in self.condict.keys():
            return self.condict[x]
        elif '*' + x in self.condict.keys():
            return self.condict['*' + x]
        else:
            return 'not0'

    def initswp(self, name, pos):  # Modify iniative position of a character
        try:
            self.init.remove(name)
            self.init.insert(int(pos) - 1, name)
        except ValueError:
            if type(pos) != int():
                print('Invalid position.')
            elif name not in self.init:
                print('Character not in initiative list.')
            else:
                print('Something went wrong')

    def damage(self, name):  # Deal damage to a character
        try:
            self.char_list[name].damage()
        except KeyError:
            print('Character not in Character List.')

    def grantcond(self, name, cond):  # Grant a character a condition
        if cond not in self.condict.keys() and '*' + cond not in self.condict.keys():
            print('Unknown condition.')
        else:
            if cond not in self.condict.keys():
                cond = '*' + cond
            try:
                if cond not in self.char_list[name].conds:
                    self.char_list[name].conds.append(cond)
                else:
                    print(f'{name} already has the condition {cond}')
            except KeyError:
                print('Character not in character list.')

    def removcond(self, name, cond):  # Remove a condition from a character
        try:
            self.char_list[name].conds.remove(cond)
        except KeyError:
            print('Character not in character list')
        except ValueError:
            try:
                self.char_list[name].conds.remove('*' + cond)
            except ValueError:
                print(f'{name} does not have the condition {cond}')

    def healc(self, name):  # Heal a character
        try:
            self.char_list[name].heal(input('Degrees of success: '))
        except KeyError:
            print('Character is not in the character list.')

    def comm(self, name):  # Give a character a commentray, displayed in the interface
        try:
            self.char_list[name].comm = input('Insert commentary: ')
        except KeyError:
            print('Character is not in the character list.')

Master()
