import options as const


class Map:
    def __init__(self, file):  # подгружать карту будем из текстового файла

        self.data = []

        def conv(letters):
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
                self.data.append(line_mod)  # срезать перенос строки!
