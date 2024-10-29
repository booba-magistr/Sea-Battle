from random import randint, seed

seed(1)


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._cells = [1] * self._length  # заменить на 1 перед отправкой
        self._is_move = True if 2 not in self._cells else False

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_length(self):
        return self._length

    def get_tp(self):
        return self._tp

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    def is_collide(self, ship):
        i, j = ship.get_start_coords()
        ship_cords = [(i + x, j) for x in range(ship.get_length())] \
            if ship.get_tp() == 1 else [(i, j + x) for x in range(ship.get_length())]
        if self._tp == 1:
            horizontal_cords = [((self._x + x - 1, self._y), (self._x + x - 1, self._y - 1),
                                 (self._x + x - 1, self._y + 1), (self._x + x, self._y + 1),
                                 (self._x + x + 1, self._y + 1), (self._x + x + 1, self._y),
                                 (self._x + x + 1, self._y - 1), (self._x + x, self._y - 1)) for x in
                                range(self.get_length())]
            for z in horizontal_cords:
                for w in ship_cords:
                    if w in z:
                        return True
        else:
            vertical_cords = [((self._x - 1, self._y + x), (self._x - 1, self._y + x - 1),
                               (self._x - 1, self._y + x + 1), (self._x, self._y + x + 1),
                               (self._x + 1, self._y + x + 1), (self._x + 1, self._y + x),
                               (self._x + 1, self._y + x - 1), (self._x, self._y + x - 1)) for x in
                              range(self.get_length())]
            for z in vertical_cords:
                for w in ship_cords:
                    if w in z:
                        return True
        return False

    def is_out_pole(self, size=10):
        if self._tp == 1:
            if self._x + self._length > size - 1:
                return True
        else:
            if self._y + self._length > size - 1:
                return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []
        self.__ship_coords = []
        self.__game_pole = [[0 for x in range(self._size)] for y in range(self._size)]

    def init(self):
        self._ships = [Ship(4, randint(1, 2)),
                       Ship(3, randint(1, 2)),
                       Ship(3, randint(1, 2)),
                       Ship(2, randint(1, 2)),
                       Ship(2, randint(1, 2)),
                       Ship(2, randint(1, 2)),
                       Ship(1, randint(1, 2)),
                       Ship(1, randint(1, 2)),
                       Ship(1, randint(1, 2)),
                       Ship(1, randint(1, 2))]

        counter = 0
        while counter != 10:
            x, y = randint(0, 9), randint(0, 9)
            res = x, y
            if res in self.__ship_coords:
                continue
            self._ships[counter].set_start_coords(x, y)
            if self._ships[counter].is_out_pole(self._size):
                continue
            if any(map(self._ships[counter].is_collide, self._ships[:counter])):
                continue
            self.__ship_coords.append(res)
            counter += 1

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for k, v in enumerate(self._ships):
            v.move(+1)
            if any((v.is_out_pole(), any(map(v.is_collide, self._ships[:k] + self._ships[k + 1:])))):
                v.move(-2)
                if any((v.is_out_pole(), any(map(v.is_collide, self._ships[:k] + self._ships[k + 1:])))):
                    v.move(+1)

    def show(self):
        for x in self.get_ships():
            i, j = x.get_start_coords()
            self.__game_pole[j][i] = 1
            if x.get_tp() == 1:
                self.__game_pole[j][i: x.get_length() + i] = x[:]
            else:
                for n in range(x.get_length()):
                    self.__game_pole[j + n][i] = 1
        for z in self.__game_pole:
            print(*z)

    def get_pole(self):
        return tuple(tuple(x) for x in self.__game_pole)