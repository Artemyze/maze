import argparse

from PIL.ImageDraw import Draw

import options as const
from map import Map
from maze import map_generator
from os import path
from PIL import Image

"""
Программа визуализации лабиринта

Этот скрипт определяет класс Program, который генерирует и визуализирует лабиринты на основе указанных параметров.
Код генерации лабиринта - реализация Алгоритма Прима.  Он также относится к классу алгоритмов создания лабиринтов и 
использует случайные элементы для генерации структуры лабиринта. Принцип работы алгоритма заключается в том,
что начиная с одной случайной точки, он поочередно добавляет проходы в лабиринте, соединяя текущую ячейку с 
соседней ячейкой, которая уже принадлежит лабиринту. 
Код поиска пути реализует алгоритм генерации лабиринта на основе поиска в глубину (Depth-First Search, DFS). Этот 
алгоритм отлично подходит для создания лабиринтов, так как он создает пути, случайным образом выбирая направления и 
соединяя ячейки лабиринта.
Он использует модуль argparse для анализа аргументов командной строки с целью настройки генерации лабиринта.

Использование:
    python script_name.py -image_output output_image.png -text_output output_text.txt
                         -text_input input_text.txt -width 800 -height 600 -difficult medium

Аргументы командной строки:
    -image_output, --img_o   : Выходной файл изображения для сгенерированного лабиринта (по умолчанию: const.IMAGE_OUTPUT).
    -text_output, --txt_o    : Выходной текстовый файл для сгенерированного лабиринта в формате .txt (по умолчанию: const.TEXT_OUTPUT).
    -text_input, --txt_i     : Входной текстовый файл для генерации лабиринта в формате .txt (по умолчанию: const.TEXT_OUTPUT).
    -width, --w              : Ширина изображения визуализации лабиринта (по умолчанию: const.WIDTH).
    -height, --h             : Высота изображения визуализации лабиринта (по умолчанию: const.HEIGHT).
    -difficult, --dif        : Параметр, определяющий сложность лабиринта (easy, medium, hard; по умолчанию определяются в словаре const.DIFFICULT_MAZE_BASE).

"""


