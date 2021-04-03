import pygame
import random
from copy import copy, deepcopy

from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        self.grid = self.create_grid(True)
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.grid = self.get_next_generation()
            self.draw_grid()
            self.draw_lines()


            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        grid = []
        for i in range(self.cell_height):
            grid.append([])
            for j in range(self.cell_width):
                if randomize:
                    val = random.randint(0, 1)
                else:
                    val = 0
                grid[i].append(val)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        grid = self.grid
        x = 0
        y = self.cell_size * (-1)
        for i in range(self.cell_height):
            y = y + self.cell_size
            x = 0
            for j in range(self.cell_width):
                if grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.cell_size, self.cell_size))
                    x = x + self.cell_size
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))
                    x = x + self.cell_size

        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x = cell[0]
        y = cell[1]

        arr = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.cell_height - 1 >= 0 <= i and j >= 0 <= self.cell_width - 1:
                    if x != i or y != j:
                        arr.append(self.grid[i][j])

        return arr

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid_copy = deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                k = (i, j)
                s = sum(self.get_neighbours(k))
                if s != 2 and s != 3 and self.grid[i][j] == 1:
                    grid_copy[i][j] = 0
                elif s == 3 and self.grid[i][j] == 0:
                    grid_copy[i][j] = 1
        return grid_copy
