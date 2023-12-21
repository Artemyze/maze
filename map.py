import options as const


class Map:
    """
        Класс для представления карты лабиринта.

        Параметры:
                file (str): Имя файла с текстовым представлением лабиринта.

        Атрибуты:
                data (list): Двумерный список, представляющий карту лабиринта.

        Методы:
                conv(letters): Вспомогательный метод для преобразования символов в цвета.

        Пример использования:
                my_map = Map('my_maze.txt')
    """
    def __init__(self, file):
        self.data = []

        def conv(letters):
            """
                Вспомогательный метод для преобразования символов в цвета.

                Параметры:
                        letters (str): Строка символов, представляющих строку лабиринта.

                Возвращаемые значения:
                        list: Список цветов, представляющих строку лабиринта.
            """
            arr = []
            for letter in letters:

                r = 0
                if letter == 'S':
                    r = const.COLOR_S
                elif letter == '1':
                    r = const.COLOR_WALL
                elif letter == '.':
                    r = const.COLOR_WAY
                elif letter == 'F':
                    r = const.COLOR_FINISH

                arr.append(r)
            return arr

        with open(file, 'rt') as f:

            for line in f:
                line_mod = list(conv(line.strip()))
                self.data.append(line_mod)