class Program:
    def __init__(self, width, height, difficult_maze, img_out_fn, txt_out_fn, txt_in_fn):
        """
                Инициализация объекта Program.

                Параметры:
                    width (int): Ширина изображения лабиринта.
                    height (int): Высота изображения лабиринта.
                    difficult_maze (str): Уровень сложности лабиринта ('easy', 'medium', 'hard').
                    img_out_fn (str): Имя файла для сохранения изображения лабиринта.
                    txt_out_fn (str): Имя файла для сохранения текстового представления лабиринта.
                    txt_in_fn (str): Имя входного файла для генерации лабиринта.
        """
        self.dict_difficult_maze = {
            # в этом словаре определяется количество путей в лабиринте для каждого
            # уровня сложности
            'easy': (const.AMOUNT_CELLS_IN_H_EASY, const.AMOUNT_CELLS_IN_W_EASY),
            'medium': (const.AMOUNT_CELLS_IN_H_MEDIUM, const.AMOUNT_CELLS_IN_W_MEDIUM),
            'hard': (const.AMOUNT_CELLS_IN_H_HARD, const.AMOUNT_CELLS_IN_W_HARD)
        }
        self.width = width
        self.height = height
        self.difficult_maze = difficult_maze
        self.img_out_fn = img_out_fn
        self.txt_out_fn = txt_out_fn
        self.txt_in_fn = txt_in_fn
        self.cells_sizes = self.dict_difficult_maze[f'{self.difficult_maze}']
        self._cell_size_h, self._cell_size_w = ((self.height / _ - 1) for _ in self.cells_sizes)
        self.sl = None  #здесь будут хранится список, хранящий наше решение для лабиринта
        self.map = None  #массив для хранения информации об объекте в каждой координате
        # (i = y, j = x если в координатной 2д плоскости)
        self.solution = [] #полный список со всеми обходами ячеек, который совершил алгоритм решения лабиринта
        self.load_map(self.cells_sizes)
        self.canvas = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        self.draw = Draw(self.canvas)

    def load_map(self, cells_sizes):
        """
                Загрузка карты лабиринта на основе уровня сложности.

                Параметры:
                    difficult_maze (tuple): кортеж с количеством ячеек по вертикали и по горизонтали.
        """
        folder = path.dirname(__file__)
        self.sl, self.solution = map_generator(*cells_sizes, self.txt_in_fn) #  формируем в списках решение
        self.map = Map(path.join(folder, self.txt_in_fn))

    def _recty(self, i, j, color, k=1):
        """
                Вспомогательный метод для отрисовки прямоугольника на изображении.

                Параметры:
                    i (int): Индекс строки.
                    j (int): Индекс столбца.
                    color (str): Цвет прямоугольника.
                    k (float): Множитель размера прямоугольника (по умолчанию 1).
        """
        y = self._cell_size_h * i
        x = self._cell_size_h * j
        self.draw.rectangle((x, y,
                             x + self._cell_size_w * k, y + self._cell_size_h * k),
                            fill=color)

    def rendering(self):
        """
               Метод визуализации лабиринта на изображении.

               Метод включает в себя три подметода для отрисовки различных элементов лабиринта:
               1. _render_initial_objects - отрисовка начального состояния лабиринта (стены, пути и т. д.).
               2. _render_solution_with_all_steps - отрисовка пути решения лабиринта с учетом всех шагов.
               3. _render_pure_solution - отрисовка чистого пути решения лабиринта без дополнительных элементов.

               Параметры:
                   Нет.

               Возвращаемые значения:
                   Нет.
        """
        def _render_initial_objects():
            """
                Подметод для отрисовки начального состояния лабиринта.

                Параметры:
                    Нет.

                Возвращаемые значения:
                    Нет.
            """
            dict_objects_in_maze = {
                2: 'blue',
                1: 'white',
                0: 'black',
                3: 'red'
            }
            for ind_i in range(len(self.map.data)):
                for ind_j in range(len(self.map.data[ind_i])):
                    self._recty(ind_i, ind_j, dict_objects_in_maze[self.map.data[ind_i][ind_j]])

        def _render_solution_with_all_steps():
            """
                Подметод для отрисовки пути решения лабиринта с учетом всех шагов.

                Параметры:
                    Нет.

                Возвращаемые значения:
                    Нет.
            """
            for col, k in self.solution:
                if col == 1:
                    color = 'yellow'
                else:
                    color = 'black'
                for n in k:
                    i = n[0]
                    j = n[1]
                    self._recty(i, j, color)

        def _render_pure_solution():
            """
                Подметод для отрисовки чистого пути решения лабиринта без дополнительных элементов.

                Параметры:
                        Нет.

                Возвращаемые значения:
                        Нет.
            """
            for i in range(len(self.sl)):
                for j in range(len(self.sl)):
                    if self.sl[i][j] == 1:
                        self._recty(i, j, 'blue', .7)

        _render_initial_objects()
        # _render_solution_with_all_steps()
        _render_pure_solution()
        self.save_img(self.img_out_fn)

    def save_img(self, file_name):
        """
            Сохранение изображения лабиринта.

            Параметры:
                file_name (str): Имя файла для сохранения изображения.
        """
        self.canvas.save(file_name)


parser = argparse.ArgumentParser(description='My example explanation')
parser.add_argument(
    '-image_output', '--img_o',
    type=str,
    default=f'{const.IMAGE_OUTPUT}',
    help='имя выходного файла для созданного лабиринта(image)',

)
parser.add_argument(
    '-text_output', '--txt_o',
    type=str,
    default=f'{const.TEXT_OUTPUT}',
    help='имя выходного файла для созданного лабиринта(.txt формат)',
)

parser.add_argument(
    '-text_input', '--txt_i',
    type=str,
    default=None,
    help='имя входного файла для создания лабиринта(.txt формат)',
)

parser.add_argument(
    '-width', '--w',
    type=int,
    default=f'{const.WIDTH}',
    help='ширина картинки',
)

parser.add_argument(
    '-height', '--h',
    type=int,
    default=f'{const.HEIGHT}',
    help='высота картинки'
)

parser.add_argument(
    '-difficult', '--dif',
    type=str,
    default=f'{const.DIFFICULT_MAZE_BASE}',
    help='параметр, отвечающий за сложность лабиринта(easy - маленькое количество путей в лабиринте,\n'
         'medium - среднее количество путей,\n'
         'hard - большое количество путей'
)

args = parser.parse_args()

app = Program(width=args.w, height=args.h,
              difficult_maze=args.dif, img_out_fn=args.img_o,
              txt_out_fn=args.txt_o, txt_in_fn=args.txt_i)
app.rendering()
