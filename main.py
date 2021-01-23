import pygame
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
ORANGE = (255, 127, 0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE  # at the beginning all nodes are white
        self.adjacent_nodes = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == YELLOW

    def is_open(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset_color(self):
        self.color = WHITE

    def set_to_start(self):
        self.color = ORANGE

    def set_to_open(self):
        self.color = RED

    def set_to_closed(self):
        self.color = YELLOW

    def set_to_barrier(self):
        self.color = BLACK

    def set_to_end(self):
        self.color = PURPLE

    def set_path(self):
        self.color = GREEN

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_adjacent_nodes(self, node):
        self.adjacent_nodes = []
        # down
        if self.row < self.total_rows - 1 and not node[self.row + 1][self.col].is_barrier():
            self.adjacent_nodes.append(node[self.row + 1][self.col])
        # up
        if self.row > 0 and not node[self.row - 1][self.col].is_barrier():
            self.adjacent_nodes.append(node[self.row - 1][self.col])
        # right
        if self.col < self.total_rows - 1 and not node[self.row][self.col + 1].is_barrier():
            self.adjacent_nodes.append(node[self.row][self.col + 1])
        # left
        if self.col > 0 and not node[self.row][self.col - 1].is_barrier():
            self.adjacent_nodes.append(node[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# heuristic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def show_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


def a_star(draw, node, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in node for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in node for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            show_path(came_from, end, draw)
            end.set_to_end()
            return True

        for adjacent in current.adjacent_nodes:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[adjacent]:
                came_from[adjacent] = current
                g_score[adjacent] = temp_g_score
                f_score[adjacent] = temp_g_score + h(adjacent.get_pos(), end.get_pos())
                if adjacent not in open_set_hash:
                    count += 1
                    open_set.put((f_score[adjacent], count, adjacent))
                    open_set_hash.add(adjacent)
                    adjacent.set_to_open()

        draw()
        if current != start:
            current.set_to_closed()
    return False


def create_grid(rows, width):
    grid = []
    distance = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, distance, rows)
            grid[i].append(spot)

    return grid


def create_grid_lines(window, rows, width):
    distance = width // rows
    # horizontal lines
    for i in range(rows):
        pygame.draw.line(window, BLACK, (0, i * distance), (width, i * distance))
        # vertical lines
        for j in range(rows):
            pygame.draw.line(window, BLACK, (j * distance, 0), (j * distance, width))


def draw_grid(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for col in row:
            col.draw(window)

    create_grid_lines(window, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    y, x = pos
    distance = width // rows
    row = y // distance
    col = x // distance

    return row, col


def visualiser(window, width):
    rows = 50
    node = create_grid(rows, width)
    start = None
    end = None
    run = True

    while run:
        draw_grid(window, node, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                spot = node[row][col]
                if not start and spot != end:
                    start = spot
                    start.set_to_start()

                elif not end and spot != start:
                    end = spot
                    end.set_to_end()

                elif spot != start and spot != end:
                    spot.set_to_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)
                spot = node[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in node:
                        for spot in row:
                            spot.update_adjacent_nodes(node)
                    a_star(lambda: draw_grid(window, node, rows, width), node, start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    node = create_grid(rows, width)

    pygame.quit()


visualiser(WIN, WINDOW_LEN)
