from random import randint


# Прописываем родительский класс для отлавливания исключений
class BoardException(Exception):
    pass


class BoardOutException(BoardException):  # Класс для получения исключения выхода за доску
    def __str__(self):
        return "Вы стреляете в доску!!!"


class BoardUsedException(BoardException):  # Класс для получения исключения попадания в одну и ту же клетку
    def __str__(self):
        return "Вы уже стреляли в эту клетку!!!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x: int, y: int):
        self.x = x  # столбец
        self.y = y  # строка

    def __eq__(self, other):
        # метод сравнения точек
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):  # форматированный вывод
        return f'Dot({self.x},{self.y})'


class Ship:
    def __init__(self, len_ship: int, start_dot_ship, ship_direction: int):
        self.len_ship = len_ship
        self.start_dot_ship = start_dot_ship
        self.ship_direction = ship_direction
        self.count_life = len_ship

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len_ship):
            current_x = self.start_dot_ship.x
            current_y = self.start_dot_ship.y

            if self.ship_direction == 0:
                current_x += i
            elif self.ship_direction == 1:
                current_y += i

            ship_dots.append(Dot(current_x, current_y))
        return ship_dots

    def shooting(self, shot):  # метод выстрела
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0  # количество_пораженных_кораблей

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []  # хранит занятые точки
        self.ships = []  # хранит корабли которые на доске

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out_board(self, dot):
        return not (0 <= dot.x < self.size) and (0 <= dot.y < self.size)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                # self.field[cur.x][cur.y] = "+"
                if not (self.out_board(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out_board(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out_board(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.count_life -= 1
                self.field[d.x][d.y] = 'X'
                if ship.count_life == 0:
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:

    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        # метод, который «спрашивает» игрока, в какую клетку он делает выстрел
        raise NotImplementedError()

    def move(self):
        # метод, который делает ход в игре
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1}{d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход:").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for len_1 in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(len_1, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        # метод генерирует случайную доску
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    @staticmethod
    def greet():
        # метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        # метод с самим игровым циклом
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
