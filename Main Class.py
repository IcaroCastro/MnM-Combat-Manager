from File_Class import File


class Master:
    def __init__(self):
        self.char_list = dict()
        pass

    def chars(self, name):
        if name in self.char_list.keys():
            print('This character is already in battle.')
            return None
        else:
            print('=-'*30+'=\n'+'-='*30+'-')
            self.char_list[name] = File()

Master()