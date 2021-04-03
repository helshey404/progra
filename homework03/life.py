import pathlib
import random
from copy import deepcopy
from typing import List, Optional, Tuple

from pygame.locals import *

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = 20
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                if randomize:
                    val = random.randint(0, 1)
                else:
                    val = 0
                grid[i].append(val)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x1 = cell[0]
        y1 = cell[1]

        arr = []
        for i in range(x1 - 1, x1 + 2):
            for j in range(y1 - 1, y1 + 2):
                if 0 <= i <= self.rows - 1 and 0 <= j <= self.cols - 1:
                    if x1 != i or y1 != j:
                        arr.append(self.curr_generation[i][j])

        return arr

    def get_next_generation(self) -> Grid:
        grid_copy = deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                k = (i, j)
                s = sum(self.get_neighbours(k))
                if s != 2 and s != 3 and self.curr_generation[i][j] == 1:
                    grid_copy[i][j] = 0
                elif s == 3 and self.curr_generation[i][j] == 0:
                    grid_copy[i][j] = 1
        return grid_copy

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.n_generation = self.n_generation + 1



    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations >= self.n_generation

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "sample_read") as file:
            arr1 = [i.split() for i in file]
            arr2 = [list(str(arr1[i][0])) for i in range(len(arr1))]
            arr3 = [[int(j) for j in arr2[i]] for i in range(len(arr2))]
            return (arr3)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "sample_write")
        a = ["".join(map(str, self.curr_generation[i])) for i in range(len(self.curr_generation))]
        k = "\n".join(a)
        file.write(str(k))
        file.close()