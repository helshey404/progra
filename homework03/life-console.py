import curses
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
        while life.generations <= life.max_generations and life.prev_generation != life.curr_generation:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            life.step()
            time.sleep(1)
        curses.endwin()

life = GameOfLife((50, 50))
ui = Console(life)
ui.run()