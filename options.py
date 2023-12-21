# Установка ширины и высоты изображения
WIDTH = 1280
HEIGHT = 1024

# Имя файла для сохранения изображения и текстового представления лабиринта
IMAGE_OUTPUT = f'output.png'
TEXT_OUTPUT = f'map.txt'

# Определение базовой сложности лабиринта
DIFFICULT_MAZE_BASE = 'medium'

# Определение размеров лабиринта для разных уровней сложности
AMOUNT_CELLS_IN_W_EASY = 20
AMOUNT_CELLS_IN_H_EASY = 20
AMOUNT_CELLS_IN_W_MEDIUM = 40
AMOUNT_CELLS_IN_H_MEDIUM = 40
AMOUNT_CELLS_IN_W_HARD = 60
AMOUNT_CELLS_IN_H_HARD = 60

# Определение цветов для отображения элементов лабиринта
COLOR_S = 2  # Цвет стартовой клетки
COLOR_WALL = 1  # Цвет стен
COLOR_WAY = 0  # Цвет свободного пространства
COLOR_FINISH = 3  # Цвет финишной клетки
