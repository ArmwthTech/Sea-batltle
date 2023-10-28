import random


class Dot:
    def __init__(self, x: int, y: int):
        self.x = x  # столбец
        self.y = y  # строка

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False


class Ship:
    def __init__(self, len_ship: int, start_dot_ship: int, ship_direction: int, count_life: int):
        self.len_ship = len_ship
        self.start_dot_ship = start_dot_ship
        self.ship_direction = ship_direction
        self.count_life = count_life

    @property
    def dots(self):
        pass


class Board:
    def __init__(self, status_list, list_ships, hid: bool, count_life_ships: int):
        self.status_list = status_list
        self.list_ships = list_ships
        self.hid = hid
        self.count_life_ships = count_life_ships
        # self.size = size
        # self.grid = [['О' for _ in range(size)] for _ in range(size)]
        # self.ships = []

    def add_ship(self):
        pass

    def print_board(self):
        print("   | 1 | 2 | 3 | 4 | 5 | 6|")
        for i in range(self.size):
            print(f"{i + 1} | {' | '.join(self.grid[i])} |")

    def contour(self):
        pass

    def out(self):
        pass

    def shot(self):
        pass


class Player:
    board_user = Board()
    board_enemy = Board()

    def ask(self):
        # метод, который «спрашивает» игрока, в какую клетку он делает выстрел
        pass

    def move(self):
        # метод, который делает ход в игре
        return True


class AI(Player):
    pass


class User(Player):
    pass


class Game:
    def random_board(self):
        # метод генерирует случайную доску

        pass

    def mode(self):
        pass

    def greet(self):
        # метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
        print('Добро пожаловать в игру "Морской Бой!".\n'
              'Чтобы сделать выстрел, вы должны ввести координату поля, сначала по строке(от 1 до 6 включительно),\n'
              'а потом по столбцу(от 1 до 6 включительно). Приятной игры!')

    def loop(self):
        # метод с самим игровым циклом
        pass

    def start(self):
        self.greet()
        self.loop()
        pass


def main():
    start_game = Game()
    start_game.start()


if __name__ == '__main__':
    main()
