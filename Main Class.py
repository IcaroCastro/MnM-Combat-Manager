from File_Class import File


class Master:
    def __init__(self):
        self.char_list = dict()
        self.init = list()
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
            self.display()
            act = input('What do you want to do? Damage (1), Change Initative Order (2), Grant Condition (3), '
                        'Heal (4), Define Condition (5), End Combat (6).  ')

    def chars(self):
        char = File()
        if char.name in self.char_list.keys():
            print('This character is already in battle.')
            print('=-'*30+'=\n'+'-='*30+'-')
        else:
            self.char_list[char.name] = char

    def init_list(self):
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
            correct = input('Is this correct? Yes(1) No(2).')
            if correct == '1':
                print('=-' * 30 + '=')
                break
            else:
                print('-' * 30)
                self.init.clear()
                continue

    def display(self):
        for chars in self.init:
            print(f'{chars} {self.char_list[chars].incapac} // {self.char_list[chars].conds} '
                  f'-{self.char_list[chars].dmgpe} // {self.char_list[chars].circ} ({self.char_list[chars].circ_comm})')

Master()
