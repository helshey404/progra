import curses
import sys

import pygame
import time

from pygame.locals import *
from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        y, x = screen.getmaxyx()
        self.cons = curses.newwin(y, x, 0, 0)
        width = life.cols + 2
        height = life.rows + 2
        for i in range(height):
            for j in range(width):
                if (i == 0 and j == 0) or (i == height - 1 and j == width - 1) or (i == height - 1 and j == 0) or (
                        i == 0 and j == width - 1):
                    self.cons.addstr(i, j, '+')
                elif (i == 0 and 0 < j < width - 1) or (i == height - 1 and 0 < j < width - 1):
                    self.cons.addstr(i, j, '-')
                elif (j == 0 and 0 < i < height - 1) or (j == width - 1 and 0 < i < height - 1):
                    self.cons.addstr(i, j, '|')
        self.cons.refresh()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(len(life.curr_generation)):
            for j in range(len(life.curr_generation[i])):
                cell_status = life.curr_generation[i][j]
                if cell_status == 1:
                    self.cons.addch(i + 1, j + 1, "*")
                elif cell_status == 0:
                    self.cons.addch(i + 1, j + 1, " ")
        self.cons.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        while life.n_generation <= life.max_generations and life.prev_generation != life.curr_generation:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            life.step()
            time.sleep(1)
        curses.endwin()

cols, rows, max_gen= 80, 25, 10

if len(sys.argv) <= 1:
    print("default")
else:
    for j in range(1, len(sys.argv), 2):
        i = sys.argv[j]
        if i == "--help":
            print('input --rows <int> and --cols <int>\n'
                  'imput maximum of generations --max_generations <int>\n')
            exit(1)
        elif i == "--rows":
            rows = int(sys.argv[j+1])
        elif i == "--cols":
            cols = int(sys.argv[j+1])
        elif i == "--max_generations":
            max_gen = int(sys.argv[j+1])
        else:
            print("Error")
            exit(1)


life = GameOfLife((25, 80))


life = GameOfLife((rows, cols), max_generations=max_gen)
ui = Console(life)
ui.run()


