import random


def get_neighbours_for_generator(i_pos, j_pos, maze, types):
    """
        Получение соседей для генератора лабиринта.

        Параметры:
            i_pos (int): Текущая позиция по вертикали.
            j_pos (int): Текущая позиция по горизонтали.
            maze (list): Двумерный список, представляющий лабиринт.
            types (list): Двумерный список, представляющий типы клеток (CELL, WALL).

        Возвращаемые значения:
            list: Список соседей в формате (i, j, direction).
    """
    nei = []
    if i_pos > 1 and maze[i_pos - 2][j_pos] == '1' \
            and types[i_pos - 2][j_pos] == 'CELL':  # сверху
        nei.append((i_pos - 2, j_pos, 'up'))
    if i_pos < (len(maze) - 2) and maze[i_pos + 2][j_pos] == '1' \
            and types[i_pos + 2][j_pos] == 'CELL':  # снизу
        nei.append((i_pos + 2, j_pos, 'down'))
    if j_pos > 1 and maze[i_pos][j_pos - 2] == '1' \
            and types[i_pos][j_pos - 2] == 'CELL':  # слева
        nei.append((i_pos, j_pos - 2, 'left'))
    if j_pos < (len(maze[0]) - 2) and maze[i_pos][j_pos + 2] == '1' \
            and types[i_pos][j_pos + 2] == 'CELL':  # справа
        nei.append((i_pos, j_pos + 2, 'right'))
    return nei


def get_neighbours_for_solution(i_pos, j_pos, maze, used):
    """
        Получение соседей для поиска пути в лабиринте.

        Параметры:
            i_pos (int): Текущая позиция по вертикали.
            j_pos (int): Текущая позиция по горизонтали.
            maze (list): Двумерный список, представляющий лабиринт.
            used (list): Двумерный список, представляющий использованные клетки.

        Возвращаемые значения:
            list: Список соседей в формате (i, j, direction).
    """
    nei = []
    # Проверяем, есть ли свободное пространство около текущей ячейки и не посещали ли мы ее уже
    if i_pos > 1 and maze[i_pos - 1][j_pos] == '.' \
            and used[i_pos - 2][j_pos] == 0:  # сверху
        nei.append((i_pos - 2, j_pos, 'up'))
    if i_pos < (len(maze) - 2) and maze[i_pos + 1][j_pos] == '.' \
            and used[i_pos + 2][j_pos] == 0:  # снизу
        nei.append((i_pos + 2, j_pos, 'down'))
    if j_pos > 1 and maze[i_pos][j_pos - 1] == '.' \
            and used[i_pos][j_pos - 2] == 0:  # слева
        nei.append((i_pos, j_pos - 2, 'left'))
    if j_pos < (len(maze[0]) - 2) and maze[i_pos][j_pos + 1] == '.' \
            and used[i_pos][j_pos + 2] == 0:  # справа
        nei.append((i_pos, j_pos + 2, 'right'))
    return nei


def map_generator(width, height, filename_inp=None):
    """
        Генерирует лабиринт и его решение.

        Параметры:
            width (int): Ширина лабиринта.
            height (int): Высота лабиринта.
            filename_inp (str): Имя файла для загрузки начального лабиринта.

        Возвращает:
            tuple: Кортеж из двух элементов - чистое решение лабиринта trace и история генерации решения history(со
            всеми шагами).

        Пример использования:
            map_generator(10, 10, 'my_maze.txt')
    """
    maze = []
    if filename_inp is not None:
        maze = open_maze_txt(filename_inp)
    else:
        types = []
        not_visited = set()
        # Создание массивов для представления лабиринта и его типов
        for i in range(height + 1):
            line = []
            t = []
            for j in range(width + 1):
                line.append('1')  # Инициализация всего лабиринта стенами 1
                if i == 0 or i == height or j == 0 or j == width:
                    t.append('WALL')  # Граничные стены
                elif i % 2 == 0 or j % 2 == 0:
                    t.append('WALL')  # Внутренние стены
                else:
                    t.append('CELL')  # Проход
                    not_visited.add((i, j))  # Добавление прохода в множество непосещенных клеток
            types.append(t)
            maze.append(line)

        maze[1][1] = 'S'  # старт
        now = (1, 1)
        not_visited.remove(now)
        stack = []
        # Генерация лабиринта
        while len(not_visited) > 0:
            nei = get_neighbours_for_generator(now[0], now[1], maze, types)
            if len(nei) > 0:
                stack.append(now)
                ind = random.randint(0, len(nei) - 1)
                next_cell = nei[ind]
                # Открываем проход в стене, соединяющей текущую и следующую клетки
                if next_cell[2] == 'up':
                    maze[now[0] - 1][next_cell[1]] = '.'
                if next_cell[2] == 'down':
                    maze[now[0] + 1][next_cell[1]] = '.'
                if next_cell[2] == 'left':
                    maze[next_cell[0]][now[1] - 1] = '.'
                if next_cell[2] == 'right':
                    maze[next_cell[0]][now[1] + 1] = '.'
                now = (next_cell[0], next_cell[1])
                maze[now[0]][now[1]] = '.'
                not_visited.remove(now)
            elif len(stack) > 0:
                now = stack.pop()
    # Инициализация массива для представления пути и вызов генерации решения
    trace = [[0 for _ in range(len(maze[0]))] for __ in range(len(maze))]
    ans = solution_generator(maze, trace)
    # Установка финишной клетки и сохранение лабиринта в файл
    maze[height - 1][width - 1] = 'F'
    with open(f'{filename_inp}', 'w') as f:
        for i in range(len(maze)):
            s = ''
            for j in range(len(maze[0])):
                s += maze[i][j]
            f.write(s + '\n')
        f.close()
    return ans


