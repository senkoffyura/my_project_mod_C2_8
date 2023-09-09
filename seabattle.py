import random


class Deck:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете мимо доски"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы стреляли в эту точку"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self,deck,ndeck,flag):
        self.deck = deck
        self.ndeck = ndeck
        self.flag = flag
        self.live = ndeck

    @property
    def decks(self):
        decks_list = []
        for i in range(self.ndeck):
            x = self.deck.x
            y = self.deck.y

            if self.flag == 0:
                x += i
            else:
                y += i

            decks_list.append(Deck(x,y))
        return decks_list

    def shotAtship(self,deck):
        return deck in self.decks

class GameBoard:
    def __init__(self,side = 6, hid = False):
        self.hid = hid
        self.side = side
        self.count = 0
        self.field = [["O"]*side for n in range(side)]
        self.set_of_ships = []
        self.busy = []
    def __str__(self):
        prt = "   |"

        for i in range(self.side):
            prt += f" {i+1} |"
        for i, dec in enumerate(self.field):
            prt += f"\n {i+1} | " + " | ".join(dec) + " | "

        if self.hid:
            prt = prt.replace("█", "O")

        return prt

    def out(self,hut):
        return not((0 <= hut.x < self.side) and (0 <= hut.y < self.side))

    def contor(self,ship, verb = False):
        near = [ (-1,-1), (0,-1), (1,-1),
                 (-1,0), (0,0), (1,0),
                 (-1,1), (0,1), (1,1)]

        for dec in ship.decks:
            for dx, dy in near:
                cur = Deck(dec.x+dx, dec.y+dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "T"
                    self.busy.append(cur)

    def add_ship(self, ship):
        for dec in ship.decks:
            if self.out(dec) or dec in self.busy:
                raise BoardWrongShipException()

        for dec in ship.decks:
            self.field[dec.x][dec.y] = "█"
            self.busy.append(dec)
        self.set_of_ships.append(ship)
        self.contor(ship)

    def shot(self,dec):
        if self.out(dec):
            raise BoardOutException()

        if dec in self.busy:
            raise BoardUsedException()

        self.busy.append(dec)

        for ship in self.set_of_ships:
            if dec in ship.decks:
                ship.live -= 1
                self.field[dec.x][dec.y] = "X"
                if ship.live == 0:
                    self.count += 1
                    self.contor(ship,True)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Корабль ранен")
                    return True
        self.field[dec.x][dec.y] = "T"
        print("Мимо")
        return False

    def begin(self):
        self.busy = []

    def sign_victory(self):
        return self.count == len(self.set_of_ships)

class Player:
    def __init__(self,myboard, enemyboard):
        self.myboard = myboard
        self.enemyboard = enemyboard
    def ask(self):
        raise NotImplementedError
    def move(self):
        while True:
            try:
                trg = self.ask()
                repead = self.enemyboard.shot(trg)
                return repead
            except BoardException as tex:
                print(tex)

class AI(Player):
    def ask(self):
        return Deck(random.randint(0,self.myboard.side), random.randint(0,self.myboard.side))

class User(Player):
    def ask(self):
        while True:
            x = input("Введите координату по вертикали: ")
            y = input("Введите координату по горизонтали: ")
            if not(x.isdigit()) and not(y.isdigit()):
                print(f"Введите числа от 1 до {self.myboard.side}")
                continue

            x, y = int(x)-1, int(y)-1
            return Deck(x, y)

class Game:
    def __init__(self, side = 6, num_dec = [3, 2, 2, 1, 1, 1, 1]):

        self.num_dec = num_dec
        self.side = side
        user = self.try_board()
        comp = self.try_board()
        comp.hid = True
        self.user = User(user, comp)
        self.comp = AI(comp, user)


    def boart_random(self):

        board = GameBoard()

        i = 0
        for n in self.num_dec:
            while True:
                i += 1
                if i > 2000:
                    return None
                ship = Ship(Deck(random.randint(0,board.side),random.randint(0,board.side)),n ,random.randint(0, 1))

                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    def try_board(self):
        board = None
        while board is None:
            board = self.boart_random()
        return board

    def loop(self):
        n = 0
        while True:
            print("-"*20)
            print("Доска пользователя")
            print(self.user.myboard)
            print("-" * 20)
            print("Доска компьютера")
            print(self.comp.myboard)
            print("-" * 20)

            if n % 2 == 0:
                print("Ходит пользователь")
                repeat = self.user.move()
            else:
                print("Ходит компьютер")
                repeat = self.comp.move()

            if repeat:
                n -= 1

            if self.comp.myboard.sign_victory():
                print("-" * 20)
                print("Пользователь выйграл")
                break
            if self.user.myboard.sign_victory():
                print("-" * 20)
                print("Комьютер выйграл")
                break
            n += 1
    def start(self):
        self.loop()


g = Game()
g.start()







