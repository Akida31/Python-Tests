import random
import pickle

class Item:
    def __init__(self, weigth, worth):
        self.weight = weigth
        self.worth = worth

class Potion(Item):
    def __init__(self, weight, worth):
        Item.__init__(self, weight, worth)

class HealthPotion(Potion):
    def __init__(self, weight, worth, regenerated_health):
        Potion.__init__(self, weight, worth)
        self.regenerated_health = regenerated_health

class Character:
    def __init__(self, hp, ad, name,worth=None):
        self.hp = hp
        self.ad = ad
        self.name = name
        self.worth = worth

    def get_hit(self, ad):
        self.hp = self.hp - ad
        if self.hp <= 0:
            self.die()

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + " died")

class Goblin(Character):
    def __init__(self):
        Character.__init__(self, 100, 10, "Goblin",1)

class Ork(Character):
    def __init__(self):
        Character.__init__(self, 300, 30, "Ork",3)

class Player(Character):
    def __init__(self, name, hp, ad):
        Character.__init__(self, hp, ad, name)
        self.max_hp = hp

    def die(self):
        exit("Wasted. Try again.")

    def rest(self):
        self.hp = self.max_hp

class fighting:
    def __init__(self,team1,team2,m):
        self.team1 = team1
        self.team2 = team2
        self.run(m)

    def run(self,m):
        enemies = self.team2
        team = self.team2
        while len(enemies) > 0:
            enemies[0].get_hit(p.ad)
            if enemies[0].is_dead():
                enemies.remove(enemies[0])
            for i in enemies:
                p.get_hit(i.ad)
            print("You are wounded and have " + str(p.hp) + " hp left")
        return 'print'
    def attack(self,p):
        print(p.weapons)
        weapon = input('Which weapon do you want to use?\n')

class Field:
    def __init__(self, enemies):
        self.enemies = enemies
        self.loot = []

    def print_state(self):
        print("You look around and see ")
        if len(self.enemies) == 0:
            print('nothing')
        for i in self.enemies:
            print(i.name)

    @staticmethod
    def gen_random():
        rand = random.randint(0,2)
        if rand == 0:
            return Field([])
        if rand == 1:
            return Field([Ork()])
        if rand == 2:
            return Field([Goblin(), Goblin(), Ork()])

class Map:
    def __init__(self, width, height):
        self.state = []
        self.x = 0
        self.y = 0
        for i in range(width):
            fields = []
            for j in range(height):
                fields.append(Field.gen_random())
            self.state.append(fields)

    def print_state(self):
        self.state[self.x][self.y].print_state()

    def get_enemies(self):
        return self.state[self.x][self.y].enemies

    def forward(self):
        if self.x == len(self.state) - 1:
            print("You see huge mountains, which you can't pass")
        else:
            self.x = self.x + 1

    def backwards(self):
        if self.x == 0:
            print("You see cliffs, but you can't jump safely")
        else:
            self.x = self.x - 1

    def right(self):
        if self.y == len(self.state[self.x]) - 1:
            print("You see huge mountains, which you can't pass")
        else:
            self.y = self.y + 1

    def left(self):
        if self.y == 0:
            print("You see cliffs, but you can't jump safely")
        else:
            self.y = self.y - 1

def forward(p, m):
    m.forward()
    return 'print'

def right(p, m):
    m.right()
    return 'print'

def left(p, m):
    m.left()
    return 'print'

def backwards(p, m):
    m.backwards()
    return 'print'

def save(p,m):
    variables = [p,m]
    with open('vars.pkl','wb') as f:
        pickle.dump(variables,f)
    print('saved')

def load(m='m',p='p'):
    with open('vars.pkl','rb') as f:
        variables  = pickle.load(f)
    print('loaded')
    variables.append('noprint')
    return variables

def quit_game(p, m):
    print("You commit suicide and leave this world.")
    exit(0)

def print_help(p, m):
    print(Commands.keys())

def pickup(p, m):
    pass

def fight(p,m):
    a = fighting(p,m.get_enemies(),m)
    return 'print'


def rest(p, m):
    p.rest()
    return 'noprint'

Commands = {
    'help': print_help,
    'exit': quit_game,
    'quit': quit_game,
    'pickup': pickup,
    'forward': forward,
    'right': right,
    'left': left,
    'backwards': backwards,
    'fight': fight,
    'save': save,
    'load': load,
    'rest': rest
}

if __name__ == '__main__':
    name = input("Enter your name\n")
    p = Player(name, 200, 100)
    map = Map(5,5)
    laden = input('Do you want to load a game?')
    if 'y' in laden:
        p,map = load()
    print("(type help to list the commands available)\n")
    while True:
        command = input(">").lower().split(" ")
        back = ' '
        if command[0] in Commands:
            back = Commands[command[0]](p, map)
        else:
            print("You run around in circles and don't know what to do.")
        if back != None:
            if not 'noprint' in back:
                map.print_state()
                print('Your hp: {} / {} '.format(p.hp,p.max_hp))