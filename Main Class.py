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
                    break
                elif d == '2':
                    done = True
                    break
                else:
                    print('Invalid answer.')
                    print('-'*30)
                    continue
        pass

    def chars(self):
        char = File()
        if char.name in self.char_list.keys():
            print('This character is already in battle.')
            print('=-'*30+'=\n'+'-='*30+'-')
        else:
            self.char_list[char.name] = char

Master()