def conv(letters):
    arr = [_ for _ in letters]
    return arr


def open_maze_txt(file):
    """
        Открывает файл и считывает лабиринт из текстового файла.

        Параметры:
            file (str): Имя файла с лабиринтом.

        Возвращает:
            list: Двумерный массив представляющий лабиринт.

        Пример использования:
            open_maze_txt('my_maze.txt')
    """
    data = []
    with open(file, 'rt') as f:
        for line in f:
            line_mod = list(conv(line.strip()))
            data.append(line_mod)  # срезать перенос строки!
    return data


def solution_generator(maze, trace):
    """
        Генерирует путь от начальной точки до конечной в лабиринте.

        Параметры:
            maze (list): Двумерный массив, представляющий лабиринт.
            trace (list): Двумерный массив для отслеживания пути.

        Возвращает:
            tuple: Кортеж из двух элементов:
                - trace (list): Двумерный массив, представляющий путь в лабиринте.
                - history (list): Список шагов в пути с информацией о каждом шаге.

        Пример использования:
            maze = [...]
            trace, history = solution_generator(maze, trace)
    """
    # Инициализация начальных значений
    trace[1][1] = 1
    used = [[0 for _ in range(len(maze[0]))] for __ in range(len(maze))]
    used[1][1] = 1  # Помечаем начальную точку как использованную
    now = (1, 1)  # Текущее положение в лабиринте
    end = (len(maze) - 2, len(maze[0]) - 2)
    stack = []  # Стек для хранения предыдущих точек
    history = []

    while now != end:
        # Получаем соседей текущей ячейки
        nei = get_neighbours_for_solution(now[0], now[1], maze, used)
        if len(nei) > 0:
            stack.append(now)  # Добавляем текущую ячейку в стек
            ind = random.randint(0, len(nei) - 1)  # Случайным образом выбираем одного из соседей
            next_cell = nei[ind]
            # Помечаем следующую ячейку в лабиринте и обновляем трассировку пути
            if next_cell[2] == 'up':
                trace[now[0] - 1][next_cell[1]] = 1
                trace[next_cell[0]][next_cell[1]] = 1
                history.append([1, [(now[0] - 1, next_cell[1]),
                                    (next_cell[0], next_cell[1])]])
                used[now[0] - 1][next_cell[1]] = 1
                used[next_cell[0]][next_cell[1]] = 1
            elif next_cell[2] == 'down':
                trace[now[0] + 1][next_cell[1]] = 1
                trace[next_cell[0]][next_cell[1]] = 1
                history.append([1, [(now[0] + 1, next_cell[1]),
                                    (next_cell[0], next_cell[1])]])
                used[now[0] + 1][next_cell[1]] = 1
                used[next_cell[0]][next_cell[1]] = 1
            elif next_cell[2] == 'left':
                trace[next_cell[0]][now[1] - 1] = 1
                trace[next_cell[0]][next_cell[1]] = 1
                history.append([1, [(next_cell[0], now[1] - 1),
                                    (next_cell[0], next_cell[1])]])
                used[next_cell[0]][now[1] - 1] = 1
                used[next_cell[0]][next_cell[1]] = 1
            elif next_cell[2] == 'right':
                trace[next_cell[0]][now[1] + 1] = 1
                trace[next_cell[0]][next_cell[1]] = 1
                history.append([1, [(next_cell[0], now[1] + 1),
                                    (next_cell[0], next_cell[1])]])
                used[next_cell[0]][now[1] + 1] = 1
                used[next_cell[0]][next_cell[1]] = 1
            now = (next_cell[0], next_cell[1])  # Обновляем текущую ячей
            """
                Когда алгоритм сталкивается с ситуацией, что текущая ячейка (now) 
                больше не имеет соседей, которые еще не посещены, он возвращается 
                к предыдущей ячейке (prev_cell) из стека
            """
        elif len(stack) > 0:
            print(len(stack))
            trace[now[0]][now[1]] = 0
            prev_cell = stack.pop()
            y = now[0]
            x = now[1]
            if now[0] + 2 == prev_cell[0]:  # пришли снизу
                trace[now[0] + 1][now[1]] = 0
                # ячейка помечается как непосещенная в матрице "trace",
                # что отражает, что возврат произошел.
                y += 1
            elif now[0] - 2 == prev_cell[0]:  # пришли сверху
                trace[now[0] - 1][now[1]] = 0
                y -= 1
            elif now[1] + 2 == prev_cell[1]:  # пришли справа
                trace[now[0]][now[1] + 1] = 0
                x += 1
            elif now[1] - 2 == prev_cell[1]:  # пришли слева
                trace[now[0]][now[1] - 1] = 0
                x -= 1
            history.append([0, [(y, x), (now[0], now[1])]])
            now = prev_cell
    return trace, history
