import pygame
import math

from queue import PriorityQueue

WIDTH = 800

CANVAS = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm!")

RED = (255, 0 ,0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255 ,0)
WHITE = (255, 255 ,255)
BLACK = (0, 0 ,0)
PURPLE = (128, 0 ,128)
ORANGE = (255, 165 ,0)
GREY = (128, 128 ,128)
TURQUOISE = (64, 224 ,208)

class Cell:

    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.column

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
   
    def is_open(self):
        return self.color == GREEN
   
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
   
    def make_open(self):
        self.color = GREEN
   
    def make_start(self):
        self.color = BLUE
    
    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.column])

        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False

def get_h_score(point_1, point_2):

    x_1, y_1 = point_1
    x_2, y_2 = point_2
    
    return abs(x_1 - x_2) + abs(y_1 - y_2)

def reconstruct_path(previous_cells, current_cell, draw):
    while current_cell in previous_cells:
        current_cell = previous_cells[current_cell]
        current_cell.make_path()
        draw()

def algorithm(draw, grid, start_cell, end_cell):
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_cell))
    previous_cells = {}

    g_score = { cell: float("inf") for row in grid for cell in row }
    g_score[start_cell] = 0

    f_score = { cell: float("inf") for row in grid for cell in row }
    f_score[start_cell] = get_h_score(start_cell.get_position(), end_cell.get_position())

    open_set_hash = { start_cell }

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cell = open_set.get()[2]
        open_set_hash.remove(current_cell)

        if current_cell == end_cell:
            start_cell.make_start()
            end_cell.make_end()
            reconstruct_path(previous_cells, end_cell, draw)
            return True

        for neighbour in current_cell.neighbours:
            temp_g_score = g_score[current_cell] + 1

            if temp_g_score < g_score[neighbour]:
                previous_cells[neighbour] = current_cell
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + get_h_score(neighbour.get_position(), end_cell.get_position())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current_cell != start_cell:
            current_cell.make_closed()

    return False



def make_grid(rows, width):

    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid        

def draw_grid(canvas, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(canvas, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(canvas, GREY, (j * gap, 0), (j * gap, width))

def draw(canvas, grid, rows, width):
    canvas.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(canvas)

    draw_grid(canvas, rows, width)

    pygame.display.update()

def get_click_position(mouse_position, rows, width):

    gap = width // rows

    x, y = mouse_position

    column = x // gap
    row = y // gap

    return column, row

def main(canvas, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start_cell = None
    end_cell = None
    
    is_running = True

    while is_running:

        draw(canvas, grid, ROWS, width)

        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                is_running = False

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = get_click_position(position, ROWS, width)
                cell = grid[row][column]
                
                if not start_cell and cell != end_cell:
                    start_cell = cell
                    start_cell.make_start()

                elif not end_cell and cell != start_cell:
                    end_cell = cell
                    end_cell.make_end()

                elif cell != start_cell and cell != end_cell:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                 position = pygame.mouse.get_pos()
                 row, column = get_click_position(position, ROWS, width)
                 cell = grid[row][column]
                 cell.reset()

                 if cell == start_cell:
                     start_cell = None
                 elif cell == end_cell:
                     end_cell = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbours(grid)

                    algorithm(lambda: draw(canvas, grid ,ROWS, width), grid, start_cell, end_cell)

                if(event.key == pygame.K_ESCAPE):
                    start_cell = None
                    end_cell = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(CANVAS, WIDTH)