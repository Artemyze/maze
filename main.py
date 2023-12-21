import argparse

from PIL.ImageDraw import Draw

import options as const
from map import Map
from maze import map_generator
from os import path
from PIL import Image


class Program:
    def __init__(self, width, height, difficult_maze, img_out_fn, txt_out_fn, txt_in_fn):
        self.dict_difficult_maze = {
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
        self.sl = None
        self.map = None
        self.solution = []
        self.solution_data = []
        self.load_map(self.cells_sizes)
        self.canvas = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        self.draw = Draw(self.canvas)

    def load_map(self, difficult_maze):
        folder = path.dirname(__file__)
        self.sl, self.solution = map_generator(*difficult_maze, self.txt_in_fn)
        self.map = Map(path.join(folder, self.txt_in_fn))

    def _recty(self, i, j, color, k=1):
        y = self._cell_size_h * i
        x = self._cell_size_h * j
        self.draw.rectangle((x, y,
                             x + self._cell_size_w * k, y + self._cell_size_h * k),
                            fill=color)

    def rendering(self):

        def _render_initial_objects():
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
            for i in range(len(self.sl)):
                for j in range(len(self.sl)):
                    if self.sl[i][j] == 1:
                        self._recty(i, j, 'blue', .7)

        _render_initial_objects()
        # _render_solution_with_all_steps()
        _render_pure_solution()
        self.save_img(self.img_out_fn)

    def save_img(self, file_name):
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
    default=f'{const.TEXT_OUTPUT}',
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
