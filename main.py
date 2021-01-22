# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import math
from queue import PriorityQueue

WINDOW_LEN = 800
WIN = pygame.display.set_mode((WINDOW_LEN, WINDOW_LEN))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = ( 255, 127, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE # at the beginning all nodes are white
        self.adjacent_nodes = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset_color(self):
        return self.color == WHITE

    def set_to_closed(self):
        self.color = RED

    def set_to_open(self):
        self.color = GREEN

    def set_to_barrier(self):
        self.color = BLACK

    def set_to_end(self):
        self.color = TURQUOISE

    def set_path(self):
        self.color = PURPLE

    def set_draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def upadate_adjacent_nodes(self,node):
        pass

    def __lt__(self, other):
        return False


# heurestic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


