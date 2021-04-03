import sys

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.speed = speed
        self.cell_size = cell_size
        self.screen_size = (self.life.rows * self.cell_size, self.life.cols * self.cell_size)
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[0]))
        for y in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen_size[1], y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        x = 0
        y = self.cell_size * (-1)
        grid = self.life.curr_generation
        for i in range(self.life.rows):
            y = y + self.cell_size
            x = 0
            for j in range(self.life.cols):
                if grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.cell_size, self.cell_size))
                    x = x + self.cell_size
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))
                    x = x + self.cell_size

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    break
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    x = event.pos[0] // self.cell_size
                                    y = event.pos[1] // self.cell_size
                                    self.life.curr_generation[y][x] = 1
                                    self.draw_grid()
                                    self.draw_lines()
                                    pygame.display.flip()
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

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
ui = GUI(life)
ui.run()
