class RC5():
    # иницилизируем переменные
    def __init__(self, w, R, key):
        self.w = w                  # слово для шифрования
        self.R = R                  # раунды
        self.key = key
        self.b = len(key)           # длина подблока
        self.T = 2 * (R + 1)        # ключ шифрования
        self.w4 = w // 4            # кратность 4
        self.w8 = w // 8            # кратность 8
        self.mod = 2 ** self.w
        self.mask = self.mod - 1
        self.__keyAlign()           # выравнивание ключа
        self.__keyExtend()          # массив расширенных ключей
        self.__mix()                # перемешивание элементов М и S

    # сдвиг влево
    def __leftshift(self, value, k):
        k %= self.w
        return ((value << k) & self.mask) | ((value & self.mask) >> (self.w - k))

    # сдвиг вправо
    def __rightshift(self, value, k):
        k %= self.w
        return ((value & self.mask) >> k) | (value << (self.w - k) & self.mask)

    # необходимые константы
    def __const(self):
        if self.w == 16:
            return (0xB7E1, 0x9E37)  # Возвращает значения P и Q соответсвенно
        elif self.w == 32:
            return (0xB7E15163, 0x9E3779B9)
        elif self.w == 64:
            return (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15)

    # выравнивание ключа
    def __keyAlign(self):
        # если ключ пустой
        if self.b == 0:
            self.x = 1
        # если размер ключа не кратен w / 8
        elif self.b % self.w8:
            # дополняем ключ байтами
            self.key += b'\x00' * (self.w8 - self.b % self.w8)
            self.b = len(self.key)
            self.x = self.b // self.w8
        else:
            self.x = self.b // self.w8
        M = [0] * self.x  # массив с блоками w / 8
        # заполняем массив M
        for i in range(self.b - 1, - 1, - 1):
            M[i // self.w8] = (M[i // self.w8] << 8) + self.key[i]
        self.M = M

    # заполняем массив S, где S[0] = Pw, S[i+1] = S[i]+Qw
    def __keyExtend(self):
        P = self.__const()
        Q = self.__const()
        self.S = [(P + i * Q) % self.mod for i in range(self.T)]

    # перемешиваем элементы массивов M и S
    def __mix(self):
        i, j, A, B = 0, 0, 0, 0
        for n in range (3 * max(self.x, self.T)):
            A = self.S[i] = self.__leftshift((self.S[i] + A + B), 3)
            B = self.M[j] = self.__leftshift((self.M[j] + A + B), A + B)
            i = (i + 1) % self.T
            j = (i + 1) % self.x

