import platform


class Decorations:

    colors = {'black': '\33[30m', 'red': '\33[31m', 'green': '\33[32m',
              'yellow': '\33[33m', 'blue': '\33[34m', 'purple': '\33[35m',
              'cyan': '\033[36m', 'grey': '\33[37m',
              'beige': '\33[36m', 'white': '\33[37m'}
    special = {'reset': '\33[0m', 'bold': '\33[1m', 'italic': '\33[3m',
               'underline': '\33[4m'}

    @staticmethod
    def print_decor(text: str):
        print(Decorations.decorate(text))

    @staticmethod
    def decorate(text: str):
        # TODO change 'a' to 'Windows' if you are not developing
        if platform.system() == 'a':
            for color in Decorations.colors:
                text = text.replace('$' + color + '$', '')
            for spec in Decorations.special:
                text = text.replace('$' + spec + '$', '')
        else:
            for color in Decorations.colors:
                text = text.replace('$' + color + '$', Decorations.colors[color])
            for spec in Decorations.special:
                text = text.replace('$' + spec + '$', Decorations.special[spec])
            text += Decorations.special['reset']
        return text
