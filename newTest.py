# from random import randint


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
                #self.field[cur.x][cur.y] = "+"
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


b = Board()
print(b)
s = Ship(4, Dot(1, 1), 0)
b.add_ship(s)
print(b)
