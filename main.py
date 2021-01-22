# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import math
from queue import PriorityQueue

WINDOW_LEN = 800
WIN = pygame.display.set_mode((WINDOW_LEN, WINDOW_LEN))
pygame.display.set_caption("A* Path Finding Algorithm")